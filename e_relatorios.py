# Relatórios do sistema de reforço escolar
# Atualizado pelo grupo em 2026

import sqlite3
import tkinter as tk
from tkinter import messagebox


conexao = sqlite3.connect("banco.db")
cursor = conexao.cursor()


# Função auxiliar de exibição 
def abrir_janela_relatorio(titulo, conteudo):

    janela = tk.Toplevel()
    janela.title(titulo)
    janela.geometry("460x380")

    tk.Label(janela, text=titulo, font=("Arial", 13, "bold")).pack(pady=10)

    barra = tk.Scrollbar(janela)
    barra.pack(side=tk.RIGHT, fill=tk.Y)

    caixa = tk.Text(janela, yscrollcommand=barra.set, width=55, height=20)
    caixa.pack(padx=10)
    barra.config(command=caixa.yview)

    caixa.insert(tk.END, conteudo)
    caixa.config(state=tk.DISABLED)


# monta a janela de busca que as 3 funções abaixo repetem
def _janela_busca(titulo, label):

    janela = tk.Toplevel()
    janela.title(titulo)
    janela.geometry("350x170")
    janela.resizable(False, False)

    tk.Label(janela, text=titulo, font=("Arial", 13, "bold")).pack(pady=10)
    tk.Label(janela, text=label).pack()

    campo_busca = tk.Entry(janela, width=30)
    campo_busca.pack(pady=4)
    campo_busca.focus_set()

    return janela, campo_busca


# Relatórios por filtro 

def relatorio_por_aluno():

    janela, campo_busca = _janela_busca("Relatório por Aluno", "Nome do aluno (ou parte):")

    def buscar():

        busca = campo_busca.get().strip()

        if not busca:
            messagebox.showerror("Erro", "Digite o nome do aluno.")
            return

        try:
            cursor.execute(
                """
                SELECT nome_aluno, nome_professor, disciplina, data, horario, status
                FROM sessoes
                WHERE LOWER(nome_aluno) LIKE LOWER(?)
                ORDER BY data
                """,
                (f"%{busca}%",)
            )
            sessoes = cursor.fetchall()

        except sqlite3.Error as erro:
            messagebox.showerror("Erro no banco", f"Falha ao consultar: {erro}")
            return

        if not sessoes:
            conteudo = f"Nenhuma sessão encontrada para '{busca}'."
        else:
            conteudo = f"Aluno: {sessoes[0][0]}\n" + "=" * 40 + "\n"
            for s in sessoes:
                conteudo += f"Professor: {s[1]}\nDisciplina: {s[2]}\nData: {s[3]} às {s[4]}\nStatus: {s[5].upper()}\n" + "-" * 40 + "\n"
            conteudo += f"\nTotal de sessões: {len(sessoes)}"

        janela.destroy()
        abrir_janela_relatorio(f"Sessões do aluno: {busca}", conteudo)

    tk.Button(janela, text="Buscar", command=buscar, width=15).pack(pady=10)


def relatorio_por_professor():

    janela, campo_busca = _janela_busca("Relatório por Professor", "Nome do professor (ou parte):")

    def buscar():

        busca = campo_busca.get().strip()

        if not busca:
            messagebox.showerror("Erro", "Digite o nome do professor.")
            return

        try:
            cursor.execute(
                """
                SELECT nome_professor, nome_aluno, disciplina, data, horario, status
                FROM sessoes
                WHERE LOWER(nome_professor) LIKE LOWER(?)
                ORDER BY data
                """,
                (f"%{busca}%",)
            )
            sessoes = cursor.fetchall()

        except sqlite3.Error as erro:
            messagebox.showerror("Erro no banco", f"Falha ao consultar: {erro}")
            return

        if not sessoes:
            conteudo = f"Nenhuma sessão encontrada para '{busca}'."
        else:
            conteudo = f"Professor: {sessoes[0][0]}\n" + "=" * 40 + "\n"
            for s in sessoes:
                conteudo += f"Aluno: {s[1]}\nDisciplina: {s[2]}\nData: {s[3]} às {s[4]}\nStatus: {s[5].upper()}\n" + "-" * 40 + "\n"
            conteudo += f"\nTotal de sessões: {len(sessoes)}"

        janela.destroy()
        abrir_janela_relatorio(f"Sessões do professor: {busca}", conteudo)

    tk.Button(janela, text="Buscar", command=buscar, width=15).pack(pady=10)


def relatorio_por_disciplina():

    janela, campo_busca = _janela_busca("Relatório por Disciplina", "Disciplina (ou parte):")

    def buscar():

        busca = campo_busca.get().strip()

        if not busca:
            messagebox.showerror("Erro", "Digite o nome da disciplina.")
            return

        try:
            cursor.execute(
                """
                SELECT nome_aluno, nome_professor, disciplina, data, horario, status
                FROM sessoes
                WHERE LOWER(disciplina) LIKE LOWER(?)
                ORDER BY data
                """,
                (f"%{busca}%",)
            )
            sessoes = cursor.fetchall()

        except sqlite3.Error as erro:
            messagebox.showerror("Erro no banco", f"Falha ao consultar: {erro}")
            return

        if not sessoes:
            conteudo = f"Nenhuma sessão encontrada para disciplina '{busca}'."
        else:
            conteudo = f"Disciplina: {sessoes[0][2]}\n" + "=" * 40 + "\n"
            for s in sessoes:
                conteudo += f"Aluno: {s[0]}\nProfessor: {s[1]}\nData: {s[3]} às {s[4]}\nStatus: {s[5].upper()}\n" + "-" * 40 + "\n"

        janela.destroy()
        abrir_janela_relatorio(f"Sessões de: {busca}", conteudo)

    tk.Button(janela, text="Buscar", command=buscar, width=15).pack(pady=10)


# sem filtro — mostra tudo que foi realizado
def relatorio_realizadas():

    try:
        cursor.execute(
            """
            SELECT nome_aluno, nome_professor, disciplina, data, horario
            FROM sessoes
            WHERE LOWER(status) = 'realizada'
            ORDER BY data
            """
        )
        sessoes = cursor.fetchall()

    except sqlite3.Error as erro:
        messagebox.showerror("Erro no banco", f"Falha ao consultar: {erro}")
        return

    if not sessoes:
        conteudo = "Nenhuma sessão marcada como realizada ainda."
    else:
        conteudo  = f"Total de atendimentos realizados: {len(sessoes)}\n"
        conteudo += "=" * 40 + "\n"
        for s in sessoes:
            conteudo += f"- {s[0]} com {s[1]} | {s[2]} | {s[3]}\n"

    abrir_janela_relatorio("Atendimentos Realizados", conteudo)
