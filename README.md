## Assistente MSEP - SENAI SP

Este é um aplicativo web que utiliza inteligência artificial para auxiliar professores do SENAI SP na elaboração de planos de ensino, cronogramas e planos de aula, seguindo as diretrizes da Metodologia SENAI de Educação Profissional (MSEP).

## Funcionalidades

- **Carregamento de Documentos:** Faça o upload do Plano de Curso e da MSEP em formato PDF.
- **Geração de Conteúdo:**
    - Gere automaticamente sugestões para planos de ensino, cronogramas e planos de aula.
    - Personalize o conteúdo gerado de acordo com o curso, unidade curricular e estratégias de aprendizagem.
- **Assistente Inteligente:**
    - Tire suas dúvidas sobre a MSEP e como aplicá-la em seus documentos.
    - Receba sugestões e orientações personalizadas.

## Como Usar

1. **Instalação:**
    - Clone o repositório: git clone https://github.com/seu-usuario/assistente-msep.git
    - Acesse o diretório: cd assistente-msep
    - Crie um ambiente virtual: python -m venv .venv
    - Ative o ambiente virtual:
        - Linux/macOS: source .venv/bin/activate
        - Windows: .venv\Scripts\activate
    - Instale as dependências: pip install -r requirements.txt
    - Configure a API Key do Google:
        - Crie um arquivo .env na raiz do projeto.
        - Adicione a seguinte linha ao arquivo .env, substituindo SUA_GOOGLE_API_KEY pela sua chave de API:
            
            `GOOGLE_API_KEY=SUA_GOOGLE_API_KEY`
            
            **content_copy**Use code [**with caution**](https://support.google.com/legal/answer/13505487).
            
2. **Execução:**
    - Execute o aplicativo: streamlit run app.py
    - Acesse o aplicativo em seu navegador no endereço indicado no terminal (geralmente [**http://localhost:8501**](http://localhost:8501/)).
3. **Utilização:**
    - **Carregue os arquivos PDF:**
        - Na barra lateral, faça o upload da MSEP e do Plano de Curso.
        - Clique em "Enviar & Processar".
    - **Gere um documento:**
        - Preencha os campos com o nome do curso, unidade curricular, tipo de documento e outras informações relevantes.
        - Selecione a estratégia de aprendizagem.
        - Clique em "Gerar [Tipo de Documento]".
    - **Utilize o assistente inteligente:**
        - Digite suas perguntas na caixa de texto.
        - O assistente fornecerá respostas e sugestões personalizadas.

## Tecnologias Utilizadas

- **Python:** Linguagem de programação principal.
- **Streamlit:** Framework para criação de aplicações web.
- **LangChain:** Framework para desenvolvimento de aplicações com Large Language Models (LLMs).
- **Google Generative AI:** Modelos de linguagem do Google para geração de texto e embeddings.
- **FAISS:** Biblioteca para pesquisa por similaridade.
- **PyPDF2:** Biblioteca para leitura de arquivos PDF.

## Próximos Passos

- Implementar a funcionalidade de geração de planos de ensino, cronogramas e planos de aula.
- Integrar com outras ferramentas e plataformas do SENAI SP.
- Melhorar a interface do usuário e a experiência de uso.

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e pull requests.

## Créditos:

Este projeto foi desenvolvido por [Lucas Salomao](lucastadeusalomao@gmail.com).

## Licença:

Este projeto é licenciado sob a licença MIT.