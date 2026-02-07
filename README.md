# Local AI PowerPoint Editor (LM Studio Agent)

A local, offline PowerPoint‑editing agent that rewrites slide text using a locally hosted LLM (LM Studio or any OpenAI‑compatible endpoint). The agent reads `.pptx` files, sends slide text to the model with a selected editing mode, and writes the updated presentation back to disk.

---

## Features

- Local‑only LLM calls (no cloud dependency)
- `.env` configuration stored in the parent directory
- Multiple editing modes:
  - **shorten** — compress text while preserving structure
  - **simplify** — rewrite for clarity and general audiences
  - **formalize** — rewrite in a professional tone
- Dry‑run mode for safe previews
- Clean CLI interface with argument validation
- Modular architecture ready for expansion

---

## Requirements

- Python 3.10+
- LM Studio (or any OpenAI‑compatible local server)
- Python packages:
  - `python-pptx`
  - `requests`
  - `python-dotenv`

Install dependencies:

```bash
pip install python-pptx requests python-dotenv
```

## Environment Configuration

The agent loads its settings from a `.env` file located **one directory above** the script. This keeps credentials and model configuration separate from the codebase.

Create a `.env` file in the parent directory with the following entries:

| Variable | Description |
| :--- | :--- |
| **LOCAL_LLM_ENDPOINT** | URL of the local OpenAI‑compatible server (LM Studio or equivalent). |
| **MODEL_NAME** | The model identifier exposed by the local server. |
| **DEFAULT_MODE** | Editing mode used when processing slides (`shorten`, `simplify`, or `formalize`). |
| **API_KEY** | Only needed if the local endpoint requires authentication. |

> **Note:** The script will exit if the `.env` file is missing or the endpoint variable is not set.

---

## Command‑Line Usage

### Test LLM Connectivity
Sends a simple prompt to confirm that the local LLM endpoint and model are responding.

```bash
python agent.py --action testapi
```

Sends a simple prompt to confirm that the local LLM endpoint and model are responding.

## Process a PowerPoint File

Run the agent in processing mode to rewrite slide text using the editing mode defined in the `.env` file:

```bash
python agent.py --action process path/to/file.pptx
```

The script will open the presentation, extract text from each slide, send it to the local LLM with the selected system prompt, and apply the rewritten text back into the file.


