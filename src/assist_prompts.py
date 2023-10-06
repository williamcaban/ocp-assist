import os 

class AssistPrompts():
    def __init__(self) -> None:
        self.prompt_class = {}
        self.read_prompts()

    def read_prompts(self, dir_path='templates'):
        """Read jija template prompts from director"""
        for fname in os.listdir(path=dir_path):
            try:
                if os.path.isfile(os.path.join(dir_path, fname)) and fname.endswith('.prompt'):
                    self.prompt_class[fname[:-7]]=open(os.path.join(dir_path, fname), 'r').read()
                    #print(f"DEBUG: Loading {fname}...")
            except FileNotFoundError:
                print(f"The directory {dir_path} does not exist")
            except PermissionError:
                print(f"Permission denied to access the directory {dir_path}")
            except OSError as e:
                print(f"An OS error occurred: {e}")

    def get_prompt_template(self, prompt_class):
        """
        Return the Jija2 prompt template.
        If prompt_class do not exist return the default prompt
        If default prompt class do not exist return None.
        """
        return self.prompt_class.get(prompt_class, 
                                     self.prompt_class.get('default', None)
                                     )

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