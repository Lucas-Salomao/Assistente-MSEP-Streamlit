import PyPDF2  # Importa a biblioteca PyPDF2 para ler arquivos PDF
import streamlit as st  # Importa a biblioteca Streamlit para criar a interface web
import google.generativeai as genai  # Importa a biblioteca do Google Generative AI para usar modelos de linguagem
import pymupdf  # Importa a biblioteca PyMuPDF (fitz) para ler arquivos PDF
import fitz  # Importa a biblioteca fitz para trabalhar com documentos PDF

LOGO_VERMELHO = 'https://upload.wikimedia.org/wikipedia/commons/8/8c/SENAI_S%C3%A3o_Paulo_logo.png'  # URL do logotipo vermelho do SENAI São Paulo
LOGO_AZUL = 'https://logodownload.org/wp-content/uploads/2019/08/senai-logo-1.png'  # URL do logotipo azul do SENAI São Paulo

generation_config = {
    "temperature": 1,  # Define a temperatura para a geração de texto (menor = mais previsível)
    "top_p": 0.95,  # Define a probabilidade de escolha das palavras (maior = mais palavras prováveis)
    "top_k": 64,  # Define o número de palavras candidatas para escolher (maior = mais opções)
    "max_output_tokens": 8192,  # Define o número máximo de tokens na saída
    "response_mime_type": "text/plain",  # Define o tipo de mídia da resposta
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",  # Define o modelo de linguagem a ser usado (Gemini 1.5 Flash)
    generation_config=generation_config,  # Define a configuração de geração de texto
    # safety_settings = Adjust safety settings  # Ajusta as configurações de segurança (opcional)
    # See https://ai.google.dev/gemini-api/docs/safety-settings  # Link para a documentação das configurações de segurança
    system_instruction="Você é um especialista em educação profissional, que trabalha no Senai São Paulo, que orienta os professores a como usar a metodologia senai de educação profissional para elaborar planos de ensino, cronogramas e planos de aula",  # Define a instrução do sistema para o modelo de linguagem
)

def ler_arquivo_txt(nome_do_arquivo):
    """
    Lê o conteúdo de um arquivo de texto.

    Args:
        nome_do_arquivo (str): O nome do arquivo de texto a ser lido.

    Returns:
        str: O conteúdo do arquivo de texto, ou None se o arquivo não for encontrado.
    """
    try:
        with open(nome_do_arquivo, 'r', encoding="utf-8") as arquivo:
            conteudo = arquivo.read()
            return conteudo
    except FileNotFoundError:
        print(f"Erro: Arquivo '{nome_do_arquivo}' não encontrado.")
        return None

def getTokens(prompt):
    """
    Conta o número de tokens em um prompt.

    Args:
        prompt (str): O prompt a ser contado.

    Returns:
        int: O número de tokens no prompt.
    """
    return model.count_tokens(prompt)

chat_session = model.start_chat(
    history=[
        # Histórico de mensagens (opcional)
    ]
)

def clear_chat_history():
    """
    Limpa o histórico de mensagens do chat.
    """
    st.session_state.messages = [
        {"role": "assistant", "content": "Faça o upload da MSEP e do Plano de Curso desejado"}]

def get_gemini_reponse(prompt,raw_text):
    """
    Obtém uma resposta do modelo Gemini.

    Args:
        prompt (str): O prompt a ser enviado para o modelo.
        raw_text (str): O texto bruto do arquivo PDF.

    Returns:
        str: A resposta do modelo Gemini.
    """
    contexto=raw_text
    response = chat_session.send_message(raw_text+prompt)
    return response.text

# read all pdf files and return text
def get_pdf_text(pdf_docs):
    """
    Lê o texto de todos os arquivos PDF fornecidos.

    Args:
        pdf_docs (list): Uma lista de arquivos PDF.

    Returns:
        str: O texto extraído de todos os arquivos PDF.
    """
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PyPDF2.PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def get_pdf_text_v2(pdf_docs):
    """
    Lê o texto de todos os arquivos PDF fornecidos usando PyMuPDF.

    Args:
        pdf_docs (list): Uma lista de arquivos PDF.

    Returns:
        str: O texto extraído de todos os arquivos PDF.
    """
    text = ""
    for pdf in pdf_docs:
        pdf_bytes = pdf.getvalue()
        # Open the PDF with PyMuPDF (fitz) using the bytes
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        for page in doc:
            text += page.get_text()
    return text

