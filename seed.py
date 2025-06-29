from app import create_app, db
from app.models import Cliente, Pet, Funcionario

app = create_app()
app.app_context().push()

# Recria as tabelas (cuidado: apaga dados se já existirem)
db.drop_all()
db.create_all()

# Cria um cliente com pets associados
cliente = Cliente(
    nome="João Silva",
    telefone="84999999999",
    email="joao@email.com",
    pets=[
        Pet(nome="Luna", genero="Fêmea", raca="Poodle"),
        Pet(nome="Thor", genero="Macho", raca="Labrador"),
        Pet(nome="Mia", genero="Fêmea", raca="Persa")
    ]
)

# Cria profissionais
profissionais = [
    Funcionario(nome="Lucas", cargo="Veterinário"),
    Funcionario(nome="Rafael", cargo="Tosador"),
    Funcionario(nome="Moisés", cargo="Banhista")
]

# Adiciona tudo ao banco
db.session.add(cliente)
db.session.add_all(profissionais)
db.session.commit()

print("Banco de dados populado com sucesso!")
