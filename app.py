import os
import PyPDF2
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import streamlit as st
import google.generativeai as genai
from langchain.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

LOGO_URL_LARGE='https://upload.wikimedia.org/wikipedia/commons/8/8c/SENAI_S%C3%A3o_Paulo_logo.png'

load_dotenv()
os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}


# read all pdf files and return text
def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PyPDF2.PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text



def main():
    
    st.logo(LOGO_URL_LARGE, link=None, icon_image=None)
    st.set_page_config(
        page_title="Assistente MSEP",
        page_icon="🤖",
    )

    # Sidebar for uploading PDF files
    st.image(LOGO_URL_LARGE)
    with st.sidebar:
        st.title("Menu:")
        nomeCurso = st.text_input("Nome do Curso:", "")
        nomeUC = st.text_input("Nome da Unidade Curricular:", "")
        tipoDocumento = st.selectbox("Selecione o tipo de documento", ("Plano de Ensino", "Cronograma", "Plano de Aula"))
        if(tipoDocumento=='Plano de Ensino'):   
            qntSituacoesAprendizagem = st.number_input("Quantidade de estratégias de aprendizagem:",min_value=1)
        estrategiaAprendizagem = st.selectbox("Selecione a estratégia de aprendizagem", ("Situação-Problema", "Estudo de Caso", "Projeto Integrador", "Projetos","Pesquisa Aplicada"))
        pdf_docs = st.file_uploader("Carregue seus arquivos PDF e clique no botão Enviar e Processar", type='.pdf',accept_multiple_files=True)
        if st.button("Enviar & Processar"):
            with st.spinner("Processando..."):
                raw_text = get_pdf_text(pdf_docs)
                print(raw_text)


                # Abrindo o arquivo no modo de escrita ("w")
                with open("meu_arquivo.txt", "w") as arquivo:
                # Escrevendo o texto no arquivo
                    arquivo.write(raw_text)


                #text_chunks = get_text_chunks(raw_text)
                #get_vector_store(text_chunks)
                st.success("Concluído")
        if st.button("Gerar "+tipoDocumento):
            with st.spinner("Processando..."):
                 st.success("Concluído")

    # Main content area for displaying chat messages
    st.title("Assistente MSEP")
    st.write("Bem vindo ao assistente do professor!")
    #st.sidebar.button('Limpar histórico do chat', on_click=clear_chat_history)

    # Chat input
    # Placeholder for chat messages

    if "messages" not in st.session_state.keys():
        st.session_state.messages = [
            {"role": "assistant", "content": "Carregue um plano de curso e elabore o documento desejado."}]

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    if prompt := st.chat_input():
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

    # Display chat messages and bot response
    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            with st.spinner("Pensando..."):
                response = user_input(prompt)
                placeholder = st.empty()
                full_response = ''
                for item in response['output_text']:
                    full_response += item
                    placeholder.markdown(full_response)
                placeholder.markdown(full_response)
        if response is not None:
            message = {"role": "assistant", "content": full_response}
            st.session_state.messages.append(message)

if __name__ == "__main__":
    main()