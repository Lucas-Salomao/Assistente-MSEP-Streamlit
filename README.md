## Assistente Virtual MSEP - SENAI São Paulo

Este projeto desenvolve um assistente virtual para professores do SENAI São Paulo, que utiliza a metodologia MSEP (Metodologia Senai de Educação Profissional) para auxiliar na criação de documentos pedagógicos.

<p align="center">
  <img src="./diagram/home_screen.png" alt="Tela Inicial">
</p>

**Objetivo:**

O objetivo do projeto é oferecer aos professores do SENAI uma ferramenta inteligente que:

- **Auxilie na criação de planos de ensino, cronogramas e planos de aula:** O assistente utiliza a MSEP como base para gerar documentos eficientes e adequados à realidade do SENAI.
- **Integre informações da MSEP e de planos de curso:** O assistente pode analisar documentos como a MSEP e planos de curso para oferecer sugestões e gerar conteúdo personalizado.
- **Agilize o processo de elaboração de documentos:** A ferramenta automatiza tarefas repetitivas, liberando tempo para o professor se dedicar a outras atividades importantes.

**Funcionalidades:**

- **Upload de arquivos PDF:** O usuário pode carregar arquivos PDF da MSEP e planos de curso para que o assistente os analise.
- **Seleção de tipo de documento:** O usuário escolhe o tipo de documento que deseja gerar (Plano de Ensino, Cronograma, Plano de Aula).
- **Configuração de informações:** O usuário pode fornecer informações adicionais, como o nome do curso, unidade curricular e estratégias de aprendizagem.
- **Interação via chat:** O assistente interage com o usuário por meio de um chat intuitivo, respondendo perguntas e fornecendo sugestões.
- **Geração de texto:** O assistente utiliza modelos de linguagem avançados para gerar textos completos e personalizados de acordo com a MSEP e as informações fornecidas pelo usuário.

**Tecnologias:**

- **Streamlit:** Biblioteca Python para criar interfaces web interativas.
- **Google Generative AI:** Serviço de modelos de linguagem avançados do Google (Gemini 1.5 Flash).
- **PyPDF2:** Biblioteca Python para ler arquivos PDF.
- **PyMuPDF (fitz):** Biblioteca Python para trabalhar com documentos PDF.

**Como usar:**

1. **Instale as dependências:**
    
    ```bash
    pip install -r requirements.txt
    
    ```
    
2. **Configure a chave API do Google AI Studio:**
    - Acesse o Google AI Studio e crie um projeto.
    - Crie uma chave API para o seu projeto.
    - Insira a chave API no campo "Chave API Google AI Studio" na interface do aplicativo.
3. **Execute o aplicativo:**
    
    ```bash
    streamlit run app.py
    
    ```
    
4. **Carregue os arquivos PDF da MSEP e do plano de curso:**
    - Clique no botão "Carregue seus arquivos PDF".
    - Selecione os arquivos PDF desejados.
5. **Selecione o tipo de documento:**
    - Escolha o tipo de documento que deseja gerar (Plano de Ensino, Cronograma, Plano de Aula).
6. **Preencha as informações adicionais (opcional):**
    - Forneça informações como o nome do curso, unidade curricular e estratégias de aprendizagem.
7. **Clique no botão "Processar documentos":**
    - O assistente irá analisar os arquivos PDF e gerar o documento solicitado.
8. **Interaja com o assistente via chat:**
    - Faça perguntas e solicite sugestões para o assistente.

**Observações:**

- O aplicativo requer uma chave API do Google AI Studio para funcionar.
- O aplicativo é experimental e está em constante desenvolvimento.
- O aplicativo pode não ser compatível com todos os formatos de arquivos PDF.

**Contribuições:**

Contribuições para o projeto são bem-vindas! Abra um *issue* para reportar problemas ou sugestões, ou envie um *pull request* com suas melhorias.

**Créditos:**

Este projeto foi desenvolvido por [Lucas Salomao](mailto:lucastadeusalomao@gmail.com).

**Licença:**

Este projeto é licenciado sob a licença MIT.

**Obrigado por usar o Assistente Virtual MSEP!**
