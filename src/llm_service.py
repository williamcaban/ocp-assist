import os

# workaround to disable UserWarning
import warnings
warnings.simplefilter("ignore", UserWarning)

# openai
import openai

# langchain
from langchain.llms import HuggingFaceTextGenInference
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

class LLMConfig():
    def __init__(self,backend='tgi', 
                 inference_url=None,
                 prompt_type='llama2',
                 api_key=None) -> None:
        self.backend=backend
        self.inference_url=inference_url
        self.prompt_type=prompt_type
        self.api_key=api_key
        self.llm=None
        self.set_prompt_format()
        self.set_llm_instance()
    
    def set_prompt_format(self):
        match self.prompt_type:
            case 'llama2':
                self.prefix='[INST]'
                self.suffix='[/INST]'
            case 'alpaca':
                self.prefix="### Instruction:\n"
                self.suffix="\n### Response:"
            case 'openai':
                self.prefix="### Instruction:\n"
                self.suffix="\n### Response:"
            case _:
                self.prefix="###"
                self.suffix="###"

    def set_llm_instance(self):
        match self.backend:
            case 'openai':
                # URI end point:port for local inference server
                openai.api_base = os.environ.get('OPENAI_API_BASE', 'http://localhost:1234/v1') # use local LM Server if not defined
                openai.api_key = os.environ.get('OPENAI_API_KEY','') # use empty API Key if not defined

                # TODO: This section need to be completed
                self.llm=None
            case 'tgi':
                self.inference_url = os.environ.get('TGI_SERVER_URL','http://localhost:8010/')
                self.tgi_llm_instance()
            case _:
                print(f'ERROR: Unsupported LLM backend type {self.backend}')

    def tgi_llm_instance(self):
        self.llm = HuggingFaceTextGenInference(
            inference_server_url=self.inference_url,
            max_new_tokens=512,
            top_k=10,
            top_p=0.95,
            typical_p=0.95,
            temperature=0.01,
            repetition_penalty=1.03,
            streaming=True
        )

    def status(self):
        return f"LLM backend={self.backend}\nLLM url={self.inference_url}\nLLM prompt_type={self.prompt_type}"


if __name__ == '__main__':
    llm_config=LLMConfig()
    llm_config.llm("Tell me a joke", callbacks=[StreamingStdOutCallbackHandler()])