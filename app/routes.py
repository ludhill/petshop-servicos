from flask import Blueprint, render_template, render_template_string, request, redirect, url_for, flash, send_file
from app import db
from .models import  Cliente, Pet, Funcionario, Servico
from datetime import datetime
from app.config_servicos import SERVICOS_POR_CARGO
from io import BytesIO
from xhtml2pdf import pisa
import pandas as pd

main = Blueprint('main', __name__)

@main.route('/')
def index():
    status = request.args.get('status')
    data_min = request.args.get('data_min')
    page = request.args.get('page', 1, type=int)

    query = Servico.query

    if status:
        query = query.filter_by(status=status)

    if data_min:
        try:
            data_obj = datetime.strptime(data_min, '%Y-%m-%d')
            query = query.filter(Servico.data_agendada >= data_obj)
        except ValueError:
            pass

    servicos = query.order_by(Servico.data_agendada).paginate(page=page, per_page=5)
    return render_template('index.html', servicos=servicos)

@main.route('/cliente', methods=['GET', 'POST'])
def cadastrar_cliente():
    if request.method == 'POST':
        nome = request.form['nome']
        telefone = request.form['telefone']
        email = request.form['email']
        cliente = Cliente(nome=nome, telefone=telefone, email=email)
        db.session.add(cliente)
        db.session.commit()
        flash("Cliente cadastrado com sucesso!")
        return redirect(url_for('main.index'))
    return render_template('cliente.html')

@main.route('/agendar', methods=['GET', 'POST'])
def agendar():
    clientes = Cliente.query.all()
    pets = Pet.query.all()
    profissionais = Funcionario.query.all()

    if request.method == 'POST':
        tipo = request.form['tipo']
        data_str = request.form['data']
        data = datetime.strptime(data_str, '%Y-%m-%dT%H:%M')
        pet_id = request.form['pet_id']
        funcionario_id = request.form['funcionario_id']

        funcionario = Funcionario.query.get(funcionario_id)
        if not funcionario:
            flash("Profissional inválido.")
            return redirect(url_for('main.agendar'))

        servicos_validos = SERVICOS_POR_CARGO.get(funcionario.cargo, [])
        if tipo not in servicos_validos:
            flash(f"O serviço '{tipo}' não é permitido para o cargo '{funcionario.cargo}'.")
            return redirect(url_for('main.agendar'))

        servico = Servico(
            tipo=tipo,
            data_agendada=data,
            pet_id=pet_id,
            funcionario_id=funcionario_id
        )
        db.session.add(servico)
        db.session.commit()
        flash("Serviço agendado com sucesso!")
        return redirect(url_for('main.index'))

    return render_template('agendar.html', clientes=clientes, pets=pets, profissionais=profissionais)


@main.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_servico(id):
    servico = Servico.query.get_or_404(id)
    profissionais = Funcionario.query.all()

    if request.method == 'POST':
        servico.status = request.form['status']
        servico.funcionario_id = request.form['funcionario_id']
        db.session.commit()
        return redirect(url_for('main.index'))

    return render_template('editar.html', servico=servico, profissionais=profissionais)

@main.route('/excluir/<int:id>')
def excluir_servico(id):
    servico = Servico.query.get_or_404(id)
    db.session.delete(servico)
    db.session.commit()
    return redirect(url_for('main.index'))

