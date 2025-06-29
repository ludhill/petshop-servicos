@REM Para Windows:
@echo off
echo Criando ambiente virtual...
python -m venv .venv

echo Ativando ambiente virtual...
call .venv\Scripts\activate

echo Instalando dependências...
pip install -r requirements.txt

IF EXIST migrations (
    echo Pasta 'migrations' já existe. Pulando flask db init...
) ELSE (
    echo Inicializando Flask-Migrate...
    flask db init
)

IF EXIST .env (
    echo Arquivo .env já existe.
) ELSE (
    echo SECRET_KEY=lucasmoisesrafael> .env
    echo .env criado com SECRET_KEY padrão.
)

echo Gerando e aplicando migração...
flask db migrate -m "Inicial"
flask db upgrade

echo Projeto configurado com sucesso!
pause
