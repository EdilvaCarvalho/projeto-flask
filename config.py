SECRET_KEY = 'ifpb2022'

SQLALCHEMY_DATABASE_URI = \
    '{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(
        SGBD = 'postgresql',
        usuario = 'postgres',
        senha = 'postgres',
        servidor = 'localhost',
        database = 'biblioteca-flask'
    )