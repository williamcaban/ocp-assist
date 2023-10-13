import os, inspect

# workaround to disable UserWarning
import warnings
warnings.simplefilter("ignore", UserWarning)

from src.logger import Logger

# langchain
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

__llm_backends= os.environ.get('LLM_BACKENDS', 'ollama').replace(" ",'').split(',')

for __backend in __llm_backends:
    if os.environ.get('LOG_LEVEL', 'INFO') == 'DEBUG': 
       print(f"Loading libraries for {__backend}")
    match __backend:
        case 'ollama':
            from langchain.llms import Ollama 
        case 'tgi':
            from langchain.llms import HuggingFaceTextGenInference
        case 'openai':
            # openai
            import openai
        case 'watson':
            # watsonX (requires WansonX libraries)
            from ibm_watson_machine_learning.foundation_models import Model
            from ibm_watson_machine_learning.metanames import GenTextParamsMetaNames as GenParams
            from ibm_watson_machine_learning.foundation_models.extensions.langchain import WatsonxLLM
        case 'bam':
            # BAM lab
            from genai.extensions.langchain import LangChainInterface
            from genai.credentials import Credentials
            from genai.model import Model
            from genai.schemas import GenerateParams
        case _:
            print(f"WARNING: Unknown dependencies for {__backend}")

