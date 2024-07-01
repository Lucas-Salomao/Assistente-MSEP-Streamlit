FROM python:3.9-slim

# Define a variável de ambiente para a porta
ENV PORT=8501

# Instala as dependências do projeto
COPY requirements.txt ./
RUN pip install -r requirements.txt

# Copia o código da aplicação para o container
COPY . .

# Define o comando para executar o aplicativo Streamlit
CMD ["streamlit", "run", "app.py", "--server.port", "$PORT"]