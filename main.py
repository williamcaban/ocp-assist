# load environment variables from .env
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file

# custom classes
from src.llm_service import LLMConfig
from src.assist_shell import AssistShell
from src.assist_prompts import AssistPrompts
from src.logger import Logger

def main():
    logger=Logger().logger

    assist_prompts=AssistPrompts(logger=logger)
    llm_config=LLMConfig(logger=logger)
    assist=AssistShell()

    assist.set_logger(logger=logger)
    assist.set_llm(llm_config.llm)
    assist.add_prompt_callback(assist_prompts.get_prompt_template)
    assist.add_status_callback(llm_config.status)
    assist.prompt_classes=assist_prompts.get_prompt_classes()
    assist.cmdloop()

if __name__ == '__main__':
    main()