# ABOUT

This is a POC experimenting with CLI-based agent experience.

## Running the POC

Note: If running the POC locally `ollama` can be used as backend. If like to run `ollama` on OpenShift check [ollama-ubi](https://github.com/williamcaban/ollama-ubi) repo for instructions.

- Create a `.env` file to pass environment variables for the script

```bash
# LLM Backends to enable (comma separated list)
LLM_BACKENDS=ollama,tgi
LLM_DEFAULT=ollama         # default LLM backend

# If using Ollama
# Some models: codellama, llama2, mistral:7b-instruct-q4_K_M, mistral
OLLAMA_API_URL=http://localhost:11434   # update to match your Ollama server
OLLAMA_MODEL=mistral:7b-instruct-q4_K_M # update to match your model

# if using Hugging Face TGI local endpont
TGI_API_URL=<url_for_your_tgi_inference_endpoint>
TGI_API_KEY=<optional_key>
TGI_MODEL=<model_name>

# if using OpenAI
OPENAI_API_URL=<local_url> # if using a local OpenAI drop-in replacement
OPENAI_API_KEY=sk-<your_key_here>
OPENAI_MODEL=<model_name>

# if using IBM WatsonX
WATSON_API_URL=<your_watsonx_url> # if using non-default URL
WATSON_API_KEY=<your_watsonx_key>
WATSON_PROJECT_ID=<your_watsonx_project_id> 
WATSON_MODEL=ibm/granite-13b-instruct-v1
#WATSON_MODEL=ibm/granite-13b-chat-v1

# If using BAM research lab
BAM_API_URL=<url_for_api_endpoing>
BAM_API_KEY=<api_key>
BAM_MODEL=<model_name>
```

- Create a Python 3.11+ virtual environment and install dependencies. **NOTE**: Must use Python 3.11 or higher.
```bash
python3.11 -m venv venv
pip install -r requirements.txt
```

- Execute the main agent script
```bash
python main.py
```

## TO-DO

Current features and progress
- &check; = completed
- &cross; = not available

| Available?    | Description                       |
|:-------------:| --------------------------------- |
| &check;       | Integration with TGI w/LLAMAv2    |
| &check;       | Integration with Ollama (any Ollama model) |
| &check;       | Integration with WatsonX (any WatsonX model) |
| &cross;       | ~~Integration with OpenAI~~ (removed) |
| &check;       | Class for multi-LLM backend       |
| &check;       | Prompt templates directory        |
| &check;       | Runtime switch of prompt template |
| &check;       | Debugging hooks with class (use logger class) |
| &cross;       | Add memory for context continuity during chat |
| &cross;       | Runtime switch of LLM-backend     |
| &cross;       | Move LLM logic from assist class to dedicated class |
| &cross;       | Decouple CLI client from backend with client/server archicture|
| &cross;       | Live connection/retrieval from Kuberenes/OpenShift cluster|
