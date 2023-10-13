import os 
from src.logger import Logger

class AssistPrompts():
    def __init__(self, prompt_class='default', logger=None) -> None:
        self.logger = logger if logger else Logger(show_message=False).logger
        self.prompt_collection = {'default':'Return a JSON with key msg and value string "{user_input}"'}
        self.prompt_class = prompt_class
        self.load_prompts()

    def load_prompts(self, dir_path='templates'):
        """Read jija template prompts from director"""
        for fname in os.listdir(path=dir_path):
            try:
                if os.path.isfile(os.path.join(dir_path, fname)) and fname.endswith('.prompt'):
                    self.prompt_collection[fname[:-7]]=open(os.path.join(dir_path, fname), 'r').read()
                    #print(f"DEBUG: Loading {fname}...")
            except FileNotFoundError:
                print(f"The directory {dir_path} does not exist")
            except PermissionError:
                print(f"Permission denied to access the directory {dir_path}")
            except OSError as e:
                print(f"An OS error occurred: {e}")

    def get_prompt_classes(self):
        self.logger.debug(f"Available Prompt Classes: {list(self.prompt_collection.keys())}")
        return self.prompt_collection.keys()

    def get_prompt_template(self, prompt_class='default'):
        """
        Return the f-string formatted prompt template.
        If prompt_class do not exist return the default prompt
        If default prompt class do not exist return None.
        """
        return self.prompt_collection.get(prompt_class, 
                                     self.prompt_collection.get('default', None)
                                     )




    # def set_llm(self,llm):
    #     self.llm=llm
    #     self.add_prompt_callback()
    #     self.build_chain()

    # def build_chain(self, prompt_class='default'):
    #     prompt_template=PromptTemplate.from_template('')
        
    #     if len(self.prompts_callbacks) > 0:
    #         for p in self.prompts_callbacks:
    #             prompt_template=prompt_template+self.get_prompt_template(prompt_class)
    #     else:
    #         prompt_template=prompt_template+'{user_input}'

    #     self.llm_chain = LLMChain(llm=self.llm, prompt=prompt_template, verbose=True)
 
    # def process_prompt(self, raw_prompt, prompt_class='default'):
    #     # rebuild chain if using a non-default prompt_class
    #     if prompt_class != 'default':
    #         self.build_chain(prompt_class=prompt_class)

    #     input_dict = self.llm_chain.input_schema().dict()
    #     input_dict['user_input']=raw_prompt

    #     for k in input_dict.keys():
    #         input_dict[k]='' if input_dict[k] is None else input_dict[k] 

    #     print(self.llm_chain.run(**input_dict))
    


    # def render_prompt(self, user_prompt=None, add_instructions='',context=''):
    #     """
    #     user_prompt:        cleaned question submitted by the user
    #     add_instructions:   additional instruction for the system
    #     context:            additional context to pass for the system
    #     """
    #     prompt = PromptTemplate.from_template(system_template_general, template_format="jinja2")
    #     rendered_prompt = prompt.format(add_instructions=add_instructions,
    #                                     context=context,
    #                                     question=user_prompt)
    #     return rendered_prompt
    
    # def classify_prompt(self, user_prompt=None, add_instructions='',topics=''):
    #     """
    #     user_prompt:        cleaned question submitted by the user
    #     add_instructions:   additional instruction for the system
    #     topics:             additional topics for classification to pass for the system
    #     """
    #     prompt = PromptTemplate.from_template(system_template_classification, template_format="jinja2")
    #     rendered_prompt = prompt.format(add_instructions=add_instructions,
    #                                     topics=topics,
    #                                     question=user_prompt)
    #     return rendered_prompt


if __name__ == '__main__':
    prompt_templates = AssistPrompts()
    print(f"{'#'*20} {'Prompt classes':^30} {'#'*20}\n{prompt_templates.prompt_class.keys()}")
    print(f"{'#'*20} {'Default prompt':^30} {'#'*20}\n{prompt_templates.get_prompt_template('default')}")
    print(f"{'#'*20} {'Handling non-existent prompt':^30} {'#'*20}\n{prompt_templates.get_prompt_template('foo')}")