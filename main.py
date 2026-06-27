import tkinter as tk
from tkinter import messagebox
import sqlite3
import os



os.chdir(os.path.dirname(os.path.abspath(__file__)))

from b_alunos import cadastro_aluno, atualizar_aluno, remover_aluno
from b_prof import cadastro_professor, atualizar_professor, remover_professor
from e_relatorios import (
    relatorio_por_aluno,
    relatorio_por_professor,
    relatorio_por_disciplina,
    relatorio_realizadas,
)

conexao_main = sqlite3.connect("banco.db")
cursor_main = conexao_main.cursor()


# Incialização do banco

def inicializar_banco():

    cursor_main.execute("""
        CREATE TABLE IF NOT EXISTS alunos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            idade INTEGER NOT NULL
        )
    """)

    cursor_main.execute("""
        CREATE TABLE IF NOT EXISTS professores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            disciplina TEXT NOT NULL,
            telefone TEXT NOT NULL
        )
    """)

    cursor_main.execute("""
        CREATE TABLE IF NOT EXISTS sessoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_aluno INTEGER NOT NULL,
            nome_aluno TEXT NOT NULL,
            id_professor INTEGER NOT NULL,
            nome_professor TEXT NOT NULL,
            disciplina TEXT NOT NULL,
            data TEXT NOT NULL,
            horario TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'agendada'
        )
    """)

    conexao_main.commit()



def buscar(sql, params=()):
    """Abre uma conexão nova, executa e fecha. Garante dados frescos."""
    con = sqlite3.connect("banco.db")
    resultado = con.execute(sql, params).fetchall()
    con.close()
    return resultado


# -------------------------------------------------------
# FUNÇÃO 2 — menu_principal
# Janela raiz — ponto de entrada do programa
# -------------------------------------------------------

def menu_principal():

    janela = tk.Tk()
    janela.title("Plataforma de Reforço Escolar")
    janela.geometry("300x350")
    janela.resizable(False, False)

    tk.Label(
        janela,
        text="Reforço Escolar",
        font=("Arial", 16, "bold")
    ).pack(pady=20)

    tk.Button(janela, text="Alunos",                    width=20, command=menu_alunos).pack(pady=5)
    tk.Button(janela, text="Professores / Voluntários", width=20, command=menu_professores).pack(pady=5)
    tk.Button(janela, text="Sessões de Reforço",        width=20, command=menu_sessoes).pack(pady=5)
    tk.Button(janela, text="Relatórios",                width=20, command=menu_relatorios).pack(pady=5)
    tk.Button(janela, text="Sair",                      width=20, command=janela.destroy).pack(pady=15)

    janela.mainloop()


# Listar usa conexão fresca; demais chamam b_alunos.py

def menu_alunos():

    janela = tk.Toplevel()
    janela.title("Alunos")
    janela.geometry("300x280")
    janela.resizable(False, False)

    tk.Label(janela, text="CRUD DE ALUNOS", font=("Arial", 14, "bold")).pack(pady=20)

    tk.Button(janela, text="Cadastrar aluno", width=20, command=cadastro_aluno).pack(pady=5)
    tk.Button(janela, text="Listar alunos",   width=20, command=listar_alunos_fresco).pack(pady=5)
    tk.Button(janela, text="Atualizar aluno", width=20, command=atualizar_aluno).pack(pady=5)
    tk.Button(janela, text="Remover aluno",   width=20, command=remover_aluno).pack(pady=5)
    tk.Button(janela, text="Voltar",          width=20, command=janela.destroy).pack(pady=10)


def listar_alunos_fresco():
    """Lista alunos com conexão nova — sempre mostra dados atualizados."""

    janela = tk.Toplevel()
    janela.title("Lista de Alunos")
    janela.geometry("400x350")

    tk.Label(janela, text="Lista de Alunos", font=("Arial", 14, "bold")).pack(pady=10)

    barra = tk.Scrollbar(janela)
    barra.pack(side=tk.RIGHT, fill=tk.Y)

    caixa = tk.Text(janela, yscrollcommand=barra.set, width=45, height=18)
    caixa.pack(padx=10)
    barra.config(command=caixa.yview)

    alunos = buscar("SELECT * FROM alunos")

    if not alunos:
        caixa.insert(tk.END, "Nenhum aluno cadastrado.")
    else:
        for aluno in alunos:
            caixa.insert(tk.END, f"ID: {aluno[0]}\n")
            caixa.insert(tk.END, f"Nome: {aluno[1]}\n")
            caixa.insert(tk.END, f"Idade: {aluno[2]}\n")
            caixa.insert(tk.END, "-" * 30 + "\n")

    caixa.config(state=tk.DISABLED)


