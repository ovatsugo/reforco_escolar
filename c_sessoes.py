import sqlite3
import tkinter as tk
from tkinter import messagebox

# ============================================================
#  RESPONSÁVEL: Integrante 3 — CRUD de Sessões
#  ARQUIVO: c_sessoes.py
#
#  Funções exportadas (usadas pelo main.py do Líder):
#    - agendar_sessao()
#    - listar_sessoes()
#    - atualizar_sessao()
#    - cancelar_sessao()
#    - tela_sessoes.html  → equivalente: menu_sessoes() aqui
#
#  Banco: banco.db (mesmo usado por b_alunos.py e b_prof.py)
#  Tabela: sessoes (criada pelo inicializar_banco() do main.py;
#          mas garantida também aqui para rodar de forma independente)
# ============================================================

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


# -------------------------------------------------------
# FUNÇÃO 1 — agendar_sessao
# Abre janela para agendar uma nova sessão de reforço.
# Carrega alunos e professores do banco.db para o usuário
# selecionar via OptionMenu (igual ao padrão do main.py).
# -------------------------------------------------------

def agendar_sessao():

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
        """Recarrega listas de alunos e professores do banco."""

        for widget in frame_menus.winfo_children():
            widget.destroy()

        con = sqlite3.connect("banco.db")
        alunos = con.execute("SELECT id, nome FROM alunos").fetchall()
        professores = con.execute("SELECT id, nome, disciplina FROM professores").fetchall()
        con.close()

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

        data = entrada_data.get().strip()
        horario = entrada_horario.get().strip()

        if not data or not horario:
            messagebox.showerror("Erro", "Data e horário são obrigatórios.")
            return

        id_aluno = int(aluno_var.get().split(" - ")[0])
        id_professor = int(prof_var.get().split(" - ")[0])

        con = sqlite3.connect("banco.db")
        cur = con.cursor()

        nome_aluno = cur.execute(
            "SELECT nome FROM alunos WHERE id = ?", (id_aluno,)
        ).fetchone()[0]

        prof = cur.execute(
            "SELECT nome, disciplina FROM professores WHERE id = ?", (id_professor,)
        ).fetchone()

        nome_professor = prof[0]
        disciplina = prof[1]

        cur.execute("""
            INSERT INTO sessoes
            (id_aluno, nome_aluno, id_professor, nome_professor, disciplina, data, horario, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (id_aluno, nome_aluno, id_professor, nome_professor, disciplina, data, horario, "agendada"))

        con.commit()
        con.close()

        messagebox.showinfo(
            "Sucesso",
            f"Sessão agendada!\n{nome_aluno} com {nome_professor}\n{data} às {horario}"
        )
        janela.destroy()

    tk.Button(janela, text="Agendar", command=salvar, width=15).pack(pady=12)


# -------------------------------------------------------
# FUNÇÃO 2 — listar_sessoes
# Exibe todas as sessões em uma janela com barra de rolagem.
# Mesmo padrão de listar_alunos() e listar_professores().
# -------------------------------------------------------

def listar_sessoes():

    janela = tk.Toplevel()
    janela.title("Lista de Sessões")
    janela.geometry("440x370")

    tk.Label(janela, text="Lista de Sessões", font=("Arial", 14, "bold")).pack(pady=10)

    barra = tk.Scrollbar(janela)
    barra.pack(side=tk.RIGHT, fill=tk.Y)

    caixa = tk.Text(janela, yscrollcommand=barra.set, width=52, height=20)
    caixa.pack(padx=10)
    barra.config(command=caixa.yview)

    con = sqlite3.connect("banco.db")
    sessoes = con.execute("SELECT * FROM sessoes ORDER BY data, horario").fetchall()
    con.close()

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


# -------------------------------------------------------
# FUNÇÃO 3 — atualizar_sessao
# Permite alterar data, horário e status de uma sessão
# pelo seu ID. Campos em branco mantêm o valor atual.
# -------------------------------------------------------

def atualizar_sessao():

    janela = tk.Toplevel()
    janela.title("Atualizar Sessão")
    janela.geometry("350x300")
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

        con = sqlite3.connect("banco.db")
        cur = con.cursor()

        sessao = cur.execute(
            "SELECT * FROM sessoes WHERE id = ?", (id_busca,)
        ).fetchone()

        if sessao is None:
            con.close()
            messagebox.showerror("Erro", "Sessão não encontrada.")
            return

        # Mantém valor atual se o campo ficou em branco
        nova_data = entrada_data.get().strip() or sessao[6]
        novo_horario = entrada_horario.get().strip() or sessao[7]
        novo_status = status_var.get()

        cur.execute(
            "UPDATE sessoes SET data = ?, horario = ?, status = ? WHERE id = ?",
            (nova_data, novo_horario, novo_status, id_busca)
        )
        con.commit()
        con.close()

        messagebox.showinfo("Sucesso", "Sessão atualizada com sucesso!")
        janela.destroy()

    tk.Button(janela, text="Atualizar", command=atualizar, width=15).pack(pady=10)


# -------------------------------------------------------
# FUNÇÃO 4 — cancelar_sessao
# Remove uma sessão pelo ID, com confirmação.
# Mesmo padrão de remover_aluno() e remover_professor().
# -------------------------------------------------------

def cancelar_sessao():

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

        con = sqlite3.connect("banco.db")
        cur = con.cursor()

        sessao = cur.execute(
            "SELECT * FROM sessoes WHERE id = ?", (id_busca,)
        ).fetchone()

        if sessao is None:
            con.close()
            messagebox.showerror("Erro", "Sessão não encontrada.")
            return

        confirmacao = messagebox.askyesno(
            "Confirmar",
            f"Deseja cancelar a sessão de '{sessao[2]}' em {sessao[6]}?"
        )

        if confirmacao:
            cur.execute("DELETE FROM sessoes WHERE id = ?", (id_busca,))
            con.commit()
            messagebox.showinfo("Sucesso", "Sessão cancelada e removida!")
            janela.destroy()

        con.close()

    tk.Button(janela, text="Cancelar Sessão", command=cancelar, width=18).pack(pady=12)
