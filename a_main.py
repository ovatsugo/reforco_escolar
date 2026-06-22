import tkinter as tk
from b_alunos import cadastro_aluno, listar_alunos, atualizar_aluno, remover_aluno


janela = tk.Tk()

janela.title("CRUD DE ALUNOS")
janela.geometry("300x300")
janela.resizable(False, False)


titulo = tk.Label(
    janela,
    text="CRUD DE ALUNOS",
    font=("Arial", 16, "bold")
)

titulo.pack(pady=20)


tk.Button(
    janela,
    text="Cadastrar aluno",
    width=20,
    command=cadastro_aluno
).pack(pady=5)


tk.Button(
    janela,
    text="Listar alunos",
    width=20,
    command=listar_alunos
).pack(pady=5)


tk.Button(
    janela,
    text="Atualizar aluno",
    width=20,
    command=atualizar_aluno
).pack(pady=5)


tk.Button(
    janela,
    text="Remover aluno",
    width=20,
    command=remover_aluno
).pack(pady=5)


janela.mainloop()