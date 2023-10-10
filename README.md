# ABOUT

This is a POC experimenting with CLI-based agent experience.

## Running the POC

- Create a `.env` file to pass environment variables for the script

```bash
# LLM Backends to enable (comma separated list)
LLM_BACKENDS=tgi,bam

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
| &check;       | Integration with WatsonX          |
| &cross;       | ~~Integration with OpenAI~~ (removed) |
| &check;       | Class for multi-LLM backend       |
| &check;       | Prompt templates directory        |
| &check;       | Runtime switch of prompt template |
| &cross;       | Debugging hooks with class        |
| &cross;       | Runtime switch of LLM-backend     |

