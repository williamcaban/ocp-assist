# ABOUT

This is a POC experimenting with CLI-based agent experience.

## Running the POC

- Create a `.env` file to pass environment variables for the script

```bash
# if using Hugging Face TGI local endpont
TGI_SERVER_URL=<url_for_your_tgi_inference_endpoint>
# if using OpenAI
OPENAI_API_KEY=sk-<your_key_here>
# if using a local OpenAI drop-in replacement
OPENAI_API_BASE=<local_url>
```

- Create a Python 3.11+ virtual environment and install dependencies
```bash
python3.11 -m venv venv
pip install -r requirements
```

- Execute the main agent script
```bash
python main.py
```