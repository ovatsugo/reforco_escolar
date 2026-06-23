import tkinter as tk
from tkinter import messagebox
import sqlite3

# Importa as funções prontas dos colegas
from b_alunos import cadastro_aluno, listar_alunos, atualizar_aluno, remover_aluno
from b_prof import cadastro_professor, listar_professores, atualizar_professor, remover_professor

# ============================================================
#  RESPONSÁVEL: Integrante 5 — Líder
#  ARQUIVO: main.py
#
#  - Importa diretamente as funções de b_alunos.py e b_prof.py
#  - b_alunos.py e b_prof.py NÃO foram modificados
#  - As telas de Sessões e Relatórios ficam aqui pois ainda
#    não há arquivo de colega responsável por elas
#  - Todos os dados vão para o mesmo banco.db
# ============================================================


# -------------------------------------------------------
# FUNÇÃO 1 — inicializar_banco
# Cria as tabelas de sessoes no banco.db caso não existam
# (alunos e professores já são criadas pelos colegas)
# -------------------------------------------------------

def inicializar_banco():

    conexao = sqlite3.connect("banco.db")
    cursor = conexao.cursor()

    cursor.execute("""
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

    conexao.commit()
    conexao.close()


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

    tk.Button(
        janela,
        text="Alunos",
        width=20,
        command=menu_alunos
    ).pack(pady=5)

    tk.Button(
        janela,
        text="Professores / Voluntários",
        width=20,
        command=menu_professores
    ).pack(pady=5)

    tk.Button(
        janela,
        text="Sessões de Reforço",
        width=20,
        command=menu_sessoes
    ).pack(pady=5)

    tk.Button(
        janela,
        text="Relatórios",
        width=20,
        command=menu_relatorios
    ).pack(pady=5)

    tk.Button(
        janela,
        text="Sair",
        width=20,
        command=janela.destroy
    ).pack(pady=15)

    janela.mainloop()


# -------------------------------------------------------
# FUNÇÃO 3 — menu_alunos
# Chama as funções prontas do b_alunos.py do colega
# -------------------------------------------------------

def menu_alunos():

    janela = tk.Toplevel()
    janela.title("Alunos")
    janela.geometry("300x280")
    janela.resizable(False, False)

    tk.Label(
        janela,
        text="CRUD DE ALUNOS",
        font=("Arial", 14, "bold")
    ).pack(pady=20)

    tk.Button(
        janela,
        text="Cadastrar aluno",
        width=20,
        command=cadastro_aluno       # função do b_alunos.py
    ).pack(pady=5)

    tk.Button(
        janela,
        text="Listar alunos",
        width=20,
        command=listar_alunos        # função do b_alunos.py
    ).pack(pady=5)

    tk.Button(
        janela,
        text="Atualizar aluno",
        width=20,
        command=atualizar_aluno      # função do b_alunos.py
    ).pack(pady=5)

    tk.Button(
        janela,
        text="Remover aluno",
        width=20,
        command=remover_aluno        # função do b_alunos.py
    ).pack(pady=5)

    tk.Button(
        janela,
        text="Voltar",
        width=20,
        command=janela.destroy
    ).pack(pady=10)


# -------------------------------------------------------
# FUNÇÃO 4 — menu_professores
# Chama as funções prontas do b_prof.py do colega
# -------------------------------------------------------

def menu_professores():

    janela = tk.Toplevel()
    janela.title("Professores / Voluntários")
    janela.geometry("300x280")
    janela.resizable(False, False)

    tk.Label(
        janela,
        text="CRUD DE PROFESSORES",
        font=("Arial", 14, "bold")
    ).pack(pady=20)

    tk.Button(
        janela,
        text="Cadastrar professor",
        width=20,
        command=cadastro_professor   # função do b_prof.py
    ).pack(pady=5)

    tk.Button(
        janela,
        text="Listar professores",
        width=20,
        command=listar_professores   # função do b_prof.py
    ).pack(pady=5)

    tk.Button(
        janela,
        text="Atualizar professor",
        width=20,
        command=atualizar_professor  # função do b_prof.py
    ).pack(pady=5)

    tk.Button(
        janela,
        text="Remover professor",
        width=20,
        command=remover_professor    # função do b_prof.py
    ).pack(pady=5)

    tk.Button(
        janela,
        text="Voltar",
        width=20,
        command=janela.destroy
    ).pack(pady=10)


# -------------------------------------------------------
# FUNÇÃO 5 (extra do líder) — menu_sessoes + menu_relatorios
# Telas implementadas aqui pois os colegas ainda não
# têm arquivos para sessões e relatórios
# Todas conectam no mesmo banco.db
# -------------------------------------------------------

def menu_sessoes():

    janela = tk.Toplevel()
    janela.title("Sessões de Reforço")
    janela.geometry("300x280")
    janela.resizable(False, False)

    tk.Label(
        janela,
        text="SESSÕES DE REFORÇO",
        font=("Arial", 14, "bold")
    ).pack(pady=20)

    tk.Button(janela, text="Agendar sessão",   width=20, command=tela_agendar_sessao).pack(pady=5)
    tk.Button(janela, text="Listar sessões",   width=20, command=tela_listar_sessoes).pack(pady=5)
    tk.Button(janela, text="Atualizar sessão", width=20, command=tela_atualizar_sessao).pack(pady=5)
    tk.Button(janela, text="Cancelar sessão",  width=20, command=tela_cancelar_sessao).pack(pady=5)

    tk.Button(janela, text="Voltar", width=20, command=janela.destroy).pack(pady=10)


def tela_agendar_sessao():

    janela = tk.Toplevel()
    janela.title("Agendar Sessão")
    janela.geometry("400x460")
    janela.resizable(False, False)

    tk.Label(janela, text="Agendar Sessão", font=("Arial", 14, "bold")).pack(pady=10)

    # Frame que vai conter os menus de aluno e professor
    # É recriado toda vez que o usuário atualiza a lista
    frame_menus = tk.Frame(janela)
    frame_menus.pack()

    aluno_var = tk.StringVar()
    prof_var = tk.StringVar()

    # Guarda referência dos menus para poder recriar
    menus = {}

    def carregar_menus():
        """
        Busca alunos e professores do banco nesse exato momento.
        Chamada na abertura e quando o usuário clica em 'Atualizar lista'.
        """

        # Limpa os widgets anteriores do frame
        for widget in frame_menus.winfo_children():
            widget.destroy()

        conexao = sqlite3.connect("banco.db")
        alunos = conexao.execute("SELECT id, nome FROM alunos").fetchall()
        professores = conexao.execute("SELECT id, nome, disciplina FROM professores").fetchall()
        conexao.close()

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

    # Carrega a lista ao abrir a janela
    carregar_menus()

    # Botão para recarregar caso o usuário tenha cadastrado alunos
    # depois de abrir essa janela
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

        conexao = sqlite3.connect("banco.db")
        cursor = conexao.cursor()

        nome_aluno = cursor.execute(
            "SELECT nome FROM alunos WHERE id = ?", (id_aluno,)
        ).fetchone()[0]

        prof = cursor.execute(
            "SELECT nome, disciplina FROM professores WHERE id = ?", (id_professor,)
        ).fetchone()

        nome_professor = prof[0]
        disciplina = prof[1]

        cursor.execute("""
            INSERT INTO sessoes
            (id_aluno, nome_aluno, id_professor, nome_professor, disciplina, data, horario, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (id_aluno, nome_aluno, id_professor, nome_professor, disciplina, data, horario, "agendada"))

        conexao.commit()
        conexao.close()

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

    conexao = sqlite3.connect("banco.db")
    sessoes = conexao.execute("SELECT * FROM sessoes").fetchall()
    conexao.close()

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

        conexao = sqlite3.connect("banco.db")
        cursor = conexao.cursor()

        sessao = cursor.execute(
            "SELECT * FROM sessoes WHERE id = ?", (id_busca,)
        ).fetchone()

        if sessao is None:
            conexao.close()
            messagebox.showerror("Erro", "Sessão não encontrada.")
            return

        nova_data = entrada_data.get().strip() or sessao[6]
        novo_horario = entrada_horario.get().strip() or sessao[7]
        novo_status = status_var.get()

        cursor.execute(
            "UPDATE sessoes SET data = ?, horario = ?, status = ? WHERE id = ?",
            (nova_data, novo_horario, novo_status, id_busca)
        )
        conexao.commit()
        conexao.close()

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

        conexao = sqlite3.connect("banco.db")
        cursor = conexao.cursor()

        sessao = cursor.execute(
            "SELECT * FROM sessoes WHERE id = ?", (id_busca,)
        ).fetchone()

        if sessao is None:
            conexao.close()
            messagebox.showerror("Erro", "Sessão não encontrada.")
            return

        confirmacao = messagebox.askyesno(
            "Confirmar",
            f"Deseja cancelar a sessão de '{sessao[2]}' em {sessao[6]}?"
        )

        if confirmacao:
            cursor.execute("DELETE FROM sessoes WHERE id = ?", (id_busca,))
            conexao.commit()
            messagebox.showinfo("Sucesso", "Sessão cancelada e removida!")
            janela.destroy()

        conexao.close()

    tk.Button(janela, text="Cancelar Sessão", command=cancelar, width=18).pack(pady=12)


def menu_relatorios():

    janela = tk.Toplevel()
    janela.title("Relatórios")
    janela.geometry("300x280")
    janela.resizable(False, False)

    tk.Label(
        janela,
        text="RELATÓRIOS",
        font=("Arial", 14, "bold")
    ).pack(pady=20)

    tk.Button(janela, text="Por aluno",               width=20, command=tela_relatorio_por_aluno).pack(pady=5)
    tk.Button(janela, text="Por professor",           width=20, command=tela_relatorio_por_professor).pack(pady=5)
    tk.Button(janela, text="Atendimentos realizados", width=20, command=tela_relatorio_realizadas).pack(pady=5)
    tk.Button(janela, text="Por disciplina",          width=20, command=tela_relatorio_por_disciplina).pack(pady=5)

    tk.Button(janela, text="Voltar", width=20, command=janela.destroy).pack(pady=10)


# Função auxiliar — abre janela de resultado com barra de rolagem
def abrir_resultado(titulo, conteudo):

    janela = tk.Toplevel()
    janela.title(titulo)
    janela.geometry("440x360")

    tk.Label(janela, text=titulo, font=("Arial", 13, "bold")).pack(pady=10)

    barra = tk.Scrollbar(janela)
    barra.pack(side=tk.RIGHT, fill=tk.Y)

    caixa = tk.Text(janela, yscrollcommand=barra.set, width=52, height=19)
    caixa.pack(padx=10)
    barra.config(command=caixa.yview)

    caixa.insert(tk.END, conteudo)
    caixa.config(state=tk.DISABLED)


def tela_relatorio_por_aluno():

    janela = tk.Toplevel()
    janela.title("Relatório por Aluno")
    janela.geometry("350x160")
    janela.resizable(False, False)

    tk.Label(janela, text="Relatório por Aluno", font=("Arial", 13, "bold")).pack(pady=10)
    tk.Label(janela, text="Nome do aluno (ou parte):").pack()

    entrada = tk.Entry(janela, width=30)
    entrada.pack(pady=4)

    def buscar():

        busca = entrada.get().strip().lower()

        conexao = sqlite3.connect("banco.db")
        sessoes = conexao.execute("SELECT * FROM sessoes").fetchall()
        conexao.close()

        conteudo = ""
        for s in sessoes:
            if busca in s[2].lower():
                conteudo += f"ID: {s[0]}  |  Status: {s[8].upper()}\n"
                conteudo += f"Professor: {s[4]}\n"
                conteudo += f"Disciplina: {s[5]}\n"
                conteudo += f"Data: {s[6]} às {s[7]}\n"
                conteudo += "-" * 38 + "\n"

        if not conteudo:
            conteudo = f"Nenhuma sessão encontrada para '{busca}'."

        janela.destroy()
        abrir_resultado(f"Sessões — {busca}", conteudo)

    tk.Button(janela, text="Buscar", command=buscar, width=15).pack(pady=10)


def tela_relatorio_por_professor():

    janela = tk.Toplevel()
    janela.title("Relatório por Professor")
    janela.geometry("350x160")
    janela.resizable(False, False)

    tk.Label(janela, text="Relatório por Professor", font=("Arial", 13, "bold")).pack(pady=10)
    tk.Label(janela, text="Nome do professor (ou parte):").pack()

    entrada = tk.Entry(janela, width=30)
    entrada.pack(pady=4)

    def buscar():

        busca = entrada.get().strip().lower()

        conexao = sqlite3.connect("banco.db")
        sessoes = conexao.execute("SELECT * FROM sessoes").fetchall()
        conexao.close()

        conteudo = ""
        total = 0
        for s in sessoes:
            if busca in s[4].lower():
                conteudo += f"ID: {s[0]}  |  Status: {s[8].upper()}\n"
                conteudo += f"Aluno: {s[2]}\n"
                conteudo += f"Disciplina: {s[5]}\n"
                conteudo += f"Data: {s[6]} às {s[7]}\n"
                conteudo += "-" * 38 + "\n"
                total += 1

        if not conteudo:
            conteudo = f"Nenhuma sessão encontrada para '{busca}'."
        else:
            conteudo += f"\nTotal de sessões: {total}"

        janela.destroy()
        abrir_resultado(f"Sessões — {busca}", conteudo)

    tk.Button(janela, text="Buscar", command=buscar, width=15).pack(pady=10)


def tela_relatorio_realizadas():

    conexao = sqlite3.connect("banco.db")
    sessoes = conexao.execute(
        "SELECT * FROM sessoes WHERE status = 'realizada'"
    ).fetchall()
    conexao.close()

    conteudo = ""

    if not sessoes:
        conteudo = "Nenhuma sessão marcada como realizada ainda."
    else:
        conteudo += f"Total de atendimentos realizados: {len(sessoes)}\n"
        conteudo += "=" * 38 + "\n"
        for s in sessoes:
            conteudo += f"- {s[2]} com {s[4]} | {s[5]} | {s[6]}\n"

    abrir_resultado("Atendimentos Realizados", conteudo)


def tela_relatorio_por_disciplina():

    janela = tk.Toplevel()
    janela.title("Relatório por Disciplina")
    janela.geometry("350x160")
    janela.resizable(False, False)

    tk.Label(janela, text="Relatório por Disciplina", font=("Arial", 13, "bold")).pack(pady=10)
    tk.Label(janela, text="Disciplina (ou parte):").pack()

    entrada = tk.Entry(janela, width=30)
    entrada.pack(pady=4)

    def buscar():

        busca = entrada.get().strip().lower()

        conexao = sqlite3.connect("banco.db")
        sessoes = conexao.execute("SELECT * FROM sessoes").fetchall()
        conexao.close()

        conteudo = ""
        for s in sessoes:
            if busca in s[5].lower():
                conteudo += f"ID: {s[0]}  |  Status: {s[8].upper()}\n"
                conteudo += f"Aluno: {s[2]}\n"
                conteudo += f"Professor: {s[4]}\n"
                conteudo += f"Data: {s[6]} às {s[7]}\n"
                conteudo += "-" * 38 + "\n"

        if not conteudo:
            conteudo = f"Nenhuma sessão encontrada para '{busca}'."

        janela.destroy()
        abrir_resultado(f"Sessões de {busca}", conteudo)

    tk.Button(janela, text="Buscar", command=buscar, width=15).pack(pady=10)


# Ponto de entrada
inicializar_banco()
menu_principal()