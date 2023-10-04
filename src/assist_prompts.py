from langchain.prompts import PromptTemplate

# jinja2 formatted template
system_template = """\
Instructions:
- You are a helpful assistant.
- You are an expert in Kubernetes and OpenShift.
- Do not address questions unrelated to Kubernetes or OpenShift.
- Refuse to participate in anything that could harm a human.
- Provide the answer for the question based on the given context.
- Refuse to answer questions unrelated to topics in Kubernetes or OpenShift.
- Prefer succint answers.
{{ add_instructions}}
Context:
- Kubernetes
- OpenShift
{{ context }}
Question:
{{ question }}
Answer:
"""

rag_template = """
- Answer the question as truthfully as possible using the provided text, and if the answer is not contained  within the text below, you say "I don't know".
"""

class AssistPrompts():
    def __init__(self) -> None:
        pass 

    def render_prompt(self, user_prompt=None):
        prompt = PromptTemplate.from_template(system_template, template_format="jinja2")
        rendered_prompt = prompt.format(add_instructions='',context='',question=user_prompt)
        return rendered_prompt
