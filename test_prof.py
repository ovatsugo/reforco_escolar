import tkinter as tk
from b_prof import cadastro_professor, listar_professores, atualizar_professor, remover_professor

janela = tk.Tk()
janela.title("CRUD DE PROFESSORES")
janela.geometry("300x300")
janela.resizable(False, False)

titulo = tk.Label(
    janela,
    text="CRUD DE PROFESSORES",
    font=("Arial", 16, "bold")
)

titulo.pack(pady=20)

tk.Button(
    janela,
    text="Cadastrar professor",
    width=20,
    command=cadastro_professor
).pack(pady=5)

tk.Button(
    janela,
    text="Listar professores",
    width=20,
    command=listar_professores
).pack(pady=5)

tk.Button(
    janela,
    text="Atualizar professor",
    width=20,
    command=atualizar_professor
).pack(pady=5)

tk.Button(
    janela,
    text="Remover professor",
    width=20,
    command=remover_professor
).pack(pady=5)

janela.mainloop()