class LLMConfig():
    def __init__(self,backend='ollama', 
                 inference_url=None,
                 prompt_type=None,
                 api_key=None,
                 model=None, logger=None) -> None:
        self.logger = logger if logger else Logger(show_message=False).logger
        self.backend=os.environ.get('LLM_DEFAULT', backend)
        self.inference_url=inference_url
        self.prompt_type=prompt_type
        self.api_key=api_key
        self.model=model
        self.llm=None
        #self.set_prompt_format()  # FIXME: Not used right now
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
                # self.prefix="###"
                # self.suffix="###"
                pass

    def set_llm_instance(self, inference_url=None, api_key=None, model=None):
        self.logger.debug(f"[{inspect.stack()[0][3]}] {self.backend}")
        match self.backend:
            case 'openai':
                # URI end point:port for local inference server
                self.inference_url = os.environ.get('OPENAI_API_URL', inference_url) # use local LM Server if not defined
                self.api_key = os.environ.get('OPENAI_API_KEY', api_key) # use empty API Key if not defined
                self.model = os.environ.get('OPENAI_MODEL', model)
                self.openai_llm_instance()
            case 'ollama':
                # 
                self.inference_url = os.environ.get('OLLAMA_API_URL', inference_url) # use local LM Server if not defined
                self.api_key = os.environ.get('OLLAMA_API_KEY', api_key) # use empty API Key if not defined
                self.model = os.environ.get('OLLAMA_MODEL', model)
                self.ollama_llm_instance()  
            case 'tgi':
                self.inference_url = os.environ.get('TGI_API_URL', inference_url)
                self.api_key = os.environ.get('TGI_API_KEY', api_key) # use empty API Key if not defined
                self.model = os.environ.get('TGI_MODEL', model)
                self.tgi_llm_instance()
            case 'watson':
                self.inference_url = os.environ.get('WATSON_API_URL', inference_url)
                self.api_key = os.environ.get('WATSON_API_KEY', api_key)
                self.model = os.environ.get('WATSON_MODEL', model)
                self.watson_llm_instance()
            case 'bam':
                # BAM Research lab
                self.inference_url = os.environ.get('BAM_API_URL', inference_url)
                self.api_key = os.environ.get('BAM_API_KEY', api_key)
                self.model = os.environ.get('BAM_MODEL', model)
                self.bam_llm_instance()
            case _:
                print(f'ERROR: Unsupported LLM backend type {self.backend}')

    def openai_llm_instance(self):
        # TODO: This section need to be completed
        self.logger.warning(f"[{inspect.stack()[0][3]}] OpenAI LLM Backend is not implemented")
        self.llm=None

    def ollama_llm_instance(self):
        self.logger.debug(f"[{inspect.stack()[0][3]}] Creating Ollama LLM instance")
        self.llm = Ollama(
            base_url=self.inference_url,
            model=self.model,
            verbose=True,
            top_k=10,
            top_p=0.95,
            temperature=0.01,
            repeat_penalty=1.03,
            callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
        )
        self.logger.debug(f"[{inspect.stack()[0][3]}] Ollama LLM instance {self.llm}")

    def tgi_llm_instance(self):
        self.logger.debug(f"[{inspect.stack()[0][3]}] Creating Hugging Face TGI LLM instance")
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
        self.logger.debug(f"[{inspect.stack()[0][3]}] Hugging Face TGI LLM instance {self.llm}")
    
    def bam_llm_instance(self):
        """BAM Research Lab"""
        self.logger.debug(f"[{inspect.stack()[0][3]}] BAM LLM instance")
        creds = Credentials(api_key=self.api_key, 
                            api_endpoint=self.inference_url)
        params = GenerateParams(decoding_method="sample", 
                                max_new_tokens=512,
                                min_new_tokens=1,
                                random_seed=42,
                                top_k= 10,
                                top_p=0.95,
                                repetition_penalty=1.03,
                                temperature=0.05)
        self.llm = LangChainInterface(model=self.model,
                                      params=params, 
                                      credentials=creds)
        self.logger.debug(f"[{inspect.stack()[0][3]}] BAM LLM instance {self.llm}")


    def watson_llm_instance(self):
        self.logger.debug(f"[{inspect.stack()[0][3]}] Watson LLM instance")
        creds = {
            "url": self.inference_url, # example from https://heidloff.net/article/watsonx-langchain/ 
            "apikey": self.api_key
        }
        params = {
            GenParams.DECODING_METHOD: "sample",
            GenParams.MIN_NEW_TOKENS: 1,
            GenParams.MAX_NEW_TOKENS: 512,
            GenParams.RANDOM_SEED: 42,
            GenParams.TEMPERATURE: 0.05,
            GenParams.TOP_K: 10,
            GenParams.TOP_P: 0.95,
            GenParams.REPETITION_PENALTY: 1.03 # https://www.ibm.com/docs/en/watsonx-as-a-service?topic=models-parameters
        }
        # Watson models:
        # google/flan-ul2, google/flan-t5-xxl, eleutherai/gpt-neox-20b, bigcode/starcoder, 
        # meta-llama/llama-2-70b-chat, bigscience/mt0-xxl,
        # ibm/granite-13b-chat-v1, ibm/granite-13b-instruct-v1, ibm/mpt-7b-instruct
        llm_model = Model(model_id=self.model,
                         credentials=creds, 
                         params=params, 
                         project_id=os.environ.get('WATSON_PROJECT_ID', None)
                         )
        self.llm = WatsonxLLM(model=llm_model)
        self.logger.debug(f"[{inspect.stack()[0][3]}] Watson LLM instance {self.llm}")

    def status(self):
        return [f"{'LLM backend':<20} = {self.backend}",
                f"{'LLM url':<20} = {self.inference_url}",
                f"{'LLM model':<20} = {self.model}",
                f"{'LLM prompt_type':<20} = {self.prompt_type}"]

if __name__ == '__main__':
    # load environment variables from .env
    from dotenv import load_dotenv, find_dotenv
    _ = load_dotenv(find_dotenv()) # read local .env file

    #prompt="What is Kubernetes?"
    prompt = PromptTemplate(
        input_variables=["question"],
        template="""\
            {question}
            Instruction:
            - You are a helpful assistant with expertise in OpenShift and Kubernetes.
            - Do not address questions unrelated to Kubernetes or OpenShift.
            - Refuse to participate in anything that could harm a human.
            - Provide the answer for the question based on the given context.
            - Refuse to answer questions unrelated to topics in Kubernetes or OpenShift.
            - Prefer succinct answers with YAML examples.
            Answer:
            """,
    )

    llm_config=LLMConfig(backend='ollama')
    llm_chain=LLMChain(llm=llm_config.llm, prompt=prompt)

    q1="How to build an application in OpenShift"
    print(f"# Test 1: {q1}")
    print(llm_chain.run(q1))

    # system should reject this request
    q2="Tell me a joke"
    print(f"# Test 2: {q2}")
    print(llm_config.llm(q2))
    #llm_config.llm("Tell me a joke", callbacks=[StreamingStdOutCallbackHandler()])
