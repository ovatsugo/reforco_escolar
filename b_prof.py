import sqlite3
import tkinter as tk
from tkinter import messagebox

conexao = sqlite3.connect("banco.db")
cursor = conexao.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS professores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    disciplina TEXT NOT NULL,
    telefone TEXT NOT NULL
)
""")

conexao.commit()


def cadastro_professor():
    janela = tk.Toplevel()
    janela.title("Cadastrar Professor")
    janela.geometry("350x300")
    janela.resizable(False, False)

    tk.Label(janela, text="Cadastrar Professor", font=("Arial", 14, "bold")).pack(pady=10)
    tk.Label(janela, text="Nome:").pack()
    entrada_nome = tk.Entry(janela, width=30)
    entrada_nome.pack(pady=4)
    tk.Label(janela, text="Disciplina:").pack()
    entrada_disciplina = tk.Entry(janela, width=30)
    entrada_disciplina.pack(pady=4)

    tk.Label(janela, text="Telefone:").pack()
    entrada_telefone = tk.Entry(janela, width=30)
    entrada_telefone.pack(pady=4)

    def salvar():

        nome = entrada_nome.get().strip()
        disciplina = entrada_disciplina.get().strip()
        telefone = entrada_telefone.get().strip()

        if not nome.replace(' ', '').isalpha():
            messagebox.showerror("Erro", "Digite somente letras no nome.")
            return

        if not disciplina.replace(' ', '').isalpha():
            messagebox.showerror("Erro", "Digite somente letras na disciplina.")
            return

        if not telefone.replace('-', '').replace(' ', '').isdigit():
            messagebox.showerror("Erro", "Digite somente números no telefone.")
            return

        cursor.execute(
            "INSERT INTO professores (nome, disciplina, telefone) VALUES (?, ?, ?)",
            (nome, disciplina, telefone)
        )
        conexao.commit()

        messagebox.showinfo("Sucesso", f"Professor '{nome}' cadastrado!")
        janela.destroy()

    tk.Button(janela, text="Salvar", command=salvar, width=15).pack(pady=12)


def listar_professores():

    janela = tk.Toplevel()
    janela.title("Lista de Professores")
    janela.geometry("420x350")

    tk.Label(janela, text="Lista de Professores", font=("Arial", 14, "bold")).pack(pady=10)

    barra = tk.Scrollbar(janela)
    barra.pack(side=tk.RIGHT, fill=tk.Y)

    caixa = tk.Text(janela, yscrollcommand=barra.set, width=48, height=18)
    caixa.pack(padx=10)
    barra.config(command=caixa.yview)

    cursor.execute("SELECT * FROM professores")
    professores = cursor.fetchall()

    if len(professores) == 0:
        caixa.insert(tk.END, "Nenhum professor cadastrado.")
    else:
        for professor in professores:
            caixa.insert(tk.END, f"ID: {professor[0]}\n")
            caixa.insert(tk.END, f"Nome: {professor[1]}\n")
            caixa.insert(tk.END, f"Disciplina: {professor[2]}\n")
            caixa.insert(tk.END, f"Telefone: {professor[3]}\n")
            caixa.insert(tk.END, "-" * 30 + "\n")

    caixa.config(state=tk.DISABLED)


def atualizar_professor():

    janela = tk.Toplevel()
    janela.title("Atualizar Professor")
    janela.geometry("350x340")
    janela.resizable(False, False)

    tk.Label(janela, text="Atualizar Professor", font=("Arial", 14, "bold")).pack(pady=10)

    tk.Label(janela, text="Nome atual do professor:").pack()
    entrada_busca = tk.Entry(janela, width=30)
    entrada_busca.pack(pady=4)

    tk.Label(janela, text="Novo nome:").pack()
    entrada_novo_nome = tk.Entry(janela, width=30)
    entrada_novo_nome.pack(pady=4)

    tk.Label(janela, text="Nova disciplina:").pack()
    entrada_nova_disciplina = tk.Entry(janela, width=30)
    entrada_nova_disciplina.pack(pady=4)

    tk.Label(janela, text="Novo telefone:").pack()
    entrada_novo_telefone = tk.Entry(janela, width=30)
    entrada_novo_telefone.pack(pady=4)

    def atualizar():

        nome_busca = entrada_busca.get().strip()
        novo_nome = entrada_novo_nome.get().strip()
        nova_disciplina = entrada_nova_disciplina.get().strip()
        novo_telefone = entrada_novo_telefone.get().strip()

        cursor.execute("SELECT * FROM professores WHERE nome = ?", (nome_busca,))
        professor = cursor.fetchone()

        if professor is None:
            messagebox.showerror("Erro", "Professor não encontrado.")
            return

        if not novo_nome.replace(' ', '').isalpha():
            messagebox.showerror("Erro", "Digite somente letras no nome.")
            return

        if not nova_disciplina.replace(' ', '').isalpha():
            messagebox.showerror("Erro", "Digite somente letras na disciplina.")
            return

        if not novo_telefone.replace('-', '').replace(' ', '').isdigit():
            messagebox.showerror("Erro", "Digite somente números no telefone.")
            return

        cursor.execute(
            "UPDATE professores SET nome = ?, disciplina = ?, telefone = ? WHERE nome = ?",
            (novo_nome, nova_disciplina, novo_telefone, nome_busca)
        )
        conexao.commit()

        messagebox.showinfo("Sucesso", "Professor atualizado com sucesso!")
        janela.destroy()

    tk.Button(janela, text="Atualizar", command=atualizar, width=15).pack(pady=10)


def remover_professor():

    janela = tk.Toplevel()
    janela.title("Remover Professor")
    janela.geometry("350x200")
    janela.resizable(False, False)

    tk.Label(janela, text="Remover Professor", font=("Arial", 14, "bold")).pack(pady=10)

    tk.Label(janela, text="ID do professor que deseja remover:").pack()
    entrada_id = tk.Entry(janela, width=30)
    entrada_id.pack(pady=4)

    def remover():

        id_busca = entrada_id.get().strip()

        if not id_busca.isdigit():
            messagebox.showerror("Erro", "Digite apenas números.")
            return

        id_busca = int(id_busca)

        cursor.execute("SELECT * FROM professores WHERE id = ?", (id_busca,))
        professor = cursor.fetchone()

        if professor is None:
            messagebox.showerror("Erro", "Professor não encontrado.")
            return

        confirmacao = messagebox.askyesno(
            "Confirmar", f"Deseja remover '{professor[1]}'?"
        )

        if confirmacao:
            cursor.execute("DELETE FROM professores WHERE id = ?", (id_busca,))
            conexao.commit()
            messagebox.showinfo("Sucesso", "Professor removido com sucesso!")
            janela.destroy()

    tk.Button(janela, text="Remover", command=remover, width=15).pack(pady=12)
