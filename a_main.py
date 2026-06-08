from b_alunos import *

def menu():

    while True:

        print("=" * 30)
        print("         MENU")
        print("=" * 30)

        print("1 - Cadastrar aluno")
        print("2 - Listar aluno")
        print("3 - Atualizar aluno")
        print("4 - Remover aluno")
        print("0 - Sair")

        opcao = input("\nDigite a opção que você deseja: ")

        if opcao == "1":
            cadastro_aluno()

        elif opcao == "2":
            listar_aluno()

        elif opcao == "3":
            atualizar_alunos()

        elif opcao == "4":
            print("Remover aluno")

        elif opcao == "0":
            print("Saindo...")
            break

        else:
            print("Opção inválida.")


menu()