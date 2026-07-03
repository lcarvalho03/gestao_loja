🚀 Gestão Loja - Referência em Arquitetura Django & PostgreSQL

Este projeto é uma aplicação web de alta performance desenvolvida com o framework Django e o banco de dados relacional PostgreSQL, utilizando a interface administrativa moderna AdminLTE 4 (baseada em Bootstrap 5).

Mais do que um sistema funcional para controle de loja, o projeto foi concebido para servir como um guia de referência prático em desenvolvimento backend, demonstrando como estruturar aplicações MVC/MVT que sejam escaláveis, seguras e de fácil manutenção.

🎯 Objetivos do Projeto & Engenharia de Software

O foco primordial deste repositório é aplicar e demonstrar as melhores práticas de desenvolvimento adotadas no mercado:

Isolamento de Configurações (.env): Gerenciamento seguro de credenciais do banco de dados e chaves criptográficas (SECRET_KEY), garantindo que informações confidenciais fiquem de fora do histórico do Git.

Separação de Responsabilidades: Divisão modular entre as regras de negócio em Apps específicas (loja e core), templates customizados e configurações gerais.

Manutenibilidade e Clean Code: Código limpo, seguindo rigorosamente as diretrizes de estilo da PEP 8, com nomenclatura autoexplicativa de variáveis, classes e funções.

Tratamento Seguro de Assets: Arquitetura otimizada para o carregamento de arquivos estáticos (CSS, JS, Imagens) preparada para deploys em nuvem através do collectstatic.

🛠️ Tecnologias e Componentes Utilizados

Backend: Python (v3.14+) & Django Framework (v6.0+)

Banco de Dados: PostgreSQL (Persistência e integridade referencial)

Interface Visual: AdminLTE 4 (Bootstrap 5) integrado nativamente por meio de componentes modulares do Django

Validações e Auxiliares:

django-localflavor: Para validação automatizada de documentos brasileiros (CPF, CNPJ, Estados)

django-phonenumber-field: Manipulação, máscara e validação de números de telefone padrão nacional e internacional

Gerenciamento de Ambiente: python-dotenv para leitura dinâmica de variáveis no sistema operacional

📂 Estrutura do Projeto

A arquitetura de arquivos foi planejada de maneira limpa e legível para qualquer desenvolvedor que analise o repositório:

```text
📁 gestao_loja/
├── 📁 core/                 # Configurações globais do Django (settings, urls)
├── 📁 loja/                 # Regras de negócio, models e views do app principal
├── 📁 static/               # Arquivos estáticos globais de desenvolvimento (CSS/JS locais)
├── 📁 staticfiles/          # Pasta gerada automaticamente em produção pelo collectstatic
├── 📁 templates/            # Telas HTML do sistema integradas e estendidas do AdminLTE 4
├── 📄 .env.example          # Modelo das variáveis de ambiente necessárias (sem valores reais)
├── 📄 .gitignore            # Filtro de arquivos protegidos (ignora .env, .venv, etc.)
├── 📄 manage.py             # CLI utilitário de gerenciamento do Django
└── 📄 requirements.txt      # Lista de dependências e pacotes do projeto


🚀 Como Executar o Projeto Localmente

Siga o passo a passo abaixo para rodar e testar o ambiente de desenvolvimento na sua máquina local:

1. Clonar o Repositório

Baixe o projeto diretamente do seu GitHub:

git clone https://github.com/lcarvalho03/gestao_loja.git
cd gestao_loja


2. Configurar o Ambiente Virtual (Virtualenv)

Recomenda-se isolar as dependências para evitar conflitos no seu sistema operacional:

# Criar o ambiente virtual na pasta .venv
python -m venv .venv

# Ativação do ambiente (Windows PowerShell)
.venv\Scripts\activate

# Ativação do ambiente (Linux/macOS)
source .venv/bin/activate


3. Instalar as Dependências do Python

Com o ambiente virtual ativado, instale os pacotes necessários listados no arquivo de requisitos:

pip install -r requirements.txt


4. Configurar as Variáveis de Ambiente (.env)

Copie o arquivo de exemplo para criar o seu arquivo .env definitivo:

# No Windows PowerShell:
cp .env.example .env


Abra o arquivo .env recém-criado na raiz do projeto e preencha as variáveis de ambiente com os dados de acesso ao seu servidor PostgreSQL local:

SECRET_KEY=uma-chave-secreta-longa-e-aleatoria-para-o-django
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

DB_NAME=nome_do_seu_banco
DB_USER=postgres
DB_PASSWORD=sua_senha_do_banco
DB_HOST=localhost
DB_PORT=5432


5. Executar as Migrations

Antes de rodar o servidor, crie a estrutura de tabelas no PostgreSQL. Certifique-se de que o seu banco já foi criado no gerenciador (como pgAdmin ou DBeaver) e execute:

python manage.py migrate


6. Inicializar o Servidor de Desenvolvimento

python manage.py runserver


Agora, basta abrir o seu navegador preferido e acessar a aplicação no endereço:
👉 http://127.0.0.1:8000/


✉️ Contato & Portfólio
Desenvolvido com dedicação por L. S. Carvalho. Sinta-se à vontade para se conectar comigo ou enviar feedbacks sobre o projeto:

💼 LinkedIn: www.linkedin.com/in/leonardo-lscarvalho — Conecte-se comigo profissionalmente.

✉️ E-mail: leo.freitascarvalho@gmail.com — Envie uma mensagem direta para parcerias ou dúvidas.

🐙 GitHub: lcarvalho03