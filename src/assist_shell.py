import cmd, re, os, inspect

from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

from src.logger import Logger

class AssistShell(cmd.Cmd):
    def preloop(self):
        self.intro = '\nWelcome to the OpenShift Assistant shell.\n'
        self.prompt = '(ocp_assist) '
        self.fname = 'ocp.chat'
        self.file = None
        self.memory = None
        self.logger = self.logger if 'logger' in dir(self) else Logger(show_message=False).logger
        self.answer_from_llm = False
        self.add_status_callback(self.status)
        self.prompt_class = 'default' # start with 'default' prompt class
        #self.prompt_classes = ['default']

    def set_logger(self, logger=None):
        self.logger = logger if logger else Logger(show_message=False).logger

    def default(self, arg):
        'Default action for prompts'
        self.process_prompt(arg)
        self.answer_from_llm = True
        
    def do_echo(self, arg):
        'Return the prompt'
        print(f"Input Prompt={arg}")

    def do_rephrase(self, arg):
        """Rephrase prompt for K8s context"""
        current_prompt_class=self.prompt_class
        self.prompt_class='rephrase'
        self.process_prompt(arg)
        print("\n")
        self.prompt_class=current_prompt_class

    def do_classify(self, arg):
        """Return a list identifying the K8s or OCP labels or topics for a given prompt"""
        current_prompt_class=self.prompt_class
        self.prompt_class='classification'
        if len(arg.split()) > 2:
            self.process_prompt(arg)
        else:
            print("[]")
        print("\n")
        self.prompt_class=current_prompt_class

    def do_assist(self, arg):
        """
        Assistant specific sub-commands.
        
        assist [<sub-command>] [<sub-command-options>]
        
            status                  : Display system status
            reset                   : Tells the agent to forget previous interactions and context
            record                  : Starts saving interaction to filename: record <file_name> (default to ocp.chat)
            playback                : Playback interaction from a filename: playback <file_name> (default to ocp.chat)
            forget                  : Removes saved interaction filename: forget <file_name> (default to ocp.chat)
            prompt <prompt_class>   : Return current prompt template or set new prompt class template
            who_are_you             : Identify assistant agent
        """
        arg_list = arg.split()

        try:
            sub_command = arg_list[0]
        except:
            sub_command = None

        try:
            param1 = arg_list[1]
        except:
            param1 = None
        
        match sub_command:
            case 'info':
                self.assist_info()
            case 'status':
                self.assist_status()
            case 'reset':
                self.assist_reset()
            case 'record':
                self.assist_record(param1)
            case 'forget':
                self.assist_forget(param1)
            case 'playback':
                self.assist_playback(param1)
            case 'prompt':
                self.assist_prompt_class(param1)
            case 'who_are_you':
                self.assist_who_are_you()
            case _:
                print('Unknown or missing <sub-command>')
                print(self.do_assist.__doc__)
        
    def assist_info(self):
        """
        Welcome to OpenShift Assistant shell. You may interact with this assistant using English natural language.
        Type help or ? for information on additional built-in commands.\n
        """
        print(self.assist_info.__doc__)

    def assist_who_are_you(self):
        print('Rocket Panda!!!')

    def assist_prompt_class(self, prompt_class=None):
        self.logger.debug(f"[{inspect.stack()[0][3]}] prompt_class={prompt_class}")

        if prompt_class != None:
            self.prompt_class=prompt_class

        prompt_template=PromptTemplate.from_template('')        
        if len(self.prompts_callbacks) > 0:
            for p in self.prompts_callbacks:
                prompt_template=prompt_template+p(self.prompt_class)
        else:
            prompt_template=prompt_template+'{user_input}'

        print(f"\nActive Prompt Class: {self.prompt_class}\nAvailable Prompt Classes:\n\t{list(self.prompt_classes)}\n")

        # Display current prompt template
        self.logger.debug(f"[{inspect.stack()[0][3]}] Active prompt class='{self.prompt_class}' with input variables='{prompt_template.input_variables}'"+
                          f"\nRAW_TEMPLATE\n"+
                          prompt_template.template)


    def assist_status(self):
        'Display the status of the system'
        msg=f"# SYSTEM STATUS\n{str('=')*15}"
        print(msg)
        for c in self.status_callbacks:
            for msg in c():
                print(f"- {msg}")

    def assist_reset(self):
        'Tells the agent to forget previous contexts.'
        self.clean_memory()
        print('My memory has been reset.')

    def do_exit(self, arg):
        'Exit assistant'
        print('Thank you for using OpenShift Assistant')
        self.close()
        return True
    
    def assist_record(self, arg):
        'Start saving interaction to filename: RECORD ocp.chat (default to ocp.chat)'
        if arg != None:
            self.fname = self.safe_fname(arg)
        self.file = open(self.fname, 'a')

    def assist_forget(self, arg):
        'Remove saved interaction filename: FORGET ocp.chat (default to ocp.chat)'
        self.remove(arg)
        print("I have forgotten our conversation.")

    def assist_playback(self, arg):
        'Playback interaction from a filename: PLAYBACK ocp.chat (default to ocp.chat)'
        self.close()
        if arg != None:
            fname = self.safe_fname(arg)
        else:
            fname = self.fname
        if os.path.exists(fname):
            f=open(fname, 'r')
            self.cmdqueue.extend(f.read().splitlines())
        else:
            print(f'I have no memory to replay.')

    def emptyline(self):
        """Invoked when empty line"""
        self.assist_info()

    def precmd(self, line):
        line = line.lower()
        if self.file and 'playback' not in line:
            print(line, file=self.file)
        return line
    
    def postcmd(self, stop: bool, line: str) -> bool:
        if self.answer_from_llm:
            msg = [
                "WARNING: This is an EXPERIMENTAL service.",
                "\nAlways verify the answers before executing commands on a live system.",
                "\nhttps://docs.openshift.com/container-platform/latest/welcome/index.html"
            ]
            length = max([len(s) for s in msg]) # get the size of the longest string
            print(f"\n{str('=')*length}\n{' '.join(msg)}\n{str('=')*length}")
        self.answer_from_llm = False
        return super().postcmd(stop, line)
    
    def close(self):
        if self.file:
            self.file.close()
            self.file = None

    def remove(self, arg=None):
        fname = ''
        if arg != None:
            fname = self.safe_fname(arg)
        else:
            fname = self.fname
        #print(f"Removing filename {fname}")
        if os.path.exists(fname):
            os.remove(fname)

    def safe_fname(self, fname):
        'clean provided string for a safe filename'
        unsafe_list = re.findall(r'[^A-Za-z0-9_\-\\]',fname)
        for c in unsafe_list:
            fname.replace(c,'_')
        if fname != '':
            safe_name = fname+".chat"
        else:
            safe_name = self.fname
        return safe_name
    
    def clean_memory(self):
        'Discard existing memory'
        self.close()
        self.remove()
        self.memory = None

    def set_llm(self,llm):
        self.llm=llm
        self.add_prompt_callback()
        self.build_chain()

    def add_status_callback(self, callback):
        'Add a status callback function. The callback function must return a string'
        try:
            self.status_callbacks
        except:
            self.status_callbacks = []
        self.status_callbacks.append(callback)

    def add_prompt_callback(self, callback=None):
        'Add a prompt callback function. The callback function must return a prompt string'
        try:
            self.prompts_callbacks
        except:
            # assume these need creation
            self.prompts_callbacks = []
            self.prompt_class = 'default'
        
        if callback != None:
            self.prompts_callbacks.append(callback)
            self.build_chain()

    def build_chain(self):
        prompt_template=PromptTemplate.from_template('')
        
        if len(self.prompts_callbacks) > 0:
            for p in self.prompts_callbacks:
                prompt_template=prompt_template+p(self.prompt_class)
        else:
            self.logger.debug(f"[{inspect.stack()[0][3]}] Cannot find 'prompts_callbacks' defined, using direct interaction")
            prompt_template=prompt_template+'{user_input}'

        # Enable verbosity=True to see the raw prompt sent to the model
        self.llm_chain = LLMChain(llm=self.llm, prompt=prompt_template, verbose=False)
 
    def process_prompt(self, raw_prompt):
        # rebuild chain if using a non-default prompt_class
        #if self.prompt_class != 'default':
        self.logger.debug(f"[{inspect.stack()[0][3]}] Found prompt_class='{self.prompt_class}'. Building LLMChain...")
        self.build_chain()

        input_dict = self.llm_chain.input_schema().dict()
        input_dict['user_input']=raw_prompt

        for k in input_dict.keys():
            input_dict[k]='' if input_dict[k] is None else input_dict[k] 

        try:
            #print(self.llm_chain.run(**input_dict))
            self.llm_chain.run(**input_dict)
        except Exception as e:
            print(f"\nERROR: Ooops. There is something wrong with the backend LLM: {type(e).__name__}")
    
    def status(self):
        return [f"{'Assistant Shell':<20} = operational",
                f"{'Assistant Chains':<20} = {self.llm_chain.llm}"]

if __name__ == '__main__':
    AssistShell().cmdloop()