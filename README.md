
# RAG Question-Answering Chatbot

A Retrieval-Augmented Generation (RAG) chatbot that answers questions using a Mini Wikipedia knowledge base.

The system retrieves relevant information using semantic search and generates answers using an LLM, while displaying the retrieved source IDs.

---

## 🚀 Project Overview

This project implements a complete RAG-based Question-Answering system.

Instead of directly asking an LLM to answer a question, the system first searches a knowledge base for relevant information and then provides that information to the LLM as context.

### Workflow

```text
User Question
      ↓
Sentence Transformer
      ↓
Embedding
      ↓
FAISS Similarity Search
      ↓
Relevant Wikipedia Chunks
      ↓
GPT-OSS-20B through Groq
      ↓
Generated Answer
      ↓
Source IDs
````

---

## 🛠️ Technologies Used

| Technology            | Purpose                         |
| --------------------- | ------------------------------- |
| Python                | Main programming language       |
| Streamlit             | Chatbot user interface          |
| Sentence Transformers | Text embeddings                 |
| all-MiniLM-L6-v2      | Embedding model                 |
| FAISS                 | Similarity search and retrieval |
| Groq API              | LLM inference                   |
| GPT-OSS-20B           | Answer generation               |
| Hugging Face Datasets | Mini Wikipedia dataset          |

---

## 📊 Dataset

The project uses the **RAG Mini Wikipedia** dataset.

* **3,200** Wikipedia passages
* **918** question-answer pairs
* **4,682** chunks after text chunking

Each document is divided into smaller chunks before generating embeddings.

---

## 📁 Project Structure

```text
rag-question-answering-chatbot/
│
├── app.py
│   └── Frontend / Streamlit chatbot
│
├── task1.py
│   └── Backend / dataset processing, chunking,
│       embeddings and FAISS index creation
│
├── README.md
│   └── Project documentation
│
├── requirements.txt
│   └── Python dependencies
│
├── .gitignore
│   └── Files excluded from Git
│
└── output/
    └── Streamlit application screenshots
```

---

## ⚙️ How It Works

### 1. Document Processing

The Mini Wikipedia passages are loaded and divided into smaller chunks.

### 2. Embeddings

Each chunk is converted into a numerical vector using:

```text
all-MiniLM-L6-v2
```

### 3. FAISS Retrieval

The embeddings are stored in a FAISS index.

When a user asks a question, the question is also converted into an embedding and FAISS searches for the most similar chunks.

### 4. Answer Generation

The retrieved chunks are provided as context to:

```text
GPT-OSS-20B
```

through the Groq API.

The model generates an answer using only the retrieved context.

### 5. Source Citations

The application displays the source IDs and similarity scores of the retrieved documents.

If no sufficiently relevant information is found, the chatbot responds:

```text
I don't know.
```

---

## 🖥️ Screenshots

### Home Page

![Home Page](output/01.%20home%20page.png)

### Working Model

![Working Model](output/02.%20Working%20Model.png)

### Unknown Answer Handling

![Unknown Answer](output/03.%20Unknown%20answer.png)

### Retrieved Sources

![Retrieved Sources](output/04.%20Working%20model%201.png)

### Question Answering

![Question Answering](output/05.%20Working%20model%202.png)

---

## ▶️ How to Run

### 1. Clone the repository

```bash
git clone https://github.com/snehachandrashekar2006-ctrl/rag-question-answering-chatbot.git
cd rag-question-answering-chatbot
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set the Groq API key

Set your Groq API key as an environment variable.

**Windows PowerShell:**

```powershell
$env:GROQ_API_KEY="YOUR_GROQ_API_KEY"
```

**Linux/macOS:**

```bash
export GROQ_API_KEY="YOUR_GROQ_API_KEY"
```

Never upload your API key to GitHub.

### 4. Build the backend

```bash
python task1.py
```

This creates:

```text
data/all_chunks.pkl
data/faiss.index
```

### 5. Start Streamlit

```bash
streamlit run app.py
```

The chatbot will open in your browser.

---

## ✨ Features

* Retrieval-Augmented Generation
* Semantic search using embeddings
* FAISS vector similarity search
* GPT-OSS-20B answer generation
* Groq API integration
* Source ID display
* Similarity scores
* "I don't know" handling for low-confidence retrieval
* Interactive Streamlit chatbot interface
* Retrieved document viewer

---

## 🔒 Security

API keys and generated data files are excluded from GitHub using `.gitignore`.

Do not upload:

* Groq API keys
* `.env` files
* `faiss.index`
* `all_chunks.pkl`

---

Yes bro 👍 Let's make the README **CV/portfolio-ready**.

### 1. Open `README.md` on GitHub

Click **README.md → ✏️ Edit**.

### 2. Replace the entire content with this