# -------------------------------------------------------
# FUNÇÃO 4 — menu_professores
# Listar usa conexão fresca; demais chamam b_prof.py
# -------------------------------------------------------

def menu_professores():

    janela = tk.Toplevel()
    janela.title("Professores / Voluntários")
    janela.geometry("300x280")
    janela.resizable(False, False)

    tk.Label(janela, text="CRUD DE PROFESSORES", font=("Arial", 14, "bold")).pack(pady=20)

    tk.Button(janela, text="Cadastrar professor", width=20, command=cadastro_professor).pack(pady=5)
    tk.Button(janela, text="Listar professores",  width=20, command=listar_professores_fresco).pack(pady=5)
    tk.Button(janela, text="Atualizar professor", width=20, command=atualizar_professor).pack(pady=5)
    tk.Button(janela, text="Remover professor",   width=20, command=remover_professor).pack(pady=5)
    tk.Button(janela, text="Voltar",              width=20, command=janela.destroy).pack(pady=10)


def listar_professores_fresco():
    """Lista professores com conexão nova — sempre mostra dados atualizados."""

    janela = tk.Toplevel()
    janela.title("Lista de Professores")
    janela.geometry("420x350")

    tk.Label(janela, text="Lista de Professores", font=("Arial", 14, "bold")).pack(pady=10)

    barra = tk.Scrollbar(janela)
    barra.pack(side=tk.RIGHT, fill=tk.Y)

    caixa = tk.Text(janela, yscrollcommand=barra.set, width=48, height=18)
    caixa.pack(padx=10)
    barra.config(command=caixa.yview)

    professores = buscar("SELECT * FROM professores")

    if not professores:
        caixa.insert(tk.END, "Nenhum professor cadastrado.")
    else:
        for p in professores:
            caixa.insert(tk.END, f"ID: {p[0]}\n")
            caixa.insert(tk.END, f"Nome: {p[1]}\n")
            caixa.insert(tk.END, f"Disciplina: {p[2]}\n")
            caixa.insert(tk.END, f"Telefone: {p[3]}\n")
            caixa.insert(tk.END, "-" * 30 + "\n")

    caixa.config(state=tk.DISABLED)



def menu_sessoes():

    janela = tk.Toplevel()
    janela.title("Sessões de Reforço")
    janela.geometry("300x280")
    janela.resizable(False, False)

    tk.Label(janela, text="SESSÕES DE REFORÇO", font=("Arial", 14, "bold")).pack(pady=20)

    tk.Button(janela, text="Agendar sessão",   width=20, command=tela_agendar_sessao).pack(pady=5)
    tk.Button(janela, text="Listar sessões",   width=20, command=tela_listar_sessoes).pack(pady=5)
    tk.Button(janela, text="Atualizar sessão", width=20, command=tela_atualizar_sessao).pack(pady=5)
    tk.Button(janela, text="Cancelar sessão",  width=20, command=tela_cancelar_sessao).pack(pady=5)
    tk.Button(janela, text="Voltar",           width=20, command=janela.destroy).pack(pady=10)


