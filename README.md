# Computer Vision & Audio Pipeline em Streamlit

Sistema completo e enterprise de Visão Computacional de tempo real e Processamento de Linguagem Natural (Speech to Text) construído em arquitetura isolada, rodando integralmente de forma gratuita na nuvem.

## 🚀 Tecnologias Aplicadas

* **Python 3.12+**
* **Streamlit** - Interface WEB responsiva e nativa
* **OpenCV & Pillow** - Processamento analítico de imagens e Visão Computacional
* **SQLAlchemy** - Mapeamento Objeto-Relacional (ORM)
* **Neon.tech** - Banco de dados PostgreSQL Serverless na Nuvem
* **Faster-Whisper** - Transcrição de áudio via IA de altíssima performance para CPU
* **Render** - Plataforma de hospedagem e Deploy Contínuo (CI/CD)

## 🏗️ Arquitetura do Sistema

O projeto segue padrões de **Clean Architecture**, dividindo responsabilidades de forma explícita:
* `Models`: Entidades e tabelas representativas.
* `Repositories`: Comunicação exclusiva de persistência de dados.
* `Services`: Algoritmos puros, processamento de imagens e motores de áudio.
* `Controllers`: Orquestração de entrada, tomada de decisões e saída.
* `Components`: Views encapsuladas do Streamlit.

## 🔧 Instalação e Execução Local

Como pré-requisito, certifique-se de configurar as variáveis no arquivo `.env` baseando-se no `.env.example`. Não é necessária a inicialização de ambientes virtuais (venv) manuais de documentação para a execução deste projeto.

1. Instale todas as dependências do sistema:
```bash
pip install -r requirements.txt