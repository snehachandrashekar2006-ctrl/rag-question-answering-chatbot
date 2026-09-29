import os
import pickle
import html

import streamlit as st
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from groq import Groq


st.set_page_config(
    page_title="RAG Knowledge Chatbot",
    page_icon="📚",
    layout="centered"
)

st.html("""
<style>
.stApp { background:#080d18; color:#f8fafc; }
.block-container { max-width:900px; padding-top:25px; padding-bottom:80px; }
.hero { text-align:center; padding:10px 0 5px; }
.hero-icon { font-size:42px; }
.hero-title { font-size:34px; font-weight:750; color:#f8fafc; margin-bottom:6px; }
.hero-subtitle { color:#94a3b8; font-size:14px; margin-bottom:20px; }
.status { display:inline-flex; gap:7px; background:#0d1b17; border:1px solid #1f493d;
          color:#72e6c3; padding:5px 12px; border-radius:20px; font-size:11px; }
.status-dot { width:7px; height:7px; background:#4ade80; border-radius:50%; }
.badges { display:flex; justify-content:center; gap:8px; flex-wrap:wrap; margin:18px 0 28px; }
.badge { background:#101827; border:1px solid #263653; border-radius:20px;
         padding:7px 13px; color:#cbd5e1; font-size:11px; }
section[data-testid="stSidebar"] { background:#0b1424; border-right:1px solid #1e2b42; }
.sidebar-title { color:#f8fafc; font-size:18px; font-weight:700; margin-bottom:8px; }
.sidebar-text { color:#aab6c8; font-size:13px; line-height:1.6; }
.system-row { display:flex; justify-content:space-between; padding:7px 0;
              color:#cbd5e1; font-size:13px; border-bottom:1px solid #172238; }
.system-value { color:#8ab4ff; font-weight:600; }
.answer-label { color:#8ab4ff; font-size:10px; font-weight:700;
                letter-spacing:1.2px; margin-bottom:5px; }
.source-header { margin-top:12px; padding-top:10px; border-top:1px solid #263653;
                 color:#70e1c0; font-size:12px; font-weight:600; }
.source-card { background:#0e1727; border:1px solid #263653; border-radius:12px;
               padding:14px; margin:9px 0; }
.source-top { display:flex; justify-content:space-between; margin-bottom:9px; }
.source-id { color:#8ab4ff; font-size:11px; font-weight:700; }
.similarity { color:#72e6c3; font-size:11px; background:#0b211b;
              padding:4px 8px; border-radius:10px; }
.source-text { color:#cbd5e1; font-size:12px; line-height:1.6; }
.footer { text-align:center; color:#526075; font-size:10px; margin-top:30px;
          padding-top:15px; }
</style>

<div class="hero">
    <div class="hero-icon">📚</div>
    <div class="hero-title">RAG Knowledge Chatbot</div>
    <div class="hero-subtitle">Ask questions from the Wikipedia knowledge base</div>
    <div class="status"><span class="status-dot"></span>System Online</div>
</div>

<div class="badges">
    <div class="badge">🧠 MiniLM Embeddings</div>
    <div class="badge">🔎 FAISS Retrieval</div>
    <div class="badge">⚡ Groq LLM</div>
    <div class="badge">📖 Source Citations</div>
</div>
""")

DATA_FOLDER = "data"
MIN_SCORE = 0.70


@st.cache_resource
def load_rag_data():
    with open(f"{DATA_FOLDER}/all_chunks.pkl", "rb") as f:
        all_chunks = pickle.load(f)

    index = faiss.read_index(f"{DATA_FOLDER}/faiss.index")

    embedding_model = SentenceTransformer(
        "sentence-transformers/all-MiniLM-L6-v2"
    )

    return all_chunks, index, embedding_model


all_chunks, index, embedding_model = load_rag_data()


@st.cache_resource
def get_groq_client():
    key = os.environ.get("GROQ_API_KEY")
    if not key:
        raise RuntimeError(
            "GROQ_API_KEY is not set. Add your Groq API key before running the app."
        )
    return Groq(api_key=key)


client = get_groq_client()


