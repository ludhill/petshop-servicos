#Para Linux/macOS:
#!/bin/bash

echo "Criando ambiente virtual..."
python3 -m venv .venv

echo "Ativando ambiente virtual..."
source .venv/bin/activate

echo "Instalando dependências..."
pip install -r requirements.txt

if [ -d "migrations" ]; then
    echo "Pasta 'migrations' já existe. Pulando flask db init..."
else
    echo "Inicializando Flask-Migrate..."
    flask db init
fi

if [ -f ".env" ]; then
    echo ".env já existe."
else
    echo "SECRET_KEY=lucasmoisesrafael" > .env
    echo ".env criado com SECRET_KEY padrão."
fi

echo "Gerando e aplicando migração..."
flask db migrate -m "Inicial"
flask db upgrade

echo "Projeto configurado com sucesso!"
