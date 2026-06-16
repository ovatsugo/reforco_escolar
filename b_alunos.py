import sqlite3

conexao = sqlite3.connect("alunos.db")
cursor = conexao.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS alunos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    idade INTEGER NOT NULL
)
""")

conexao.commit()


def cadastro_aluno():

    while True:

        nome = input("Digite o seu nome para o cadastro: ")

        if nome.replace(' ', '').isalpha():
            break

        print('Digite somente letras.')

    while True:

        idade = input('Digite sua idade: ')

        if idade.isdigit():

            idade = int(idade)
            break

        print('Digite somente numeros.')

    cursor.execute(
        """
        INSERT INTO alunos (nome, idade)
        VALUES (?, ?)
        """,
        (nome, idade)
    )

    conexao.commit()

    print('Aluno cadastrado.')
    input('Clique ENTER para continuar...')


def atualizar_aluno():

    nome_busca = input(
        'Digite o nome do aluno que você deseja atualizar: '
    )

    cursor.execute(
        "SELECT * FROM alunos WHERE nome = ?",
        (nome_busca,)
    )

    aluno = cursor.fetchone()

    if aluno is None:

        print('Aluno não encontrado.')
        input('Digite ENTER para continuar...')
        return

    while True:

        novo_nome = input('Digite o novo nome: ')

        if novo_nome.replace(' ', '').isalpha():
            break

        print('Digite somente letras.')

    while True:

        nova_idade = input('Digite a nova idade: ')

        if nova_idade.isdigit():

            nova_idade = int(nova_idade)
            break

        print('Digite somente numeros.')

    cursor.execute(
        """
        UPDATE alunos
        SET nome = ?, idade = ?
        WHERE nome = ?
        """,
        (novo_nome, nova_idade, nome_busca)
    )

    conexao.commit()

    print('Aluno atualizado com sucesso!')
    input('Digite ENTER para continuar...')


def listar_alunos():

    cursor.execute("SELECT * FROM alunos")

    alunos = cursor.fetchall()

    if len(alunos) == 0:

        print('Nenhum aluno cadastrado.')
        input('Digite ENTER para continuar...')
        return

    print('\n===== LISTA DE ALUNOS =====')

    for aluno in alunos:

        print(f'''
ID: {aluno[0]}
Nome: {aluno[1]}
Idade: {aluno[2]}
''')

    input('\nClique ENTER para continuar...')


def remover_aluno():

    id_busca = input(
        'Digite o ID do aluno que deseja remover: '
    )

    if not id_busca.isdigit():

        print('Digite apenas números.')
        input('Digite ENTER para continuar...')
        return

    id_busca = int(id_busca)

    cursor.execute(
        "SELECT * FROM alunos WHERE id = ?",
        (id_busca,)
    )

    aluno = cursor.fetchone()

    if aluno is None:

        print('Aluno não encontrado.')
        input('Digite ENTER para continuar...')
        return

    cursor.execute(
        "DELETE FROM alunos WHERE id = ?",
        (id_busca,)
    )

    conexao.commit()

    print('Aluno removido com sucesso!')
    input('Digite ENTER para continuar...')