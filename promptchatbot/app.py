# Bring in deps
import os
from apikey import apikey

import streamlit as st
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain.utilities import WikipediaAPIWrapper

# Set OpenAI API key
os.environ['OPENAI_API_KEY'] = apikey

# App framework
st.title('Test bot')
prompt = st.text_input('Plug in the topic here')

# Check if there's a prompt
if prompt:
   

    question_template = PromptTemplate(
            input_variables=['topic', 'wikipedia_research','answer'],
            template='create 5 multiple-choice question and answer with the following information: QUESTION: {topic} OPTIONS: {wikipedia_research} ANSWER: {wikipedia_research}'
    )



    # Memory
    
    question_memory = ConversationBufferMemory(input_key='topic', memory_key='chat_history')
    

    # Llms
    llm = OpenAI(temperature=0.9)
  
    question_chain = LLMChain(llm=llm, prompt=question_template, verbose=True, output_key='question', memory=question_memory)
   
    wiki = WikipediaAPIWrapper()

    # Run chains
   
    
    wiki_research = wiki.run(prompt)
    question = question_chain.run(topic=prompt, wikipedia_research=wiki_research)
    

    
    st.write("Question:", question)
  
    


    
    with st.expander('Question history'):
        st.info(question_memory.buffer)

    with st.expander('Wikipedia Research'):
        st.info(wiki_research)
else:
    st.warning("Please enter your topic.")
