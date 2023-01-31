from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, PasswordField, validators

class FormularioLivro(FlaskForm):
    nome = StringField('Nome', [validators.DataRequired(), validators.Length(min=1, max=150)])
    genero = StringField('Gênero', [validators.DataRequired(), validators.Length(min=1, max=50)])
    autor = StringField('Autor', [validators.DataRequired(), validators.Length(min=1, max=150)])
    num_paginas = IntegerField('Número de páginas', [validators.DataRequired()])
    salvar = SubmitField('Salvar')

class FormularioUsuario(FlaskForm):
    username = StringField('Nome de usuário', [validators.DataRequired(), validators.Length(min=1, max=30)])
    senha = PasswordField('Senha', [validators.DataRequired(), validators.Length(min=1, max=30)])
    login = SubmitField('Entrar')