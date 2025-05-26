# Gerador de Atividades para Crianças Autistas

Este projeto gera programações semanais de atividades para crianças autistas, com foco no desenvolvimento de habilidades específicas, usando a API da Hugging Face.

## Estrutura
- `static/`: Arquivos estáticos (CSS, JS).
- `templates/`: Arquivos HTML (index.html, result.html).
- `app.py`: Servidor Flask que serve o front-end e a API.
- `requirements.txt`: Dependências do projeto.

## Como Executar Localmente
1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/gerador_atividades.git
   ```
2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
3. Defina a variável de ambiente `HF_API_KEY` com sua chave da Hugging Face.
4. Execute a aplicação:
   ```bash
   python app.py
   ```
5. Acesse em `http://localhost:5000`.

## Hospedagem
A aplicação está hospedada no Render. Acesse em: [INSIRA O LINK DO RENDER AQUI]

## Configuração no Render
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn app:app`
- **Environment Variable**: `HF_API_KEY` com sua chave da Hugging Face.