@main.route('/exportar/excel')
def exportar_excel():
    status = request.args.get('status')
    data_min = request.args.get('data_min')

    query = Servico.query

    if status:
        query = query.filter_by(status=status)

    if data_min:
        try:
            data_obj = datetime.strptime(data_min, '%Y-%m-%d')
            query = query.filter(Servico.data_agendada >= data_obj)
        except ValueError:
            pass

    servicos = query.all()

    if not servicos:
        flash("Nenhum serviço encontrado para exportar.")
        return redirect(url_for('main.index'))

    data = [{
        'Tipo': s.tipo,
        'Data': s.data_agendada.strftime('%d/%m/%Y %H:%M'),
        'Pet': s.pet.nome,
        'Tutor': s.pet.dono.nome,
        'Profissional': s.funcionario.nome,
        'Status': s.status
    } for s in servicos]

    df = pd.DataFrame(data)
    output = BytesIO()
    df.to_excel(output, index=False, engine='openpyxl')
    output.seek(0)

    return send_file(
        output,
        download_name='servicos.xlsx',
        as_attachment=True,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

@main.route('/importar/excel', methods=['POST'])
def importar_excel():
    file = request.files.get('arquivo')
    if not file or not file.filename.endswith(('.xls', '.xlsx')):
        flash("Arquivo inválido. Envie um Excel .xls ou .xlsx")
        return redirect(url_for('main.index'))

    try:
        df = pd.read_excel(file)
        for _, row in df.iterrows():
            pet = Pet.query.filter_by(nome=row['Pet']).first()
            dono = Cliente.query.filter_by(nome=row['Tutor']).first()
            funcionario = Funcionario.query.filter_by(nome=row['Profissional']).first()

            if pet and funcionario:
                novo_servico = Servico(
                    tipo=row['Tipo'],
                    data_agendada=datetime.strptime(row['Data'], '%d/%m/%Y %H:%M'),
                    pet_id=pet.id,
                    funcionario_id=funcionario.id,
                    status=row['Status']
                )
                db.session.add(novo_servico)
        db.session.commit()
        flash("Serviços importados com sucesso!")
    except Exception as e:
        flash(f"Erro ao importar: {str(e)}")

    return redirect(url_for('main.index'))

@main.route('/exportar/pdf')
def exportar_pdf():
    status = request.args.get('status')
    data_min = request.args.get('data_min')

    query = Servico.query

    if status:
        query = query.filter_by(status=status)

    if data_min:
        try:
            data_obj = datetime.strptime(data_min, '%Y-%m-%d')
            query = query.filter(Servico.data_agendada >= data_obj)
        except ValueError:
            pass

    servicos = query.all()

    # if not servicos:
    #     return "Nenhum serviço encontrado para exportar.", 400
    if not servicos:
        flash("Nenhum serviço encontrado para exportar.")
        return redirect(url_for('main.index'))

    html = render_template_string("""
    <h2>Serviços Agendados</h2>
    <table border="1" cellpadding="5">
      <tr>
        <th>Tipo</th><th>Data</th><th>Pet</th><th>Tutor</th><th>Profissional</th><th>Status</th>
      </tr>
      {% for s in servicos %}
      <tr>
        <td>{{ s.tipo }}</td>
        <td>{{ s.data_agendada.strftime('%d/%m/%Y %H:%M') }}</td>
        <td>{{ s.pet.nome }}</td>
        <td>{{ s.pet.dono.nome }}</td>
        <td>{{ s.funcionario.nome }}</td>
        <td>{{ s.status }}</td>
      </tr>
      {% endfor %}
    </table>
    """, servicos=servicos)

    output = BytesIO()
    pisa.CreatePDF(html, dest=output)
    output.seek(0)
    
    return send_file(
        output,
        download_name='servicos.pdf',
        mimetype='application/pdf',
        as_attachment=False
    )

    # return send_file(output, download_name='servicos.pdf', as_attachment=True)
# @main.route('/')
# def index():
#     status = request.args.get('status')
#     data_min = request.args.get('data_min')

#     query = Servico.query

#     if status:
#         query = query.filter_by(status=status)

#     if data_min:
#         try:
#             data_obj = datetime.strptime(data_min, '%Y-%m-%d')
#             query = query.filter(Servico.data_agendada >= data_obj)
#         except ValueError:
#             pass  # ignora se a data for inválida

#     servicos = query.order_by(Servico.data_agendada).all()
#     return render_template('index.html', servicos=servicos)

# @main.route('/')
# def index():
#     servicos = Servico.query.all()
#     return render_template('index.html', servicos=servicos)


# from flask import Blueprint, render_template, request, redirect, url_for
# from .models import Servico, Pet, Funcionario
# from . import db
# from datetime import datetime 


# main = Blueprint('main', __name__)

# @main.route('/')
# def index():
#     servicos = Servico.query.all()
#     return render_template('index.html', servicos=servicos)

# # @main.route('/agendar', methods=['GET', 'POST'])
# # def agendar():
# #     if request.method == 'POST':
# #         novo = Servico(
# #             tipo=request.form['tipo'],
# #             pet=request.form['pet'],
# #             profissional=request.form['profissional'],
# #             data_agendada=datetime.strptime(request.form['data'], '%Y-%m-%dT%H:%M')
# #         )
# #         db.session.add(novo)
# #         db.session.commit()
# #         return redirect(url_for('main.index'))
# #     return render_template('agendar.html')

# @main.route('/agendar', methods=['GET', 'POST'])
# def agendar():
#     tipos = ['Banho', 'Tosa', 'Consulta', 'Adestramento', 'Hospedagem']
#     pets = Pet.query.all()
#     profissionais = Funcionario.query.all()

#     if request.method == 'POST':
#         tipo = request.form['tipo']
#         pet = request.form['pet']
#         profissional = request.form['profissional']
#         data = request.form['data']

#         if not tipo or not pet or not profissional or not data:
#             # return render_template('agendar.html', erro="Todos os campos são obrigatórios.", tipos=tipos, pets=pets)
#             return render_template('agendar.html', erro="Todos os campos são obrigatórios.", tipos=tipos, pets=pets, profissionais=profissionais)

#         novo = Servico(
#             tipo=tipo,
#             pet=pet,
#             profissional=profissional,
#             data_agendada=datetime.strptime(data, '%Y-%m-%dT%H:%M')
#         )
#         db.session.add(novo)
#         db.session.commit()
#         return redirect(url_for('main.index'))

#     return render_template('agendar.html', tipos=tipos, pets=pets)

# @main.route('/editar/<int:id>', methods=['GET', 'POST'])
# def editar(id):
#     servico = Servico.query.get_or_404(id)
#     if request.method == 'POST':
#         servico.status = request.form['status']
#         db.session.commit()
#         return redirect(url_for('main.index'))
#     return render_template('editar.html', servico=servico)

# @main.route('/excluir/<int:id>')
# def excluir(id):
#     servico = Servico.query.get_or_404(id)
#     db.session.delete(servico)
#     db.session.commit()
#     return redirect(url_for('main.index'))


