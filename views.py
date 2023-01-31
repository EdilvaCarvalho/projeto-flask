from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
from biblioteca import app, db
from models import Livros, Usuarios
import os
import time
from helpers import FormularioLivro, FormularioUsuario

@app.route('/')
def index():
    lista = Livros.query.order_by(Livros.id)
    return render_template('lista.html', titulo='Livros', livros=lista)

@app.route('/cadastro')
def cadastro():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('cadastro')))
    form = FormularioLivro()
    return render_template('cadastro.html', titulo='Novo Livro', form=form)

@app.route('/criar', methods=['POST',])
def criar():
    form = FormularioLivro(request.form)

    if not form.validate_on_submit():
        flash('Formulário inválido!')
        return redirect(url_for('cadastro'))

    nome = form.nome.data
    genero = form.genero.data
    autor = form.autor.data
    num_paginas = form.num_paginas.data

    livro = Livros.query.filter_by(nome=nome).first()

    if livro:
        flash('Livro já existente!')
        return redirect(url_for('index'))

    novo_livro = Livros(nome=nome, genero=genero, autor=autor, num_paginas=num_paginas)

    db.session.add(novo_livro)
    db.session.commit()

    capa = request.files['capa']
    upload_path = app.config['UPLOAD_PATH']
    timestamp = time.time()
    capa.save(f'{upload_path}/capa{novo_livro.id}-{timestamp}.jpg')

    flash('Livro criado com sucesso!')
    return redirect(url_for('index'))

@app.route('/editar/<int:id>')
def editar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('editar')))
    livro = Livros.query.filter_by(id=id).first()
    form = FormularioLivro()
    form.nome.data = livro.nome
    form.genero.data = livro.genero
    form.autor.data = livro.autor
    form.num_paginas.data = livro.num_paginas

    return render_template('editar.html', titulo='Editar Livro', id=id, form=form)

@app.route('/atualizar', methods=['POST',])
def atualizar():
    form = FormularioLivro(request.form)

    if form.validate_on_submit():
        livro = Livros.query.filter_by(id=request.form['id']).first()
        livro.nome = form.nome.data
        livro.genero = form.genero.data
        livro.autor = form.autor.data
        livro.num_paginas = form.num_paginas.data

        db.session.add(livro)
        db.session.commit()

        capa = request.files['capa']
        upload_path = app.config['UPLOAD_PATH']
        timestamp = time.time()
        deleta_arquivo(livro.id)
        capa.save(f'{upload_path}/capa{livro.id}-{timestamp}.jpg')

        flash('Livro atualizado com sucesso!')
    else:
        flash('Erro ao atualizar!')

    return redirect(url_for('index'))

@app.route('/deletar/<int:id>')
def deletar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))

    Livros.query.filter_by(id=id).delete()
    db.session.commit()
    flash('Livro deletado com sucesso!')

    return redirect(url_for('index'))

@app.route('/visualizar/<int:id>')
def visualizar(id):
    livro = Livros.query.filter_by(id=id).first()
    capa_livro = recupera_imagem(id)
    return render_template('livro.html', livro=livro, capa=capa_livro)

@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    form = FormularioUsuario()
    return render_template('login.html', proxima=proxima, titulo='Login', form=form)

@app.route('/autenticar', methods=['POST',])
def autenticar():
    form = FormularioUsuario(request.form)

    usuario = Usuarios.query.filter_by(username=form.username.data).first()
    if usuario:
        if form.senha.data == usuario.senha:
            session['usuario_logado'] = usuario.username
            flash(usuario.username + ' logado com sucesso!')
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
        else:
            flash('Usuário não logado com sucesso!')
            return redirect(url_for('login'))
    else:
        flash('Usuário não logado com sucesso!')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Logout efetuado com sucesso!')
    return redirect(url_for('index'))

@app.route('/uploads/<nome_arquivo>')
def imagem(nome_arquivo):
    return send_from_directory('uploads', nome_arquivo)

def recupera_imagem(id):
    for nome_arquivo in os.listdir(app.config['UPLOAD_PATH']):
        if f'capa{id}' in nome_arquivo:
            return nome_arquivo

    return 'livro.png'

def deleta_arquivo(id):
    arquivo = recupera_imagem(id)
    if arquivo != 'livro.png':
        os.remove(os.path.join(app.config['UPLOAD_PATH'], arquivo))