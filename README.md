# 🐾 Petshop - Módulo de Serviços

Este é o módulo de agendamento de serviços do sistema Petshop, desenvolvido por Lucas, Moisés e Rafael.

## 🚀 Funcionalidades

- Cadastro de clientes e pets
- Agendamento de serviços por profissional
- Exportação de serviços em PDF e Excel
- Filtros por status e data
- Interface dinâmica com validação

## 🛠️ Tecnologias

- Python + Flask
- SQLite + SQLAlchemy
- HTML + CSS + JavaScript
- Pandas, xhtml2pdf, openpyxl

## 📦 Como executar

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/petshop-servicos.git
   cd petshop-servicos

2. Crie e ative o ambiente virtual:
   ```bash
    python -m venv .venv
    source .venv/bin/activate  # Linux/macOS
    .venv\\Scripts\\activate   # Windows

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt

5. Execute o projeto:
   ```bash
   python seed.py (OPCIONAL: POPULE O BANCO)
   python run.py

6. Acesse em:
   ```URL
   http://localhost:5000