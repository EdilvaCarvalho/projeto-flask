from flask import render_template, request, redirect, session, flash, url_for
from biblioteca import app, db
from models import Livros, Usuarios

@app.route('/')
def index():
    lista = Livros.query.order_by(Livros.id)
    return render_template('lista.html', titulo='Livros', livros=lista)

@app.route('/cadastro')
def cadastro():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('cadastro')))
    return render_template('cadastro.html', titulo='Novo Livro')

@app.route('/criar', methods=['POST',])
def criar():
    nome = request.form['nome']
    genero = request.form['genero']
    autor = request.form['autor']
    num_paginas = request.form['num_paginas']
    livro = Livros(nome=nome, genero=genero, autor=autor, num_paginas=num_paginas)

    db.session.add(livro)
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/editar/<int:id>')
def editar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('editar')))
    livro = Livros.query.filter_by(id=id).first()
    return render_template('editar.html', titulo='Editar Livro', livro=livro)

@app.route('/atualizar', methods=['POST',])
def atualizar():
    livro = Livros.query.filter_by(id=request.form['id']).first()
    livro.nome = request.form['nome']
    livro.genero = request.form['genero']
    livro.autor = request.form['autor']
    livro.num_paginas = request.form['num_paginas']
    print(livro)
    db.session.add(livro)
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/deletar/<int:id>')
def deletar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))

    Livros.query.filter_by(id=id).delete()
    db.session.commit()
    flash('Livro deletado com sucesso!')

    return redirect(url_for('index'))

@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima, titulo='Login')

@app.route('/autenticar', methods=['POST',])
def autenticar():
    usuario = Usuarios.query.filter_by(username=request.form['usuario']).first()
    if usuario:
        if request.form['senha'] == usuario.senha:
            session['usuario_logado'] = usuario.username
            flash(usuario.username + ' logado com sucesso!')
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
    else:
        flash('Usuário não logado com sucesso!')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Logout efetuado com sucesso!')
    return redirect(url_for('index'))