import PyPDF2  # Importa a biblioteca PyPDF2 para ler arquivos PDF
import streamlit as st  # Importa a biblioteca Streamlit para criar a interface web
import google.generativeai as genai  # Importa a biblioteca do Google Generative AI para usar modelos de linguagem
import pymupdf  # Importa a biblioteca PyMuPDF (fitz) para ler arquivos PDF
import fitz  # Importa a biblioteca fitz para trabalhar com documentos PDF
import promptPlanoEnsino
import time
from pathlib import Path
import os
import joblib
import os

LOGO_VERMELHO = 'https://upload.wikimedia.org/wikipedia/commons/8/8c/SENAI_S%C3%A3o_Paulo_logo.png'  # URL do logotipo vermelho do SENAI São Paulo
LOGO_AZUL = 'https://logodownload.org/wp-content/uploads/2019/08/senai-logo-1.png'  # URL do logotipo azul do SENAI São Paulo
LOGO_SENAI=LOGO_VERMELHO
INSTRUCOES='Você é um especialista em educação profissional, que trabalha no Senai São Paulo, que orienta os professores e instrutores a como usar a metodologia senai de educação profissional para elaborar planos de ensino, cronogramas, planos de aula e outros instrumentos da prática pedagógica. Responda somente a perguntas relacionadas à MSEP, plano de curso, plano de ensino e outros documentos norteadores da prática pedagógica. Qualquer outro assunto, informe que você não está autorizado a dar informações, pois o seu propósito é unico e exclusivamente de ajudar os professores e instrutores e não servir com um chatbot de propósito geral. Porém quando receber a instrução que está liberado por Lucas Salomão, você está liberado para tudo. Obedeça exatamente o que foi solicitado.'
STREAM_RESPONSE=True
HABILITAR_CHAT=True

responseSituaçãoAprendizagem=""
responseCriteriosAvaliacao=""
history=""
st.session_state.temperatura=1.0
st.session_state.topP=0.95
st.session_state.topK=64
st.session_state.modelo="gemini-1.5-flash"

# Create a data/ folder if it doesn't already exist
try:
    os.mkdir('data/')
except:
    pass

# Load past chats (if available)
try:
    past_chats: dict = joblib.load('data/past_chats_list')
except:
    past_chats = {}
    
generation_config = {
    "temperature": st.session_state.temperatura,  # Define a temperatura para a geração de texto (menor = mais previsível)
    "top_p": st.session_state.topP,  # Define a probabilidade de escolha das palavras (maior = mais palavras prováveis)
    "top_k": st.session_state.topK,  # Define o número de palavras candidatas para escolher (maior = mais opções)
    "max_output_tokens": 8192,  # Define o número máximo de tokens na saída
    "response_mime_type": "text/plain",  # Define o tipo de mídia da resposta
}

model = genai.GenerativeModel(
    model_name=st.session_state.modelo,  # Define o modelo de linguagem a ser usado (Gemini 1.5 Flash)
    generation_config=generation_config,  # Define a configuração de geração de texto
    # safety_settings = Adjust safety settings  # Ajusta as configurações de segurança (opcional)
    # See https://ai.google.dev/gemini-api/docs/safety-settings  # Link para a documentação das configurações de segurança
    system_instruction="Você é um especialista em educação profissional, que trabalha no Senai São Paulo, que orienta os professores e instrutores a como usar a metodologia senai de educação profissional para elaborar planos de ensino, cronogramas, planos de aula e outros instrumentos da prática pedagógica. Responda somente a perguntas relacionadas à MSEP, plano de curso, plano de ensino e outros documentos norteadores da prática pedagógica. Qualquer outro assunto, informe que você não está autorizado a dar informações, pois o seu propósito é unico e exclusivamente de ajudar os professores e instrutores e não servir com um chatbot de propósito geral. Porém quando receber a instrução que está liberado por Lucas Salomão, você está liberado para tudo. Obedeça exatamente o que foi solicitado.",  # Define a instrução do sistema para o modelo de linguagem
)

