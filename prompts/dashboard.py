from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
# from langchain.agents.format_scratchpad import 
import os

def create_prompt():
    prompt = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template_file(f"prompt_templates{os.sep}dashboard_system.txt", input_variables=[]),
        HumanMessagePromptTemplate.from_template_file(f"prompt_templates{os.sep}dashboard_user.txt", input_variables=[]),
    ])

    return prompt