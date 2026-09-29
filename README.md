# RAG Question-Answering Chatbot

A Retrieval-Augmented Generation (RAG) chatbot that answers questions using a Mini Wikipedia knowledge base.

## Project Structure

```text
rag-question-answering-chatbot/
│
├── app.py                 # Frontend / Streamlit application
├── task1.py               # Backend: dataset, chunking, embeddings and FAISS
├── README.md              # Project documentation
├── requirements.txt       # Python dependencies
├── .gitignore             # Files excluded from Git
│
├── data/
│   ├── all_chunks.pkl     # Generated locally by task1.py
│   └── faiss.index        # Generated locally by task1.py
│
└── output/
    ├── screenshot-1.png
    ├── screenshot-2.png
    └── ...
```

## How It Works

```text
User Question
      ↓
MiniLM Embedding
      ↓
FAISS Similarity Search
      ↓
Relevant Wikipedia Chunks
      ↓
GPT-OSS-20B through Groq
      ↓
Answer + Source IDs
```

## Technologies

- Python
- Streamlit
- Sentence Transformers
- `all-MiniLM-L6-v2`
- FAISS
- Groq API
- `openai/gpt-oss-20b`
- Hugging Face Datasets

## Dataset

RAG Mini Wikipedia contains:

- 3,200 passages
- 918 question-answer pairs
- 4,682 chunks after chunking

## Run the Project

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Set the Groq API key

Windows PowerShell:

```powershell
$env:GROQ_API_KEY="YOUR_GROQ_API_KEY"
```

Linux/macOS:

```bash
export GROQ_API_KEY="YOUR_GROQ_API_KEY"
```

Never upload the API key to GitHub.

### 3. Build the RAG backend

```bash
python task1.py
```

This creates:

```text
data/all_chunks.pkl
data/faiss.index
```

### 4. Start Streamlit

```bash
streamlit run app.py
```

## Features

- Semantic retrieval using embeddings
- FAISS similarity search
- Context-based LLM answers
- Source ID display
- "I don't know" response when retrieval confidence is low
- Streamlit chatbot interface
- Retrieved-document viewer

## Output

Screenshots of the Streamlit application are stored in the `output/` folder.

## Important

The generated FAISS index and chunk file are not included in GitHub because they are generated data files. Run `task1.py` to create them locally.
