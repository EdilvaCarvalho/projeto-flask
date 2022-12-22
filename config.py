import os

SECRET_KEY = 'ifpb2022'

SQLALCHEMY_DATABASE_URI = \
    '{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(
        SGBD = 'postgresql',
        usuario = 'postgres',
        senha = 'postgres',
        servidor = 'localhost',
        database = 'biblioteca-flask'
    )

# pegando o nome do caminho absoluto do diretório e concatenando com o diretório uplouds
UPLOAD_PATH = os.path.dirname(os.path.abspath(__file__)) + '/uploads'