def tela_agendar_sessao():

    janela = tk.Toplevel()
    janela.title("Agendar Sessão")
    janela.geometry("400x460")
    janela.resizable(False, False)

    tk.Label(janela, text="Agendar Sessão", font=("Arial", 14, "bold")).pack(pady=10)

    frame_menus = tk.Frame(janela)
    frame_menus.pack()

    aluno_var = tk.StringVar()
    prof_var = tk.StringVar()
    menus = {}

    def carregar_menus():

        for widget in frame_menus.winfo_children():
            widget.destroy()

        alunos = buscar("SELECT id, nome FROM alunos")
        professores = buscar("SELECT id, nome, disciplina FROM professores")

        if not alunos:
            tk.Label(frame_menus, text="Nenhum aluno cadastrado ainda.", fg="red").pack()
        else:
            tk.Label(frame_menus, text="Aluno:").pack()
            opcoes_alunos = [f"{a[0]} - {a[1]}" for a in alunos]
            aluno_var.set(opcoes_alunos[0])
            menus["aluno"] = tk.OptionMenu(frame_menus, aluno_var, *opcoes_alunos)
            menus["aluno"].config(width=28)
            menus["aluno"].pack(pady=4)

        if not professores:
            tk.Label(frame_menus, text="Nenhum professor cadastrado ainda.", fg="red").pack()
        else:
            tk.Label(frame_menus, text="Professor/Voluntário:").pack()
            opcoes_professores = [f"{p[0]} - {p[1]} ({p[2]})" for p in professores]
            prof_var.set(opcoes_professores[0])
            menus["prof"] = tk.OptionMenu(frame_menus, prof_var, *opcoes_professores)
            menus["prof"].config(width=28)
            menus["prof"].pack(pady=4)

    carregar_menus()

    tk.Button(
        janela,
        text="↻ Atualizar lista de alunos/professores",
        command=carregar_menus,
        width=35
    ).pack(pady=4)

    tk.Label(janela, text="Data (ex: 26/06/2026):").pack()
    entrada_data = tk.Entry(janela, width=30)
    entrada_data.pack(pady=4)

    tk.Label(janela, text="Horário (ex: 14:00):").pack()
    entrada_horario = tk.Entry(janela, width=30)
    entrada_horario.pack(pady=4)

    def salvar():

        if not aluno_var.get() or not prof_var.get():
            messagebox.showerror("Erro", "Cadastre um aluno e um professor antes de agendar.")
            return

        id_aluno = int(aluno_var.get().split(" - ")[0])
        id_professor = int(prof_var.get().split(" - ")[0])
        data = entrada_data.get().strip()
        horario = entrada_horario.get().strip()

        if not data or not horario:
            messagebox.showerror("Erro", "Data e horário são obrigatórios.")
            return

        nome_aluno = buscar("SELECT nome FROM alunos WHERE id = ?", (id_aluno,))[0][0]
        prof = buscar("SELECT nome, disciplina FROM professores WHERE id = ?", (id_professor,))[0]
        nome_professor = prof[0]
        disciplina = prof[1]

        con = sqlite3.connect("banco.db")
        con.execute("""
            INSERT INTO sessoes
            (id_aluno, nome_aluno, id_professor, nome_professor, disciplina, data, horario, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (id_aluno, nome_aluno, id_professor, nome_professor, disciplina, data, horario, "agendada"))
        con.commit()
        con.close()

        messagebox.showinfo("Sucesso", f"Sessão agendada!\n{nome_aluno} com {nome_professor}\n{data} às {horario}")
        janela.destroy()

    tk.Button(janela, text="Agendar", command=salvar, width=15).pack(pady=12)


def tela_listar_sessoes():

    janela = tk.Toplevel()
    janela.title("Lista de Sessões")
    janela.geometry("440x370")

    tk.Label(janela, text="Lista de Sessões", font=("Arial", 14, "bold")).pack(pady=10)

    barra = tk.Scrollbar(janela)
    barra.pack(side=tk.RIGHT, fill=tk.Y)

    caixa = tk.Text(janela, yscrollcommand=barra.set, width=52, height=20)
    caixa.pack(padx=10)
    barra.config(command=caixa.yview)

    sessoes = buscar("SELECT * FROM sessoes")

    if not sessoes:
        caixa.insert(tk.END, "Nenhuma sessão agendada.")
    else:
        for s in sessoes:
            caixa.insert(tk.END, f"ID: {s[0]}  |  Status: {s[8].upper()}\n")
            caixa.insert(tk.END, f"Aluno: {s[2]}\n")
            caixa.insert(tk.END, f"Professor: {s[4]}\n")
            caixa.insert(tk.END, f"Disciplina: {s[5]}\n")
            caixa.insert(tk.END, f"Data: {s[6]} às {s[7]}\n")
            caixa.insert(tk.END, "-" * 38 + "\n")

    caixa.config(state=tk.DISABLED)


def tela_atualizar_sessao():

    janela = tk.Toplevel()
    janela.title("Atualizar Sessão")
    janela.geometry("350x290")
    janela.resizable(False, False)

    tk.Label(janela, text="Atualizar Sessão", font=("Arial", 14, "bold")).pack(pady=10)

    tk.Label(janela, text="ID da sessão:").pack()
    entrada_id = tk.Entry(janela, width=30)
    entrada_id.pack(pady=4)

    tk.Label(janela, text="Nova data (ex: 26/06/2026):").pack()
    entrada_data = tk.Entry(janela, width=30)
    entrada_data.pack(pady=4)

    tk.Label(janela, text="Novo horário (ex: 14:00):").pack()
    entrada_horario = tk.Entry(janela, width=30)
    entrada_horario.pack(pady=4)

    tk.Label(janela, text="Novo status:").pack()
    status_var = tk.StringVar(value="agendada")
    tk.OptionMenu(janela, status_var, "agendada", "realizada", "cancelada").pack(pady=4)

    def atualizar():

        id_busca = entrada_id.get().strip()

        if not id_busca.isdigit():
            messagebox.showerror("Erro", "Digite apenas números no ID.")
            return

        id_busca = int(id_busca)
        sessao = buscar("SELECT * FROM sessoes WHERE id = ?", (id_busca,))

        if not sessao:
            messagebox.showerror("Erro", "Sessão não encontrada.")
            return

        sessao = sessao[0]
        nova_data = entrada_data.get().strip() or sessao[6]
        novo_horario = entrada_horario.get().strip() or sessao[7]
        novo_status = status_var.get()

        con = sqlite3.connect("banco.db")
        con.execute(
            "UPDATE sessoes SET data = ?, horario = ?, status = ? WHERE id = ?",
            (nova_data, novo_horario, novo_status, id_busca)
        )
        con.commit()
        con.close()

        messagebox.showinfo("Sucesso", "Sessão atualizada com sucesso!")
        janela.destroy()

    tk.Button(janela, text="Atualizar", command=atualizar, width=15).pack(pady=10)


def tela_cancelar_sessao():

    janela = tk.Toplevel()
    janela.title("Cancelar Sessão")
    janela.geometry("350x180")
    janela.resizable(False, False)

    tk.Label(janela, text="Cancelar Sessão", font=("Arial", 14, "bold")).pack(pady=10)

    tk.Label(janela, text="ID da sessão que deseja cancelar:").pack()
    entrada_id = tk.Entry(janela, width=30)
    entrada_id.pack(pady=4)

    def cancelar():

        id_busca = entrada_id.get().strip()

        if not id_busca.isdigit():
            messagebox.showerror("Erro", "Digite apenas números.")
            return

        id_busca = int(id_busca)
        sessao = buscar("SELECT * FROM sessoes WHERE id = ?", (id_busca,))

        if not sessao:
            messagebox.showerror("Erro", "Sessão não encontrada.")
            return

        sessao = sessao[0]
        confirmacao = messagebox.askyesno(
            "Confirmar",
            f"Deseja cancelar a sessão de '{sessao[2]}' em {sessao[6]}?"
        )

        if confirmacao:
            con = sqlite3.connect("banco.db")
            con.execute("DELETE FROM sessoes WHERE id = ?", (id_busca,))
            con.commit()
            con.close()
            messagebox.showinfo("Sucesso", "Sessão cancelada e removida!")
            janela.destroy()

    tk.Button(janela, text="Cancelar Sessão", command=cancelar, width=18).pack(pady=12)


def menu_relatorios():

    janela = tk.Toplevel()
    janela.title("Relatórios")
    janela.geometry("300x280")
    janela.resizable(False, False)

    tk.Label(janela, text="RELATÓRIOS", font=("Arial", 14, "bold")).pack(pady=20)

    # Chama diretamente as funções do e_relatorios.py
    tk.Button(janela, text="Por aluno",               width=20, command=relatorio_por_aluno).pack(pady=5)
    tk.Button(janela, text="Por professor",           width=20, command=relatorio_por_professor).pack(pady=5)
    tk.Button(janela, text="Atendimentos realizados", width=20, command=relatorio_realizadas).pack(pady=5)
    tk.Button(janela, text="Por disciplina",          width=20, command=relatorio_por_disciplina).pack(pady=5)
    tk.Button(janela, text="Voltar",                  width=20, command=janela.destroy).pack(pady=10)


# Ponto de entrada
inicializar_banco()
menu_principal()