with st.sidebar:
    st.html("""
    <div class="sidebar-title">📚 About</div>
    <div class="sidebar-text">
    This chatbot uses Retrieval-Augmented Generation (RAG)
    to answer questions from the Wikipedia knowledge base.
    </div>
    """)

    st.divider()

    st.html("""
    <div class="sidebar-title">⚙️ System</div>
    <div class="system-row"><span>Documents</span><span class="system-value">3,200</span></div>
    <div class="system-row"><span>QA Pairs</span><span class="system-value">918</span></div>
    <div class="system-row"><span>Chunks</span><span class="system-value">4,682</span></div>
    <div class="system-row"><span>Embedding</span><span class="system-value">MiniLM</span></div>
    <div class="system-row"><span>Retrieval</span><span class="system-value">FAISS</span></div>
    <div class="system-row"><span>LLM</span><span class="system-value">GPT-OSS-20B</span></div>
    """)

    st.divider()

    if st.button("🧹 Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.divider()

    st.html("""
    <div class="sidebar-text">
    💡 <b>How it works</b><br><br>
    1. Question → embedding<br>
    2. FAISS searches the knowledge base<br>
    3. Relevant chunks are retrieved<br>
    4. Groq generates the answer<br>
    5. Source IDs are displayed
    </div>
    """)


def retrieve(question, k=3):
    query_embedding = embedding_model.encode(
        [question],
        normalize_embeddings=True
    )
    query_embedding = np.asarray(query_embedding, dtype="float32")

    distances, indices = index.search(query_embedding, k)
    return distances[0], indices[0]


def generate_answer(question):
    distances, indices = retrieve(question, k=3)
    best_score = float(distances[0])

    if best_score < MIN_SCORE:
        return "I don't know.", [], best_score, distances, indices

    context_parts = []
    source_ids = []

    for score, i in zip(distances, indices):
        context_parts.append(
            f"Source ID: {all_chunks[i]['passage_id']}\n"
            f"{all_chunks[i]['chunk']}"
        )
        source_ids.append(all_chunks[i]["passage_id"])

    context = "\n\n".join(context_parts)
    source_ids = list(dict.fromkeys(source_ids))

    prompt = f"""
Answer the question using ONLY the context.

Give the answer first in a clear and direct way.

If the answer is not present in the context,
reply exactly: I don't know.

Do not mention Source IDs in the answer.
Do not make up information.

Context:
{context}

Question:
{question}
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
        max_tokens=150,
        include_reasoning=False
    )

    answer = response.choices[0].message.content.strip()

    if "i don't know" in answer.lower():
        answer = "I don't know."

    return answer, source_ids, best_score, distances, indices


if "messages" not in st.session_state:
    st.session_state.messages = []


for message in st.session_state.messages:
    avatar = "🧑" if message["role"] == "user" else "🤖"

    with st.chat_message(message["role"], avatar=avatar):
        if message["role"] == "assistant":
            st.markdown(
                '<div class="answer-label">ANSWER</div>',
                unsafe_allow_html=True
            )
        st.write(message["content"])


question = st.chat_input("Ask something from the knowledge base...")


if question:
    with st.chat_message("user", avatar="🧑"):
        st.write(question)

    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("🔎 Searching the knowledge base..."):
            answer, source_ids, score, distances, indices = generate_answer(question)

        st.markdown(
            '<div class="answer-label">ANSWER</div>',
            unsafe_allow_html=True
        )
        st.write(answer)

        if source_ids:
            st.html(
                f'<div class="source-header">📌 Retrieved Sources: '
                f'{", ".join(map(str, source_ids))}</div>'
            )

            with st.expander("📖 View retrieved documents"):
                for similarity, i in zip(distances, indices):
                    source_id = all_chunks[i]["passage_id"]
                    safe_text = html.escape(all_chunks[i]["chunk"])

                    st.html(f"""
                    <div class="source-card">
                        <div class="source-top">
                            <div class="source-id">📄 Source ID: {source_id}</div>
                            <div class="similarity">Similarity: {similarity:.3f}</div>
                        </div>
                        <div class="source-text">{safe_text}</div>
                    </div>
                    """)

        else:
            st.warning(
                f"⚠️ No sufficiently relevant source found "
                f"(similarity: {score:.3f})"
            )

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })


st.html("""
<div class="footer">
Built with RAG • Sentence Transformers • FAISS • Groq • Streamlit
</div>
""")
