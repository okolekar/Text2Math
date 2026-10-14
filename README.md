# MathGPT

A Streamlit math-problem assistant powered by Groq's `openai/gpt-oss-120b`. It can use a calculator for mathematical expressions and Wikipedia for factual lookups, then return a step-by-step explanation.

## Features

- Chat-style interface with conversation history
- Groq-hosted GPT OSS 120B model
- Calculator tool for mathematical expressions
- Wikipedia search tool for supporting information
- API key entry in the sidebar or through a local `.env` file

## Requirements

- Python 3.10 or later
- A Groq account and API key with access to `openai/gpt-oss-120b`

Model availability, account limits, and pricing are controlled by Groq and may change. Check your Groq account before making requests.

## Setup

Clone the repository and move into the project directory:

```bash
git clone https://github.com/okolekar/Text2Math.git
cd .
```

Create and activate a virtual environment:

```bash
python -m venv .venv
```

Linux/macOS:

```bash
source .venv/bin/activate
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

## Configure the API key

Either enter your Groq API key in the app's sidebar, or create a local `.env` file:

```bash
cp .env.example .env
```

Set `GROQ_API_KEY` in `.env` to your key. The `.env` file is excluded from Git; never commit or share your real API key.

## Run

```bash
streamlit run chat_app.py
```

Enter a math problem in the text area and select **Find my answer**. The app can use its calculator or Wikipedia tools when appropriate.

## Project structure

```text
.
├── chat_app.py       # Streamlit app and LangChain agent
├── requirements.txt  # Python dependencies
├── .env.example      # Example environment configuration
└── .gitignore        # Local files excluded from Git
```

## Notes

AI-generated explanations and calculations can be incorrect. Verify important results independently. The app sends prompts to Groq and may send search queries to Wikipedia when the agent uses those tools.