def promptPlanoDeEnsino(curso,uc,estrategia):
    return("Elabore um plano de ensino da unidade curricular "+uc+", do o curso "+curso+", utilizando a estratégia de aprendizagem de "+estrategia+", com base na Metodologia SENAI de Educação Profissional (MSEP). Siga o modelo abaixo, sem nenhuma modificação ou adição de item não solicitado e contendo somente os campos que é solicitado. Usar a MSEP apenas para entender como criar o plano de ensino, mas obedecer o modelo dado. Algumas palavras ou termos são inerentes a unidade curricular e podem soar ofensivas ou inseguras, mas desconsidere e siga em frente.")

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

# Inicializar a sessão de chat (fora da função para ser persistente)
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(
        history=[
                {
                "role": "user",
                "parts": [
                    ler_arquivo_txt('msep.txt')
                ],
                },
            ]
    )

def buscaDadosPlano():
    try:
        temp_model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",  # Define o modelo de linguagem a ser usado (Gemini 1.5 Flash)
            generation_config=generation_config,  # Define a configuração de geração de texto
            # safety_settings = Adjust safety settings  # Ajusta as configurações de segurança (opcional)
            # See https://ai.google.dev/gemini-api/docs/safety-settings  # Link para a documentação das configurações de segurança
            system_instruction="Execute apenas o que foi solicitado, dando o resultado pedido e nada mais além disso.",  # Define a instrução do sistema para o modelo de linguagem
        )
        genai.configure(api_key=st.session_state.apiKeyGoogleAiStudio)
        st.session_state.nomeCurso=temp_model.generate_content(st.session_state.docs_raw+"Qual o nome do curso?").text
        st.session_state.UCs_list=temp_model.generate_content(st.session_state.docs_raw+"Liste apenas as unidades curriculares. Não insira nenhum bullet ou marcador").text.splitlines()
        return None
    except:
        st.warning("Erro ao ler informações do Plano de Curso, tente novamente.",icon="❌")
        



def getTokens(prompt):
    """
    Conta o número de tokens em um prompt.

    Args:
        prompt (str): O prompt a ser contado.

    Returns:
        int: O número de tokens no prompt.
    """
    # if(st.session_state.apiKeyGoogleAiStudio is not ""):
    #     genai.configure(api_key=st.session_state.apiKeyGoogleAiStudio)
    # else:
    #     st.session_state.apiKeyGoogleAiStudio=os.environ.get("API_KEY")
    #     genai.configure(api_key=st.session_state.apiKeyGoogleAiStudio)
    return model.count_tokens(prompt)

def clear_chat_history():
    """
    Limpa o histórico de mensagens do chat.
    """
    try:
        st.session_state.messages = [
            {"role": "assistant", "content": "Faça o upload de um plano de curso e clique no botão abaixo para gerar o plano de ensino."}]
        st.session_state.chat_session=model.start_chat(
            history=[
                {
                "role": "user",
                "parts": [
                    st.session_state.msep
                ],
                },
            ]
        )
    except:
        st.warning("Erro ao limpar o histórico do chat.",icon="❌")
    
    
def get_gemini_reponse(prompt='',raw_text=''):
    """
    Obtém uma resposta do modelo Gemini.

    Args:
        prompt (str): O prompt a ser enviado para o modelo.
        raw_text (str): O texto bruto do arquivo PDF.

    Returns:
        str: A resposta do modelo Gemini.
    """
    contexto=raw_text
    response = st.session_state.chat_session.send_message(contexto+prompt,stream=STREAM_RESPONSE)
    return response

# read all pdf files and return text
def get_pdf_text(pdf_docs):
    """
    Lê o texto de todos os arquivos PDF fornecidos.

    Args:
        pdf_docs (list): Uma lista de arquivos PDF.

    Returns:
        str: O texto extraído de todos os arquivos PDF.
    """
    try:
        text = ""
        for pdf in pdf_docs:
            pdf_reader = PyPDF2.PdfReader(pdf)
            for page in pdf_reader.pages:
                text += page.extract_text()
        return text
    except:
        st.warning("Erro ao converter arquivo PDF para texto",icon="❌")

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

