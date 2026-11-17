# AutoScript --- AI-Powered Code Completion for Visual Studio Code

AutoScript is an AI-assisted code-completion project that connects a
Visual Studio Code extension to a Python backend and an LLM inference
API. The backend receives a code prefix, sends it to the configured
model through Groq, and returns the generated continuation to the
extension.

> **Project status:** The VS Code extension is published in the Visual
> Studio Marketplace. This GitHub repository currently contains the
> FastAPI backend service; the extension's client-side source is not
> included in this repository.

## Features

-   AI-assisted inline code continuation from a supplied code prefix.
-   FastAPI endpoint for receiving completion requests.
-   Groq API integration using the `llama-3.3-70b-versatile` model
    identifier.
-   Prompt instructions designed to continue existing code, preserve
    indentation, and avoid repeating the supplied prefix.
-   Environment-variable-based API-key configuration.
-   Render deployment configuration.

## Architecture

``` text
Visual Studio Code extension
          |
          | POST /complete
          | { "prefix": "...", "language": "python" }
          v
     FastAPI backend
          |
          | Groq chat-completions API
          v
  Llama 3.3 70B Versatile
          |
          | generated continuation
          v
     FastAPI response
          |
          v
Visual Studio Code extension
```

The backend's current request model accepts `prefix` and an optional
`language` field. The current implementation sends the prefix to the
model; the language field is accepted but is not yet incorporated into
the prompt.

## Technology stack

-   **Language:** Python
-   **Backend:** FastAPI
-   **Model inference provider:** Groq
-   **Model identifier configured in code:** `llama-3.3-70b-versatile`
-   **Request validation:** Pydantic
-   **HTTP client:** Requests
-   **Configuration:** python-dotenv and environment variables
-   **Deployment configuration:** Render

## Repository structure

``` text
AutoScript/
├── main.py
├── requirements.txt
├── render.yaml
└── README.md
```

## Run the backend locally

### 1. Clone the repository

``` bash
git clone https://github.com/adityayadav13/AutoScript.git
cd AutoScript
```

### 2. Create and activate a virtual environment

``` bash
python -m venv .venv
```

On macOS/Linux:

``` bash
source .venv/bin/activate
```

On Windows PowerShell:

``` powershell
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

``` bash
pip install -r requirements.txt
```

### 4. Configure the API key

Create a `.env` file in the project root:

``` env
GROQ_API_KEY=your_groq_api_key
```

Do not commit `.env` or expose your API key in source code, screenshots,
logs, or public repositories.

### 5. Start the API server

``` bash
uvicorn main:app --reload
```

The local API will be available at:

``` text
http://127.0.0.1:8000
```

FastAPI's interactive API documentation is available at:

``` text
http://127.0.0.1:8000/docs
```

## API usage

### Health check

``` http
GET /
```

Example response:

``` json
{
  "status": "AutoScript Backend Running ✔"
}
```

### Request a code completion

``` http
POST /complete
Content-Type: application/json
```

Example request:

``` json
{
  "prefix": "def calculate_total(items):\n    total = 0\n",
  "language": "python"
}
```

Example response shape:

``` json
{
  "completion": "    for item in items:\n        total += item\n    return total"
}
```

The generated completion is model-dependent; the response above is
illustrative, not a guaranteed output.

## Configuration and deployment

The backend reads `GROQ_API_KEY` from the environment. For local
development, `python-dotenv` can load it from `.env`. In a hosted
environment, configure the key as a secret environment variable in the
hosting provider.

A `render.yaml` file is included for Render deployment. The service
starts with:

``` bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```

## Important implementation notes

-   The model identifier is currently configured in `main.py`.
-   The backend currently returns an empty completion when the upstream
    Groq request returns a non-200 response. More detailed error
    handling and request timeouts would improve reliability.
-   The current CORS configuration is permissive. For a production
    deployment, restrict allowed origins to the required extension or
    application origins.
-   The backend currently logs the submitted code prefix. Avoid logging
    potentially sensitive source code; consider removing or redacting
    this output.
-   The `language` request field is currently accepted but not used in
    the model prompt.
-   This repository does not include a test suite or the VS Code
    extension's client-side source code at present.

## Links

-   **GitHub repository:** https://github.com/adityayadav13/AutoScript
-   **Visual Studio Marketplace:**
    https://marketplace.visualstudio.com/items?itemName=Adityayadav.autoscript

## Future improvements

Potential areas for further development include:

-   Incorporating the programming-language field into prompt
    construction.
-   Adding request timeouts, structured error responses, and retry
    handling.
-   Restricting CORS and removing sensitive code from logs.
-   Adding automated tests for the API and upstream-provider failure
    cases.
-   Documenting the extension's commands, configuration, and user
    workflow.
-   Publishing the extension client source alongside the backend or
    linking its source repository.

## Author

**Aditya Yadav**

This project explores the integration of large language models into
developer tooling through an IDE extension and an API-based inference
backend.
