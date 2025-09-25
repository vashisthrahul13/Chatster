
# ChatSter

A **general-purpose chatbot** built using [LangGraph](https://github.com/langchain-ai/langgraph), designed for multi-threaded conversations with persistent storage, an interactive front-end, and support for multiple LLMs.

---

## ✨ Features

* **Multi-threaded Conversations**

  * Create, reset, and switch across multiple chat sessions.
  * Persistent conversation history stored with **SQLite**.

* **Interactive Streamlit Frontend**

  * Real-time streaming of chatbot responses.
  * Clean, intuitive UI for managing multiple conversations.

* **Support for tool calling**
  * Real time search results using google search integration.
  * MySQL database interaction support and with safe query checking.
  * Multiple other tools implemented

* **LLM Flexibility**

  * Plug-and-play integration with different **LLMs**, including custom fine-tuned models.
  * Ongoing benchmarking with **LangSmith** for performance tracking.

* **Scalable & Extensible**

  * Designed with modularity in mind to support future **multimodal integration** (text + images + more).

---

## 📸 Demo

### Chat Interface

![Chat Interface Demo](assets/chat_interface.png)

### Multi-Thread Conversation Management

![Multi-thread Demo](assets/multithread_demo.gif)

---

## 📂 Project Structure

```
├── langgraph_backend.py     # Backend: LangGraph pipeline, thread management, persistence
├── frontend_multithread.py  # Frontend: Streamlit app with multithread chat support
├── requirements.txt         # Python dependencies
├── assets/                  # (Optional) screenshots and GIFs for README
└── README.md                # Project documentation
```

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/langgraph-chatbot.git
cd langgraph-chatbot
```

### 2. Install Dependencies

It is recommended to use a virtual environment:

```bash
pip install -r requirements.txt
```

### 3. Set Environment Variables

Create a `.env` file in the project root and add your API keys (e.g., OpenAI):

```env
OPENAI_API_KEY=your_openai_key_here
LANGSMITH_API_KEY=your_langsmith_key_here   # optional, for benchmarking
```

### 4. Run the Backend

The backend manages LangGraph workflows and persistent conversation storage.

```bash
python langgraph_backend.py
```

### 5. Run the Frontend

Launch the Streamlit interface:

```bash
streamlit run frontend_multithread.py
```

---

## 🖥️ Usage

1. Open the Streamlit app in your browser (default: `http://localhost:8501`).
2. Start a new conversation thread or continue from previous ones.
3. Switch between multiple active threads.
4. Enjoy real-time chatbot responses powered by LangGraph.

---

## 🔮 Roadmap

* ✅ Multi-threaded conversation management
* ✅ S3QLite persistence
* ✅ Streamlit real-time streaming
* 🔄 LLM benchmarking with LangSmith
* 🔮 Multimodal integration (text + images, documents)
* 🔮 Deployment on cloud (Docker + Kubernetes)