def main():
    """
    A função principal da aplicação.
    """
    if 'docs_raw' not in st.session_state:
        st.session_state.docs_raw = ''

    st.logo(LOGO_AZUL, link=None, icon_image=None)  # Exibe o logotipo azul do SENAI

    st.set_page_config(
        page_title="Assistente Virtual MSEP - Metodologia Senai de Educação Profissional",  # Define o título da página
        page_icon="🤖",  # Define o ícone da página
        menu_items={'Get Help': 'https://www.extremelycoolapp.com/help',  # Define os itens do menu
                   'Report a bug': "mailto:lucas.salomao@gmail.com",
                   'About': "SENAI São Paulo - Gerência de Educação\n\nSupervisão de Tecnologias Educacionais - Guilherme Dias\n\nCriado por Lucas Salomão"}
    )

    # Sidebar for uploading PDF files
    st.image(LOGO_AZUL, width=200)  # Exibe o logotipo azul na sidebar
    with st.sidebar:
        st.title("Menu:")
        apiKeyGoogleAiStudio = st.text_input("Chave API Google AI Studio:", "", type='password')  # Campo de entrada para a chave API
        nomeCurso = st.text_input("Nome do Curso:", "")  # Campo de entrada para o nome do curso
        nomeUC = st.text_input("Nome da Unidade Curricular:", "")  # Campo de entrada para o nome da unidade curricular
        tipoDocumento = st.selectbox("Selecione o tipo de documento", ("Plano de Ensino", "Cronograma", "Plano de Aula"))  # Menu dropdown para selecionar o tipo de documento
        if(tipoDocumento=='Plano de Ensino'):
            qntSituacoesAprendizagem = st.number_input("Quantidade de estratégias de aprendizagem:", min_value=1)  # Campo de entrada numérico para a quantidade de estratégias de aprendizagem
            estrategiaAprendizagem = st.selectbox("Selecione a estratégia de aprendizagem", ("Situação-Problema", "Estudo de Caso", "Projeto Integrador", "Projetos","Pesquisa Aplicada"))  # Menu dropdown para selecionar a estratégia de aprendizagem
        pdf_docs = st.file_uploader("Carregue seus arquivos PDF e clique no botão Enviar e Processar", type='.pdf', accept_multiple_files=True, help='Faça o upload da MSEP e de um plano de curso que deseja elaborar os documentos de prática docente.')  # Carregador de arquivos PDF
        if st.button("Processar documentos"):
            with st.spinner("Processando..."):
                st.session_state.docs_raw = get_pdf_text(pdf_docs)  # Lê o texto dos arquivos PDF e armazena na sessão

                # Abrindo o arquivo no modo de escrita ("w")
                with open("meu_arquivo.txt", "w", encoding="utf-8") as arquivo:
                    # Escrevendo o texto no arquivo
                    arquivo.write(st.session_state.docs_raw)

                st.success("Concluído")  # Exibe uma mensagem de sucesso

    # Main content area for displaying chat messages
    st.title("Assistente Virtual MSEP - Metodologia Senai de Educação Profissional")  # Título da página
    st.write("Bem vindo ao assistente virtual do professor para auxiliar a elaboração de documentos da prática pedagógica de acordo com a MSEP!")  # Mensagem de boas-vindas
    st.sidebar.button('Limpar histórico do chat', on_click=clear_chat_history)  # Botão para limpar o histórico do chat

    # Chat input
    # Placeholder for chat messages
    if "messages" not in st.session_state.keys():
        st.session_state.messages = [{"role": "assistant", "content": "Carregue um plano de curso e elabore o documento desejado de acordo com a MSEP."}]  # Mensagem inicial do assistente

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])  # Exibe as mensagens do chat

    st.session_state.text_btn="Gerar "+tipoDocumento  # Define o texto do botão
    if st.button(st.session_state.text_btn):
        if (st.session_state.text_btn=="Gerar Plano de Ensino"):
            print("Gerando Plano de Ensino")
            # prompt=ler_arquivo_txt('prompt-plano-ensino.txt')
            prompt="Elabore um plano de ensino conforme a MSEP da unidade curricular de Banco de Dados"
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.write("Gerar Plano de Ensino")

    # Display chat messages and bot response
    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            with st.spinner("Pensando..."):
                response = get_gemini_reponse(prompt, st.session_state.docs_raw)  # Obtém a resposta do modelo Gemini
                placeholder = st.empty()  # Cria um placeholder para a resposta
                placeholder.markdown(response)  # Exibe a resposta no placeholder

                # Abrindo o arquivo no modo de escrita ("w")
                with open("response.txt", "w", encoding="utf-8") as arquivo:
                    # Escrevendo o texto no arquivo
                    arquivo.write(response)

        if response is not None:
            message = {"role": "assistant", "content": response}
            st.session_state.messages.append(message)  # Adiciona a resposta ao histórico de mensagens

if __name__ == "__main__":
    main()