````markdown
# RAG Question-Answering Chatbot

A Retrieval-Augmented Generation (RAG) chatbot that answers questions using a Mini Wikipedia knowledge base.

The system retrieves relevant information using semantic search and generates answers using an LLM, while displaying the retrieved source IDs.

---

## 🚀 Project Overview

This project implements a complete RAG-based Question-Answering system.

Instead of directly asking an LLM to answer a question, the system first searches a knowledge base for relevant information and then provides that information to the LLM as context.

### Workflow

```text
User Question
      ↓
Sentence Transformer
      ↓
Embedding
      ↓
FAISS Similarity Search
      ↓
Relevant Wikipedia Chunks
      ↓
GPT-OSS-20B through Groq
      ↓
Generated Answer
      ↓
Source IDs
````

---

## 🛠️ Technologies Used

| Technology            | Purpose                         |
| --------------------- | ------------------------------- |
| Python                | Main programming language       |
| Streamlit             | Chatbot user interface          |
| Sentence Transformers | Text embeddings                 |
| all-MiniLM-L6-v2      | Embedding model                 |
| FAISS                 | Similarity search and retrieval |
| Groq API              | LLM inference                   |
| GPT-OSS-20B           | Answer generation               |
| Hugging Face Datasets | Mini Wikipedia dataset          |

---

## 📊 Dataset

The project uses the **RAG Mini Wikipedia** dataset.

* **3,200** Wikipedia passages
* **918** question-answer pairs
* **4,682** chunks after text chunking

Each document is divided into smaller chunks before generating embeddings.

---

## 📁 Project Structure

```text
rag-question-answering-chatbot/
│
├── app.py
│   └── Frontend / Streamlit chatbot
│
├── task1.py
│   └── Backend / dataset processing, chunking,
│       embeddings and FAISS index creation
│
├── README.md
│   └── Project documentation
│
├── requirements.txt
│   └── Python dependencies
│
├── .gitignore
│   └── Files excluded from Git
│
└── output/
    └── Streamlit application screenshots
```

---

## ⚙️ How It Works

### 1. Document Processing

The Mini Wikipedia passages are loaded and divided into smaller chunks.

### 2. Embeddings

Each chunk is converted into a numerical vector using:

```text
all-MiniLM-L6-v2
```

### 3. FAISS Retrieval

The embeddings are stored in a FAISS index.

When a user asks a question, the question is also converted into an embedding and FAISS searches for the most similar chunks.

### 4. Answer Generation

The retrieved chunks are provided as context to:

```text
GPT-OSS-20B
```

through the Groq API.

The model generates an answer using only the retrieved context.

### 5. Source Citations

The application displays the source IDs and similarity scores of the retrieved documents.

If no sufficiently relevant information is found, the chatbot responds:

```text
I don't know.
```

---

## 🖥️ Screenshots

### Home Page

![Home Page](output/01.%20home%20page.png)

### Working Model

![Working Model](output/02.%20Working%20Model.png)

### Unknown Answer Handling

![Unknown Answer](output/03.%20Unknown%20answer.png)

### Retrieved Sources

![Retrieved Sources](output/04.%20Working%20model%201.png)

### Question Answering

![Question Answering](output/05.%20Working%20model%202.png)

---

## ▶️ How to Run

### 1. Clone the repository

```bash
git clone https://github.com/snehachandrashekar2006-ctrl/rag-question-answering-chatbot.git
cd rag-question-answering-chatbot
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set the Groq API key

Set your Groq API key as an environment variable.

**Windows PowerShell:**

```powershell
$env:GROQ_API_KEY="YOUR_GROQ_API_KEY"
```

**Linux/macOS:**

```bash
export GROQ_API_KEY="YOUR_GROQ_API_KEY"
```

Never upload your API key to GitHub.

### 4. Build the backend

```bash
python task1.py
```

This creates:

```text
data/all_chunks.pkl
data/faiss.index
```

### 5. Start Streamlit

```bash
streamlit run app.py
```

The chatbot will open in your browser.

---

## ✨ Features

* Retrieval-Augmented Generation
* Semantic search using embeddings
* FAISS vector similarity search
* GPT-OSS-20B answer generation
* Groq API integration
* Source ID display
* Similarity scores
* "I don't know" handling for low-confidence retrieval
* Interactive Streamlit chatbot interface
* Retrieved document viewer

---

## 🔒 Security

API keys and generated data files are excluded from GitHub using `.gitignore`.

Do not upload:

* Groq API keys
* `.env` files
* `faiss.index`
* `all_chunks.pkl`

---

## 👩‍💻 Author

**Sneha C**

AI & Data Science Student

GitHub:
[https://github.com/snehachandrashekar2006-ctrl](https://github.com/snehachandrashekar2006-ctrl)

````


