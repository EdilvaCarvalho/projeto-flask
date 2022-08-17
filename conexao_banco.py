import psycopg2

conn = psycopg2.connect(
        host="localhost",
        database="biblioteca-flask",
        user='postgres',
        password='postgres')

# Abra um cursor para realizar operações de banco de dados
cur = conn.cursor()

# Execute um comando: isso cria uma nova tabela
cur.execute('DROP TABLE IF EXISTS Livros;')
cur.execute('CREATE TABLE Livros (id serial PRIMARY KEY,'
                                 'nome varchar (150) NOT NULL,'
                                 'genero varchar (50) NOT NULL,'
                                 'autor varchar (150) NOT NULL,'
                                 'num_paginas integer NOT NULL);'
                                 )
cur.execute('DROP TABLE IF EXISTS Usuarios;')
cur.execute('CREATE TABLE Usuarios (id serial PRIMARY KEY,'
                                 'nome varchar (150) NOT NULL,'
                                 'username varchar (30) NOT NULL,'
                                 'senha varchar (30) NOT NULL);'
                                 )

# Insert data into the table

cur.execute('INSERT INTO Livros (nome, genero, autor, num_paginas)'
            'VALUES (%s, %s, %s, %s)',
            ('A Moreninha',
             'Romance',
             'Joaquim Manuel de Macedo',
             216)
            )


cur.execute('INSERT INTO Livros (nome, genero, autor, num_paginas)'
            'VALUES (%s, %s, %s, %s)',
            ('As Crônicas de Nárnia',
             'Fantasia',
             'C. S. Lewis',
             752)
            )

cur.execute('INSERT INTO Usuarios (nome, username, senha)'
            'VALUES (%s, %s, %s)',
            ('Edilva Carvalho',
             'Edilva',
             '12345')
            )

conn.commit()

cur.close()
conn.close()