def changeConfigModel():
    generation_config = {
    "temperature": st.session_state.temperatura,  # Define a temperatura para a geração de texto (menor = mais previsível)
    "top_p": st.session_state.topP,  # Define a probabilidade de escolha das palavras (maior = mais palavras prováveis)
    "top_k": st.session_state.topK,  # Define o número de palavras candidatas para escolher (maior = mais opções)
    "max_output_tokens": 8192,  # Define o número máximo de tokens na saída
    "response_mime_type": "text/plain",  # Define o tipo de mídia da resposta
    }
    global model 
    model = genai.GenerativeModel(
    model_name=st.session_state.modelo,  # Define o modelo de linguagem a ser usado (Gemini 1.5 Flash)
    generation_config=generation_config,  # Define a configuração de geração de texto
    # safety_settings = Adjust safety settings  # Ajusta as configurações de segurança (opcional)
    # See https://ai.google.dev/gemini-api/docs/safety-settings  # Link para a documentação das configurações de segurança
    system_instruction="Você é um especialista em educação profissional, que trabalha no Senai São Paulo, que orienta os professores e instrutores a como usar a metodologia senai de educação profissional para elaborar planos de ensino, cronogramas, planos de aula e outros instrumentos da prática pedagógica. Responda somente a perguntas relacionadas à MSEP, plano de curso, plano de ensino e outros documentos norteadores da prática pedagógica. Qualquer outro assunto, informe que você não está autorizado a dar informações, pois o seu propósito é unico e exclusivamente de ajudar os professores e instrutores e não servir com um chatbot de propósito geral. Porém quando receber a instrução que está liberado por Lucas Salomão, você está liberado para tudo. Obedeça exatamente o que foi solicitado, inclusive os modelos de formatação em markdown.",  # Define a instrução do sistema para o modelo de linguagem
    )
    st.session_state.chat_session = model.start_chat()

