import cmd, re, os

from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

class AssistShell(cmd.Cmd):
    def preloop(self):
        self.intro = '\nWelcome to the OpenShift Assistant shell.\n'
        self.prompt = '(ocp_assist) '
        self.fname = 'ocp.chat'
        self.file = None
        self.memory = None
        self.answer_from_llm = False
        self.add_status_callback(self.status)

    def default(self, arg):
        'Default action for prompts'
        self.process_prompt(arg)
        self.answer_from_llm = True
        #return answer

    def do_info(self, arg):
        """
        Welcome to OpenShift Assistant shell. You may interact with this assistant using English natural language.
        Type help or ? for information on additional built-in commands.\n
        """
        print(self.do_info.__doc__)

    def do_who_are_you(self, arg):
        print('Rocket Panda!!!')

    def do_status(self, arg):
        'Display the status of the system'
        msg=f"# SYSTEM STATUS\n{str('=')*15}"
        print(msg)
        for c in self.status_callbacks:
            for msg in c():
                print(f"- {msg}")

    def do_reset(self, arg):
        'Tells the agent to forget previous contexts.'
        self.clean_memory()
        print('My memory has been reset.')

    def do_exit(self, arg):
        'Stop recording, and exit assistant'
        print('Thank you for using OpenShift Assistant')
        self.close()
        return True
    
    def do_record(self, arg):
        'Start saving interaction to filename: RECORD ocp.chat (default to ocp.chat)'
        if arg != None:
            self.fname = self.safe_fname(arg)
        self.file = open(self.fname, 'a')

    def do_forget(self, arg):
        'Remove saved interaction filename: FORGET ocp.chat (default to ocp.chat)'
        self.remove(arg)
        print("I have forgotten our conversation.")

    def do_playback(self, arg):
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
            self.prompts_callbacks = []
        
        if callback != None:
            self.prompts_callbacks.append(callback)
            self.build_chain()

    def build_chain(self, prompt_class='default'):
        prompt_template=PromptTemplate.from_template('')
        
        if len(self.prompts_callbacks) > 0:
            for p in self.prompts_callbacks:
                prompt_template=prompt_template+p(prompt_class)
        else:
            prompt_template=prompt_template+'{user_input}'

        self.llm_chain = LLMChain(llm=self.llm, prompt=prompt_template, verbose=True)
 
    def process_prompt(self, raw_prompt, prompt_class='default'):
        # rebuild chain if using a non-default prompt_class
        if prompt_class != 'default':
            self.build_chain(prompt_class=prompt_class)

        input_dict = self.llm_chain.input_schema().dict()
        input_dict['user_input']=raw_prompt

        for k in input_dict.keys():
            input_dict[k]='' if input_dict[k] is None else input_dict[k] 

        print(self.llm_chain.run(**input_dict))
    
    def status(self):
        return [f"{'Assistant Shell':<20} = operational",
                f"{'Assistant Chains':<20} = {self.llm_chain.llm}"]

if __name__ == '__main__':
    AssistShell().cmdloop()