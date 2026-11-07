# Telagram-RAG-Bot# Telegram RAG Bot

A Telegram bot that answers questions using your own documents (PDF, DOCX, TXT) as a knowledge base. Every answer is generated only from the retrieved document fragments and comes with references to its sources. If the documents don't contain the answer, the bot says so instead of making something up.

## How it works

1. **Indexing** (`index.py`) – documents from the `docs/` folder are split into overlapping chunks (500 characters, 100 overlap), converted into multilingual embeddings and stored in a local ChromaDB database.
2. **Retrieval** (`rag.py`) – the user's question is embedded with the same model and the 3 most similar chunks are fetched from ChromaDB.
3. **Generation** (`llm.py`) – the chunks and the question are sent to an LLM (Groq) with strict instructions: answer only from the provided text, ignore any instructions inside the documents, and admit when there is no answer.
4. **Telegram interface** (`bot.py`) – the bot receives a message, shows a "typing…" indicator, runs the pipeline in a separate thread so it never blocks, and replies with the answer and its sources.

## Tech stack

- Python 3.12+ (developed on 3.13)
- [python-telegram-bot](https://python-telegram-bot.org/) – Telegram interface
- [ChromaDB](https://www.trychroma.com/) – vector database
- [sentence-transformers](https://www.sbert.net/) with `paraphrase-multilingual-MiniLM-L12-v2` – multilingual embeddings (works well with Ukrainian and English)
- [Contextifier](https://pypi.org/project/contextifier/) – text extraction and chunking for PDF/DOCX/TXT
- [Groq](https://groq.com/) API with `openai/gpt-oss-20b` – answer generation

## Project structure

```
├── bot.py            # Telegram bot (entry point)
├── rag.py            # RAG pipeline: search + LLM answer + sources
├── llm.py            # Groq request and prompt
├── index.py          # Builds the vector database from docs/
├── db.py             # ChromaDB client and collection
├── docs/             # Your documents (not tracked by git)
├── chroma_db/        # Vector database (generated, not tracked by git)
├── requirements.txt
└── .env              # Secrets (not tracked by git)
```

## Setup

### 1. Clone and create a virtual environment

```bash
git clone <repository-url>
cd Telegram-RAG-Bot
python -m venv .venv
```

Activate it:

- Windows: `.venv\Scripts\activate`
- Linux / macOS: `source .venv/bin/activate`

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

The first installation is large (several GB) because `sentence-transformers` pulls in PyTorch.

### 3. Create the `.env` file

In the project root create a file named `.env`:

```
BOT_TOKEN=your_telegram_bot_token
GROQ_API_KEY=your_groq_api_key
```

- Get the bot token from [@BotFather](https://t.me/BotFather) in Telegram (`/newbot`).
- Get the API key from the [Groq console](https://console.groq.com/).

Never commit this file – it is listed in `.gitignore`.

### 4. Add your documents

Create a `docs/` folder and put your `.pdf`, `.docx` or `.txt` files in it.

### 5. Build the knowledge base

```bash
python index.py
```

The first run also downloads the embedding model (about 470 MB). Run `index.py` again whenever you add or change documents.

### 6. Start the bot

```bash
python bot.py
```

Open your bot in Telegram, send `/start` and ask a question.

## Quick test without Telegram

```bash
python rag.py
```

Type a question in the terminal to see the answer and its sources.

## Notes and limitations

- The bot has no conversation memory: every question is answered independently.
- If the LLM request fails (network issue, rate limit, invalid key), the bot replies with a short error message and prints details to the console.
- Groq's free tier has rate limits; frequent requests may be temporarily rejected.
- Replies longer than Telegram's 4096-character limit are truncated.
- Keep your documents out of version control: the `docs/` folder is ignored by git on purpose.