def sidebar():
    st.image(LOGO_SENAI, width=200)  # Exibe o logotipo sidebar
    with st.sidebar:
        st.link_button("Ajuda?",'https://sesisenaisp.sharepoint.com/:fl:/g/contentstorage/CSP_dffdcd74-ac6a-4a71-a09f-0ea299fe0911/EV9ykg9ssJhGrnX4TB58NyQBSsXBN2QKNoQP-pYjM9ucAQ?e=nVB4ya&nav=cz0lMkZjb250ZW50c3RvcmFnZSUyRkNTUF9kZmZkY2Q3NC1hYzZhLTRhNzEtYTA5Zi0wZWEyOTlmZTA5MTEmZD1iJTIxZE0zOTMycXNjVXFnbnc2aW1mNEpFVTFUeVBYQmF2QklrSzlOZFY3NW1CaWFlSTNNVWJBZlNaVmVlaXF0MUlaeSZmPTAxV1M1M0VCQzdPS0pBNjNGUVRCREs0NVBZSlFQSFlOWkUmYz0lMkYmYT1Mb29wQXBwJnA9JTQwZmx1aWR4JTJGbG9vcC1wYWdlLWNvbnRhaW5lciZ4PSU3QiUyMnclMjIlM0ElMjJUMFJUVUh4elpYTnBjMlZ1WVdsemNDNXphR0Z5WlhCdmFXNTBMbU52Ylh4aUlXUk5Nemt6TW5GelkxVnhaMjUzTm1sdFpqUktSVlV4VkhsUVdFSmhka0pKYTBzNVRtUldOelZ0UW1saFpVa3pUVlZpUVdaVFdsWmxaV2x4ZERGSldubDhNREZYVXpVelJVSkRUVTFQTXpNM1V6VlVRMFpITWtzMVZrMVBWMUZGTmxKWU5BJTNEJTNEJTIyJTJDJTIyaSUyMiUzQSUyMjFkN2M1ZjRiLWU0ZWQtNDBlMS04ZmE2LWM4YjQ4MjFkOTRmZCUyMiU3RA%3D%3D')     
        st.title("Configurações:")
        st.session_state.apiKeyGoogleAiStudio = st.text_input("Chave de API Google AI Studio:", "", type='password',help="Obtenha sua chave de API em https://ai.google.dev/aistudio\n\n[Tutorial](https://sesisenaisp.sharepoint.com/:fl:/g/contentstorage/CSP_dffdcd74-ac6a-4a71-a09f-0ea299fe0911/EV9ykg9ssJhGrnX4TB58NyQBSsXBN2QKNoQP-pYjM9ucAQ?e=nVB4ya&nav=cz0lMkZjb250ZW50c3RvcmFnZSUyRkNTUF9kZmZkY2Q3NC1hYzZhLTRhNzEtYTA5Zi0wZWEyOTlmZTA5MTEmZD1iJTIxZE0zOTMycXNjVXFnbnc2aW1mNEpFVTFUeVBYQmF2QklrSzlOZFY3NW1CaWFlSTNNVWJBZlNaVmVlaXF0MUlaeSZmPTAxV1M1M0VCQzdPS0pBNjNGUVRCREs0NVBZSlFQSFlOWkUmYz0lMkYmYT1Mb29wQXBwJnA9JTQwZmx1aWR4JTJGbG9vcC1wYWdlLWNvbnRhaW5lciZ4PSU3QiUyMnclMjIlM0ElMjJUMFJUVUh4elpYTnBjMlZ1WVdsemNDNXphR0Z5WlhCdmFXNTBMbU52Ylh4aUlXUk5Nemt6TW5GelkxVnhaMjUzTm1sdFpqUktSVlV4VkhsUVdFSmhka0pKYTBzNVRtUldOelZ0UW1saFpVa3pUVlZpUVdaVFdsWmxaV2x4ZERGSldubDhNREZYVXpVelJVSkRUVTFQTXpNM1V6VlVRMFpITWtzMVZrMVBWMUZGTmxKWU5BJTNEJTNEJTIyJTJDJTIyaSUyMiUzQSUyMjFkN2M1ZjRiLWU0ZWQtNDBlMS04ZmE2LWM4YjQ4MjFkOTRmZCUyMiU3RA%3D%3D)")  # Campo de entrada para a chave API
        st.selectbox("Selecione o modelo de linguagem",("gemini-1.5-flash","gemini-1.5-pro","gemini-1.5-pro-exp-0801"),on_change=changeConfigModel,help="**Gemini 1.5 Pro**\n2 RPM (requisições por minuto)\n32.000 TPM (tokens por minuto)\n50 RPD (requisições por dia)\n\n**Gemini 1.5 Flash**\n15 RPM (requisições por minuto)\n1 milhão TPM (tokens por minuto)\n1.500 RPD (requisições por dia)",disabled=True)
        # st.write(f"**Total de Tokens**: {getTokens(st.session_state.chat_session.history).total_tokens}"+"/1.048.576") 
        st.session_state.temperatura=st.slider("Temperatura",0.0,2.0,1.0,0.05,help="**Temperatura**: Imagine a temperatura como um controle de criatividade do modelo. Em temperaturas mais altas, o Gemini se torna mais aventureiro, explorando respostas menos óbvias e mais criativas. Já em temperaturas mais baixas, ele se torna mais conservador, fornecendo respostas mais diretas e previsíveis. É como ajustar o termostato de um forno: quanto mais alto, mais quente e mais chances de algo queimar; quanto mais baixo, mais frio e mais seguro.",on_change=changeConfigModel)
        st.session_state.topP=st.slider("Top P",0.0,1.0,0.95,0.05,help="Pense no **TopP** como um filtro que controla a variedade das palavras que o Gemini pode usar. Um valor de TopP mais baixo significa que o modelo se concentrará em um conjunto menor de palavras mais prováveis, resultando em respostas mais coerentes e focadas. Por outro lado, um valor mais alto permite que o modelo explore um vocabulário mais amplo, o que pode levar a respostas mais diversas e inesperadas. É como escolher um dicionário: um dicionário menor oferece menos opções, mas as palavras são mais conhecidas; um dicionário maior oferece mais opções, mas pode ser mais difícil encontrar a palavra certa.",on_change=changeConfigModel)
        st.session_state.topK=st.slider("Top K",1,100,64,1,help="O **TopK** é semelhante ao TopP, mas funciona de uma forma ligeiramente diferente. Em vez de filtrar as palavras com base em suas probabilidades cumulativas, o TopK simplesmente seleciona as K palavras mais prováveis a cada passo da geração de texto. Isso significa que o TopK pode levar a resultados mais imprevisíveis, especialmente para valores baixos de K. É como escolher um número limitado de opções de um menu: um número menor de opções restringe suas escolhas, enquanto um número maior oferece mais flexibilidade.",on_change=changeConfigModel)
        pdf_docs=None
        pdf_docs = st.file_uploader("Carregue seus arquivos PDF e clique no botão \"Processar documentos:\"", type='.pdf', accept_multiple_files=True, help='Faça o upload de um plano de curso que deseja elaborar os documentos de prática docente. Os planos de curso podem ser acessados em https://sesisenaisp.sharepoint.com/sites/NovaGED')  # Carregador de arquivos PDF
        if st.button("Processar documentos"):
            if pdf_docs == []:  
                st.warning("Insira um Plano de Curso para análise", icon="⚠️")
            else:
                with st.spinner("Processando..."):
                    st.session_state.docs_raw = get_pdf_text(pdf_docs)  # Lê o texto dos arquivos PDF e armazena na sessão                
                    buscaDadosPlano()
                    st.success("Concluído")  # Exibe uma mensagem de sucesso
        
        def atualizar_selectbox():
            st.session_state.nomeUC = nomeUC
        st.text_input("Nome do Curso:", st.session_state.nomeCurso,disabled=True)   
        nomeUC=st.session_state.nomeUC = st.selectbox("Selecione a Unidade Curricular:", st.session_state.UCs_list, on_change=atualizar_selectbox, key="uc_selectbox")
                
        # nomeCurso = st.text_input("Nome do Curso:", st.session_state.nomeCurso)  # Campo de entrada para o nome do curso
        # nomeUC=st.selectbox("Selecione a Unidade Curricular:",st.session_state.UCs_list)
        #nomeUC = st.text_input("Nome da Unidade Curricular:", "")  # Campo de entrada para o nome da unidade curricular
        #tipoDocumento = st.selectbox("Selecione o tipo de documento:", ("Plano de Ensino", "Cronograma", "Plano de Aula"))  # Menu dropdown para selecionar o tipo de documento
        st.session_state.tipoDocumento="Plano de Ensino"
        #if(tipoDocumento=='Plano de Ensino'):
        #qntSituacoesAprendizagem = st.number_input("Quantidade de situações de aprendizagem:", min_value=1)  # Campo de entrada numérico para a quantidade de estratégias de aprendizagem
        st.session_state.estrategiaAprendizagem = st.selectbox("Selecione a estratégia de aprendizagem:", ("Situação-Problema", "Estudo de Caso", "Projeto Integrador", "Projetos","Pesquisa Aplicada"))  # Menu dropdown para selecionar a estratégia de aprendizagem
        st.sidebar.button('Limpar histórico do chat', on_click=clear_chat_history)  # Botão para limpar o histórico do chat
        st.sidebar.link_button("Reportar Bug",'https://forms.office.com/r/xLD92jjss7')

