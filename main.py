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
    assist.set_llm(llm_config.llm)
    assist.add_prompt_callback(assist_prompts.render_prompt)
    assist.add_status_callback(llm_config.status)
    assist.cmdloop()

if __name__ == '__main__':
    main()