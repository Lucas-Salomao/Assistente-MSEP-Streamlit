import PyPDF2
import streamlit as st
import google.generativeai as genai
import pymupdf
import fitz

LOGO_VERMELHO='https://upload.wikimedia.org/wikipedia/commons/8/8c/SENAI_S%C3%A3o_Paulo_logo.png'
LOGO_AZUL='https://logodownload.org/wp-content/uploads/2019/08/senai-logo-1.png'

docs_raw=''

generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-pro",
  generation_config=generation_config,
  # safety_settings = Adjust safety settings
  # See https://ai.google.dev/gemini-api/docs/safety-settings
  system_instruction="Você é um especialista em educação profissional, que trabalha no Senai São Paulo, que orienta os professores a como usar a metodologia senai de educação profissional para elaborar planos de ensino, cronogramas e planos de aula",
)

chat_session = model.start_chat(
  history=[
  ]
)



def get_gemini_reponse(prompt,raw_text):
    contexto=raw_text
    response = chat_session.send_message(raw_text+prompt)
    return response.text

# read all pdf files and return text
def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PyPDF2.PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def get_pdf_text_v2(pdf_docs):

    text = ""
    for pdf in pdf_docs:
        pdf_bytes = pdf.getvalue()
        # Open the PDF with PyMuPDF (fitz) using the bytes
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        for page in doc:
            text += page.get_text()
    return text

def main():
    global docs_raw
    st.logo(LOGO_AZUL, link=None, icon_image=None)
    
    st.set_page_config(
        page_title="Assistente MSEP",
        page_icon="🤖",
        menu_items={'Get Help': 'https://www.extremelycoolapp.com/help','Report a bug': "mailto:lucas.salomao@gmail.com",'About': "SENAI São Paulo - Gerência de Educação\n\nSupervisão de Tecnologias Educacionais - Guilherme Dias\n\nCriado por Lucas Salomão"}
    )

    # Sidebar for uploading PDF files
    st.image(LOGO_AZUL,width=200)
    with st.sidebar:
        st.title("Menu:")
        apiKeyGoogleAiStudio = st.text_input("Chave API Google AI Studio:", "",type='password')
        nomeCurso = st.text_input("Nome do Curso:", "")
        nomeUC = st.text_input("Nome da Unidade Curricular:", "")
        tipoDocumento = st.selectbox("Selecione o tipo de documento", ("Plano de Ensino", "Cronograma", "Plano de Aula"))
        if(tipoDocumento=='Plano de Ensino'):   
            qntSituacoesAprendizagem = st.number_input("Quantidade de estratégias de aprendizagem:",min_value=1)
        estrategiaAprendizagem = st.selectbox("Selecione a estratégia de aprendizagem", ("Situação-Problema", "Estudo de Caso", "Projeto Integrador", "Projetos","Pesquisa Aplicada"))
        pdf_docs = st.file_uploader("Carregue seus arquivos PDF e clique no botão Enviar e Processar", type='.pdf',accept_multiple_files=True,help='Faça o upload da MSEP e de um plano de curso que deseja elaborar os documentos de prática docente.')
        if st.button("Processar documentos"):
            with st.spinner("Processando..."):
                raw_text = get_pdf_text_v2(pdf_docs)
                docs_raw=raw_text
                #print(raw_text)


                # Abrindo o arquivo no modo de escrita ("w")
                with open("meu_arquivo.txt", "w") as arquivo:
                # Escrevendo o texto no arquivo
                    arquivo.write(raw_text)

                st.success("Concluído")
        if st.button("Gerar "+tipoDocumento):
            with st.spinner("Processando..."):
                # if(tipoDocumento=='Plano de Aula'):

                # if(tipoDocumento=='Plano de Aula'):
                # if(tipoDocumento=='Plano de Aula'):
                
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

    if prompt := st.chat_input(placeholder=''):
        genai.configure(api_key=apiKeyGoogleAiStudio)
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)
    # Display chat messages and bot response
    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            with st.spinner("Pensando..."):
                response = get_gemini_reponse(prompt, docs_raw)
                placeholder = st.empty()
                placeholder.markdown(response)

                #print(response)

                # # Abrindo o arquivo no modo de escrita ("w")
                # with open("response.txt", "w") as arquivo:
                # # Escrevendo o texto no arquivo
                #     arquivo.write(response)


                # full_response = ''
                # for item in response['output_text']:
                #     full_response += item
                #     placeholder.markdown(full_response)
                # placeholder.markdown(full_response)

        if response is not None:
            message = {"role": "assistant", "content": response}
            st.session_state.messages.append(message)

if __name__ == "__main__":
    main()