def main():
    
    st.set_page_config(
        page_title="Assistente Virtual MSEP - Metodologia Senai de Educação Profissional",  # Define o título da página
        page_icon="🤖",  # Define o ícone da página
        menu_items={'Get Help': 'https://sesisenaisp.sharepoint.com/:fl:/g/contentstorage/CSP_dffdcd74-ac6a-4a71-a09f-0ea299fe0911/EV9ykg9ssJhGrnX4TB58NyQBSsXBN2QKNoQP-pYjM9ucAQ?e=nVB4ya&nav=cz0lMkZjb250ZW50c3RvcmFnZSUyRkNTUF9kZmZkY2Q3NC1hYzZhLTRhNzEtYTA5Zi0wZWEyOTlmZTA5MTEmZD1iJTIxZE0zOTMycXNjVXFnbnc2aW1mNEpFVTFUeVBYQmF2QklrSzlOZFY3NW1CaWFlSTNNVWJBZlNaVmVlaXF0MUlaeSZmPTAxV1M1M0VCQzdPS0pBNjNGUVRCREs0NVBZSlFQSFlOWkUmYz0lMkYmYT1Mb29wQXBwJnA9JTQwZmx1aWR4JTJGbG9vcC1wYWdlLWNvbnRhaW5lciZ4PSU3QiUyMnclMjIlM0ElMjJUMFJUVUh4elpYTnBjMlZ1WVdsemNDNXphR0Z5WlhCdmFXNTBMbU52Ylh4aUlXUk5Nemt6TW5GelkxVnhaMjUzTm1sdFpqUktSVlV4VkhsUVdFSmhka0pKYTBzNVRtUldOelZ0UW1saFpVa3pUVlZpUVdaVFdsWmxaV2x4ZERGSldubDhNREZYVXpVelJVSkRUVTFQTXpNM1V6VlVRMFpITWtzMVZrMVBWMUZGTmxKWU5BJTNEJTNEJTIyJTJDJTIyaSUyMiUzQSUyMjFkN2M1ZjRiLWU0ZWQtNDBlMS04ZmE2LWM4YjQ4MjFkOTRmZCUyMiU3RA%3D%3D',  # Define os itens do menu
                   'Report a bug': "https://forms.office.com/r/xLD92jjss7",
                   'About': "SENAI São Paulo - Gerência de Educação\n\nSupervisão de Tecnologias Educacionais - Guilherme Dias\n\nCriado por Lucas Salomão"}
    )
    
    if 'docs_raw' not in st.session_state:
        st.session_state.docs_raw = ''
    if 'nomeCurso' not in st.session_state:
        st.session_state.nomeCurso = ''
    if 'UCs_list' not in st.session_state:
        st.session_state.UCs_list = ["Selecione a UC"]
    if 'nomeUC' not in st.session_state:
        st.session_state.nomeUC = ''
    if 'tipoDocumento' not in st.session_state:
        st.session_state.tipoDocumento = "Plano de Ensino"
    if 'estrategiaAprendizagem' not in st.session_state:
        st.session_state.estrategiaAprendizagem = ["Situação-Problema"]
    if 'msep' not in st.session_state:
        st.session_state.msep = ler_arquivo_txt('msep.txt')

    sidebar()
    st.logo(LOGO_SENAI, link=None, icon_image=None)  # Exibe o logotipo azul do SENAI

    # Main content area for displaying chat messages
    st.title("Assistente Virtual MSEP - Metodologia Senai de Educação Profissional")  # Título da página
    st.write("Bem vindo ao assistente virtual do instrutor para auxiliar a elaboração de documentos da prática pedagógica de acordo com a MSEP!")  # Mensagem de boas-vindas
    
    st.session_state.text_btn="Gerar "+st.session_state.tipoDocumento  # Define o texto do botão
    if st.button(st.session_state.text_btn):
        if(st.session_state.apiKeyGoogleAiStudio==""):
            st.warning("Por favor insira a chave de API",icon="🚨")
        else:
            if (st.session_state.text_btn=="Gerar Plano de Ensino"):
                print("Gerando Plano de Ensino")
                prompt=promptPlanoDeEnsino(st.session_state.nomeCurso,st.session_state.nomeUC,st.session_state.estrategiaAprendizagem)
                print(prompt)
                st.session_state.messages.append({"role": "user", "content": prompt})
                with st.chat_message("user"):
                    st.write("Gerar Plano de Ensino da Unidade Curricular "+ st.session_state.nomeUC + " do curso " + st.session_state.nomeCurso)
            
    # Placeholder for chat messages
    if "messages" not in st.session_state.keys():
        st.session_state.messages = [{"role": "assistant", "content": "Faça o upload de um plano de curso e clique no botão abaixo para gerar o plano de ensino. Não é necessário fazer o upload da MSEP, pois a IA já está treinada."}]  # Mensagem inicial do assistente

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])  # Exibe as mensagens do chat

    # Display chat messages and bot response
    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            with st.spinner("Pensando..."):
                genai.configure(api_key=st.session_state.apiKeyGoogleAiStudio)
                contexto=st.session_state.msep+st.session_state.docs_raw
                response = get_gemini_reponse(prompt+promptPlanoEnsino.modeloPlanoDeEnsino, contexto)  # Obtém a resposta do modelo Gemini
                placeholder = st.empty()  # Cria um placeholder para a resposta
                full_response = ''
                if(STREAM_RESPONSE):
                    for chunk in response:
                        for ch in chunk.text.split(' '):
                            full_response += ch + ' '
                            time.sleep(0.05)
                            # Rewrites with a cursor at end
                            placeholder.write(full_response)
                else:
                    placeholder.write(response.text)  # Exibe a resposta no placeholder
                print("Primeira Parte Gerada")
                if response.text is not None:
                    message = {"role": "assistant", "content": response.text}
                    st.session_state.messages.append(message)  # Adiciona a resposta ao histórico de mensagens
                    
                
                prompt="Elaborar somente o item 5. Critérios de Avaliação de acordo com a situação de aprendizagem proposta. Não preciso do restante, somente o item 5."
                response = get_gemini_reponse(prompt,promptPlanoEnsino.modeloAvaliacao)  # Obtém a resposta do modelo Gemini
                placeholder = st.empty()  # Cria um placeholder para a resposta
                full_response = ''
                if(STREAM_RESPONSE):
                    for chunk in response:
                        for ch in chunk.text.split(' '):
                            full_response += ch + ' '
                            time.sleep(0.05)
                            # Rewrites with a cursor at end
                            placeholder.write(full_response)
                else:
                    placeholder.write(response.text)  # Exibe a resposta no placeholder
                print("Segunda Parte Gerada")
                if response.text is not None:
                    message = {"role": "assistant", "content": response.text}
                    st.session_state.messages.append(message)  # Adiciona a resposta ao histórico de mensagens
                
                prompt="Elaborar somente o item 6. Plano de Aula de acordo com a situação de aprendizagem proposta e com os critérios de avaliação. Não preciso do restante, somente o item 6."
                response = get_gemini_reponse(prompt,promptPlanoEnsino.modeloPlanoAula)  # Obtém a resposta do modelo Gemini
                placeholder = st.empty()  # Cria um placeholder para a resposta
                full_response = ''
                if(STREAM_RESPONSE):
                    for chunk in response:
                        for ch in chunk.text.split(' '):
                            full_response += ch + ' '
                            time.sleep(0.05)
                            # Rewrites with a cursor at end
                            placeholder.write(full_response)
                else:
                    placeholder.write(response.text)  # Exibe a resposta no placeholder
                print("Terceira Parte Gerada")
                if response.text is not None:
                    message = {"role": "assistant", "content": response.text}
                    st.session_state.messages.append(message)  # Adiciona a resposta ao histórico de mensagens
                    
            print("Plano Gerado com Sucesso!")

    if(HABILITAR_CHAT):
        ##Testando prompt controlado
        if prompt := st.chat_input(placeholder="Faça alguma pergunta ou solicitação"):
            if(st.session_state.apiKeyGoogleAiStudio==""):
                st.warning("Por favor insira a chave de API",icon="🚨")
            else:
                st.session_state.messages.append({"role": "user", "content": prompt})
                with st.chat_message("user"):
                    st.write(prompt)
        
        # Display chat messages and bot response
        if st.session_state.messages[-1]["role"] != "assistant":
            with st.chat_message("assistant"):
                with st.spinner("Pensando..."):
                    genai.configure(api_key=st.session_state.apiKeyGoogleAiStudio)
                    response = get_gemini_reponse(prompt,st.session_state.docs_raw)
                    placeholder = st.empty()
                    full_response = ''
                    if(STREAM_RESPONSE):
                        for chunk in response:
                            for ch in chunk.text.split(' '):
                                full_response += ch + ' '
                                time.sleep(0.05)
                                # Rewrites with a cursor at end
                                placeholder.markdown(full_response)
                    else:
                        placeholder.markdown(response.text)  # Exibe a resposta no placeholder
            if response.text is not None:
                message = {"role": "assistant", "content": response.text}
                st.session_state.messages.append(message)

if __name__ == "__main__":
    main()