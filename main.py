# load environment variables from .env
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file

# custom classes
from src.llm_service import LLMConfig
from src.assist_shell import AssistShell
from src.assist_prompts import AssistPrompts

def main():
    assist_prompts=AssistPrompts()
    llm_config=LLMConfig()
    assist=AssistShell()

    #print("DEBUG [main]: Setting assistant.llm")
    assist.set_llm(llm_config.llm)
    #print("DEBUG [main]: Adding prompt_callback")
    assist.add_prompt_callback(assist_prompts.get_prompt_template)
    #print("DEBUG [main]: Adding status_callback")
    assist.add_status_callback(llm_config.status)
    #print("DEBUG [main]: Adding invoking cmdloop")
    assist.cmdloop()

if __name__ == '__main__':
    main()