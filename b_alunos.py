import sqlite3
import tkinter as tk
from tkinter import messagebox

conexao = sqlite3.connect("banco.db")
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

    janela = tk.Toplevel()
    janela.title("Cadastrar Aluno")
    janela.geometry("350x220")
    janela.resizable(False, False)

    tk.Label(janela, text="Cadastrar Aluno", font=("Arial", 14, "bold")).pack(pady=10)

    tk.Label(janela, text="Nome:").pack()
    entrada_nome = tk.Entry(janela, width=30)
    entrada_nome.pack(pady=4)

    tk.Label(janela, text="Idade:").pack()
    entrada_idade = tk.Entry(janela, width=30)
    entrada_idade.pack(pady=4)

    def salvar():

        nome = entrada_nome.get().strip()
        idade = entrada_idade.get().strip()

        if not nome.replace(' ', '').isalpha():
            messagebox.showerror("Erro", "Digite somente letras no nome.")
            return

        if not idade.isdigit():
            messagebox.showerror("Erro", "Digite somente números na idade.")
            return

        cursor.execute(
            "INSERT INTO alunos (nome, idade) VALUES (?, ?)",
            (nome, int(idade))
        )
        conexao.commit()

        messagebox.showinfo("Sucesso", f"Aluno '{nome}' cadastrado!")
        janela.destroy()

    tk.Button(janela, text="Salvar", command=salvar, width=15).pack(pady=12)

def listar_alunos():

    janela = tk.Toplevel()
    janela.title("Lista de Alunos")
    janela.geometry("400x350")

    tk.Label(janela, text="Lista de Alunos", font=("Arial", 14, "bold")).pack(pady=10)

    barra = tk.Scrollbar(janela)
    barra.pack(side=tk.RIGHT, fill=tk.Y)

    caixa = tk.Text(janela, yscrollcommand=barra.set, width=45, height=18)
    caixa.pack(padx=10)
    barra.config(command=caixa.yview)

    cursor.execute("SELECT * FROM alunos")
    alunos = cursor.fetchall()

    if len(alunos) == 0:
        caixa.insert(tk.END, "Nenhum aluno cadastrado.")
    else:
        for aluno in alunos:
            caixa.insert(tk.END, f"ID: {aluno[0]}\n")
            caixa.insert(tk.END, f"Nome: {aluno[1]}\n")
            caixa.insert(tk.END, f"Idade: {aluno[2]}\n")
            caixa.insert(tk.END, "-" * 30 + "\n")

    caixa.config(state=tk.DISABLED)


def atualizar_aluno():

    janela = tk.Toplevel()
    janela.title("Atualizar Aluno")
    janela.geometry("350x280")
    janela.resizable(False, False)

    tk.Label(janela, text="Atualizar Aluno", font=("Arial", 14, "bold")).pack(pady=10)

    tk.Label(janela, text="Nome atual do aluno:").pack()
    entrada_busca = tk.Entry(janela, width=30)
    entrada_busca.pack(pady=4)

    tk.Label(janela, text="Novo nome:").pack()
    entrada_novo_nome = tk.Entry(janela, width=30)
    entrada_novo_nome.pack(pady=4)

    tk.Label(janela, text="Nova idade:").pack()
    entrada_nova_idade = tk.Entry(janela, width=30)
    entrada_nova_idade.pack(pady=4)

    def atualizar():

        nome_busca = entrada_busca.get().strip()
        novo_nome = entrada_novo_nome.get().strip()
        nova_idade = entrada_nova_idade.get().strip()

        cursor.execute("SELECT * FROM alunos WHERE nome = ?", (nome_busca,))
        aluno = cursor.fetchone()

        if aluno is None:
            messagebox.showerror("Erro", "Aluno não encontrado.")
            return

        if not novo_nome.replace(' ', '').isalpha():
            messagebox.showerror("Erro", "Digite somente letras no nome.")
            return

        if not nova_idade.isdigit():
            messagebox.showerror("Erro", "Digite somente números na idade.")
            return

        cursor.execute(
            "UPDATE alunos SET nome = ?, idade = ? WHERE nome = ?",
            (novo_nome, int(nova_idade), nome_busca)
        )
        conexao.commit()

        messagebox.showinfo("Sucesso", "Aluno atualizado com sucesso!")
        janela.destroy()

    tk.Button(janela, text="Atualizar", command=atualizar, width=15).pack(pady=10)


def remover_aluno():

    janela = tk.Toplevel()
    janela.title("Remover Aluno")
    janela.geometry("350x200")
    janela.resizable(False, False)

    tk.Label(janela, text="Remover Aluno", font=("Arial", 14, "bold")).pack(pady=10)

    tk.Label(janela, text="ID do aluno que deseja remover:").pack()
    entrada_id = tk.Entry(janela, width=30)
    entrada_id.pack(pady=4)

    def remover():

        id_busca = entrada_id.get().strip()

        if not id_busca.isdigit():
            messagebox.showerror("Erro", "Digite apenas números.")
            return

        id_busca = int(id_busca)

        cursor.execute("SELECT * FROM alunos WHERE id = ?", (id_busca,))
        aluno = cursor.fetchone()

        if aluno is None:
            messagebox.showerror("Erro", "Aluno não encontrado.")
            return

        confirmacao = messagebox.askyesno(
            "Confirmar", f"Deseja remover '{aluno[1]}'?"
        )

        if confirmacao:
            cursor.execute("DELETE FROM alunos WHERE id = ?", (id_busca,))
            conexao.commit()
            messagebox.showinfo("Sucesso", "Aluno removido com sucesso!")
            janela.destroy()

    tk.Button(janela, text="Remover", command=remover, width=15).pack(pady=12)