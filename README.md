# 🪶 Poet’s Atelier — AI Prosody Analyzer & Anthology Book Studio

**Poet’s Atelier** is an end-to-end Generative AI creative writing studio built with **Python**, **Streamlit**, **Groq LLM API**, **ChromaDB**, and **Sentence-Transformers**. It helps poets evaluate rhyme schemes, meter, and line-by-line craft flaws, compare drafts against classic poems from the **Poetry Foundation dataset**, archive manuscripts for iterative revision, and automatically compile saved poems into a print-ready `.docx` anthology book.

---

## ✨ Key Features

- **🔍 Prosody & Rhyme Scheme Diagnostics:** Automatically detects exact rhyme schemes (`ABAB`, `AABB`, `Free Verse`, etc.), dominant meter, literary devices, and assigns a structured Craft Score (`1–100`) using Pydantic-validated JSON outputs.
- **🪄 Line-by-Line Critique & One-Click Revision:** Flags forced rhymes, broken meter, clichés, and weak verbs with concrete rewrite suggestions that can be applied directly to the draft in a single click.
- **📚 Literary Archive RAG (Poetry Foundation Dataset):** Embeds published poems locally using `all-MiniLM-L6-v2` and **ChromaDB** to surface stylistically similar classic works alongside every critique.
- **📜 Persistent Manuscript Vault:** Saves drafts, themes, and revision timestamps in a local **SQLite** database (`poems.db`) so poets can reload and refine poems over time.
- **📖 Automated Anthology Book Compiler:** Groups saved manuscripts into thematic chapters, generates chapter epigraphs and a literary preface, and exports a formatted **Microsoft Word (`.docx`)** book manuscript.
- **🎨 Illuminated Midnight Velvet & Gold UI:** Custom CSS glassmorphism interface with GPU-accelerated aurora animations, floating starlight motes, and editorial serif typography (`Cinzel Decorative`, `Cormorant Garamond`, `Lora`).

---

## 🛠️ Tech Stack

| Layer | Technology |
| :--- | :--- |
| **Frontend & UI** | Streamlit + Custom CSS / Google Fonts |
| **LLM Inference** | Groq API (auto-detects active Llama / Qwen chat models) |
| **Structured Outputs** | Pydantic v2 (`PoemAnalysis`, `PoetryBookPlan`) |
| **Dataset & RAG** | Hugging Face `datasets` (`Poetry-Foundation-Poems`), ChromaDB, `sentence-transformers` (`all-MiniLM-L6-v2`) |
| **Database** | SQLite (`poems.db`) |
| **Book Export** | `python-docx` |

---

## 📁 Project Structure

```text
poet-buddy/
├── .streamlit/
│   └── config.toml          # Midnight velvet & burnished gold theme config
├── .env                     # Environment variables (GROQ_API_KEY)
├── requirements.txt         # Python dependencies
├── prepare_dataset.py       # Downloads & indexes Poetry Foundation dataset into ChromaDB
├── database.py              # SQLite CRUD operations for the Manuscript Vault
├── poetry_engine.py         # Groq LLM prosody analyzer, RAG search & book planner
├── book_exporter.py         # Compiles structured book plan into a .docx file
├── app.py                   # Multi-tab Streamlit web application
└── README.md                # Project documentation
