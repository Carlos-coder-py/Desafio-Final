import tkinter as tk
from tkinter import messagebox, Toplevel, scrolledtext
import funcoes1 as fn
import funcoes_estatistica as fnes
from log_config import get_logger  # Importa o logger modularizado

# 1. Obter o logger específico para este módulo
logger = get_logger('GUI.Interface')

USUARIOS = {}


class Aplicacao(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Controle Financeiro")
        self.geometry("450x400")

        logger.info("Aplicação iniciada.")

        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (TelaLogin, TelaCadastro, TelaSistema):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("TelaLogin")

    def show_frame(self, page_name):
        logger.info(f"Navegando para a tela: {page_name}")
        frame = self.frames[page_name]
        frame.tkraise()

    def verificar_login(self, usuario, senha):
        if not USUARIOS:
            logger.warning("Tentativa de login sem usuários cadastrados.")
            messagebox.showwarning("Atenção",
                                   "Nenhum usuário cadastrado. Por favor, use o botão 'Criar Conta' para cadastrar o primeiro usuário.")
            return False

        if usuario in USUARIOS and USUARIOS[usuario] == senha:
            logger.info(f"Login bem-sucedido para o usuário: {usuario}")
            messagebox.showinfo("Login", "Login bem-sucedido!")
            self.show_frame("TelaSistema")
            return True
        else:
            logger.error(f"Falha de login: Usuário '{usuario}' ou senha incorretos.")
            messagebox.showerror("Erro de Login", "Nome de usuário ou senha incorretos.")
            return False

    def adicionar_usuario(self, usuario, senha):
        if not usuario or not senha:
            logger.error("Tentativa de cadastro com campos vazios.")
            messagebox.showerror("Erro de Cadastro", "Nome de usuário e senha não podem ser vazios.")
            return False

        if usuario in USUARIOS:
            logger.warning(f"Tentativa de cadastro de usuário já existente: {usuario}")
            messagebox.showerror("Erro de Cadastro", "Nome de usuário já existe.")
            return False

        USUARIOS[usuario] = senha
        logger.info(f"Novo usuário cadastrado: {usuario}")
        messagebox.showinfo("Cadastro", f"Usuário '{usuario}' cadastrado com sucesso!")
        self.show_frame("TelaLogin")
        return True


class TelaLogin(tk.Frame):
    def __init__(self, parent, controller):
        # CORREÇÃO TKINTER
        super().__init__(parent)
        self.controller = controller

        center_frame = tk.Frame(self)
        center_frame.place(relx=0.5, rely=0.5, anchor='center')

        label_titulo = tk.Label(center_frame, text="Login", font=("Arial", 16, "bold"))
        label_titulo.pack(pady=20)

        label_usuario = tk.Label(center_frame, text="Nome:")
        label_usuario.pack(pady=2)
        self.entrada_usuario = tk.Entry(center_frame, width=30, justify='center')
        self.entrada_usuario.pack(pady=2)

        label_senha = tk.Label(center_frame, text="Senha:")
        label_senha.pack(pady=2)
        self.entrada_senha = tk.Entry(center_frame, width=30, show="*", justify='center')
        self.entrada_senha.pack(pady=2)

        botao_entrar = tk.Button(
            center_frame,
            text="Entrar",
            command=self.acao_login,
            width=20
        )
        botao_entrar.pack(pady=10)

        botao_cadastrar = tk.Button(
            center_frame,
            text="Criar Conta (Cadastrar)",
            command=lambda: self.controller.show_frame("TelaCadastro"),
            width=20
        )
        botao_cadastrar.pack(pady=5)

    def acao_login(self):
        usuario = self.entrada_usuario.get()
        senha = self.entrada_senha.get()
        self.controller.verificar_login(usuario, senha)


class TelaCadastro(tk.Frame):
    def __init__(self, parent, controller):
        # CORREÇÃO TKINTER
        super().__init__(parent)
        self.controller = controller

        center_frame = tk.Frame(self)
        center_frame.place(relx=0.5, rely=0.5, anchor='center')

        label_titulo = tk.Label(center_frame, text="Cadastro de Usuário", font=("Arial", 16, "bold"))
        label_titulo.pack(pady=20)

        label_usuario = tk.Label(center_frame, text="Nome de Usuário:")
        label_usuario.pack(pady=2)
        self.entrada_usuario = tk.Entry(center_frame, width=30, justify='center')
        self.entrada_usuario.pack(pady=2)

        label_senha = tk.Label(center_frame, text="Senha:")
        label_senha.pack(pady=2)
        self.entrada_senha = tk.Entry(center_frame, width=30, show="*", justify='center')
        self.entrada_senha.pack(pady=2)

        botao_registrar = tk.Button(
            center_frame,
            text="Registrar",
            command=self.acao_cadastro,
            width=25
        )
        botao_registrar.pack(pady=10)

    def acao_cadastro(self):
        usuario = self.entrada_usuario.get()
        senha = self.entrada_senha.get()
        if self.controller.adicionar_usuario(usuario, senha):
            self.entrada_usuario.delete(0, tk.END)
            self.entrada_senha.delete(0, tk.END)


# Pop-up para Adicionar Transação
class AdicionarTransacaoPopup(Toplevel):
    def __init__(self, parent):
        # CORREÇÃO TKINTER
        super().__init__(parent)
        self.title("Adicionar Nova Transação")
        self.geometry("300x350")
        self.transient(parent)
        self.grab_set()

        # Variáveis de controle
        self.data_var = tk.StringVar()
        self.tipo_var = tk.StringVar(value="entrada")
        self.categoria_var = tk.StringVar()
        self.descricao_var = tk.StringVar()
        self.valor_var = tk.StringVar()

        # Data
        tk.Label(self, text="Data (dd/mm/aaaa):").pack(pady=5)
        tk.Entry(self, textvariable=self.data_var, width=20).pack(pady=2)

        # Tipo
        tk.Label(self, text="Tipo:").pack(pady=5)
        tk.Radiobutton(self, text="Entrada", variable=self.tipo_var, value="entrada").pack()
        tk.Radiobutton(self, text="Saída", variable=self.tipo_var, value="saida").pack()

        # Categoria
        tk.Label(self, text="Categoria:").pack(pady=5)
        tk.Entry(self, textvariable=self.categoria_var, width=20).pack(pady=2)

        # Descrição
        tk.Label(self, text="Descrição:").pack(pady=5)
        tk.Entry(self, textvariable=self.descricao_var, width=20).pack(pady=2)

        # Valor
        tk.Label(self, text="Valor:").pack(pady=5)
        tk.Entry(self, textvariable=self.valor_var, width=20).pack(pady=2)

        # Botão Salvar
        tk.Button(self, text="Salvar", command=self.salvar).pack(pady=15)

    def salvar(self):
        resultado = fn.adicionar_transacao(
            self.data_var.get(),
            self.tipo_var.get(),
            self.categoria_var.get(),
            self.descricao_var.get(),
            self.valor_var.get()
        )

        if resultado.startswith("Erro"):
            logger.error(f"Falha ao salvar transação. Detalhe: {resultado}")
            messagebox.showerror("Erro ao Salvar", resultado)
        else:
            logger.info(f"Transação salva com sucesso: {self.tipo_var.get()} | {self.valor_var.get()}")
            messagebox.showinfo("Sucesso", resultado)
            self.destroy()


# Pop-up para Listar Todas
class ListarTodasPopup(Toplevel):
    def __init__(self, parent):
        # CORREÇÃO TKINTER
        super().__init__(parent)
        self.title("Todas as Transações")
        self.geometry("600x400")
        logger.info("Listagem de todas as transações solicitada.")

        resultado = fn.listar_todas()

        text_area = scrolledtext.ScrolledText(self, wrap=tk.WORD, width=70, height=20)
        text_area.insert(tk.INSERT, resultado)
        text_area.config(state=tk.DISABLED)
        text_area.pack(pady=10, padx=10)


# Pop-up para Remover Transação
class RemoverTransacaoPopup(Toplevel):
    def __init__(self, parent):
        # CORREÇÃO TKINTER
        super().__init__(parent)
        self.title("🗑Remover Transação")
        self.geometry("450x300")
        self.transient(parent)
        self.grab_set()

        tk.Label(self, text="Transações Atuais:").pack(pady=5)

        lista_transacoes = scrolledtext.ScrolledText(self, wrap=tk.WORD, width=50, height=5)
        lista_transacoes.insert(tk.INSERT, fn.listar_todas())
        lista_transacoes.config(state=tk.DISABLED)
        lista_transacoes.pack(pady=5, padx=10)

        self.idx_var = tk.StringVar()
        tk.Label(self, text="Digite o NÚMERO (Índice) da transação para remover:").pack(pady=10)
        tk.Entry(self, textvariable=self.idx_var, width=10).pack(pady=2)

        tk.Button(self, text="Remover", command=self.remover).pack(pady=15)

    def remover(self):
        idx = self.idx_var.get()
        resultado = fn.remover_transacao(idx)

        if resultado.startswith("Erro"):
            logger.error(f"Falha ao remover transação (Índice: {idx}). Detalhe: {resultado}")
            messagebox.showerror("Erro ao Remover", resultado)
        else:
            logger.info(f"Transação de índice '{idx}' removida com sucesso.")
            messagebox.showinfo("Sucesso", resultado)
            self.destroy()


# Pop-up para Listar por Categoria
class ListarPorCategoriaPopup(Toplevel):
    def __init__(self, parent):
        # CORREÇÃO TKINTER
        super().__init__(parent)
        self.title("Listar por Categoria")
        self.geometry("400x350")
        self.transient(parent)
        self.grab_set()

        self.cat_var = tk.StringVar()

        tk.Label(self, text="Digite a Categoria Desejada:").pack(pady=10)
        tk.Entry(self, textvariable=self.cat_var, width=20).pack(pady=5)

        tk.Button(self, text="Buscar", command=self.buscar).pack(pady=10)

        self.resultado_area = scrolledtext.ScrolledText(self, wrap=tk.WORD, width=45, height=10)
        self.resultado_area.pack(pady=5, padx=10)

    def buscar(self):
        categoria = self.cat_var.get()
        logger.info(f"Buscando transações pela categoria: {categoria}")
        resultado = fn.listar_por_categoria(categoria)

        self.resultado_area.config(state=tk.NORMAL)
        self.resultado_area.delete(1.0, tk.END)
        self.resultado_area.insert(tk.INSERT, resultado)
        self.resultado_area.config(state=tk.DISABLED)


# Pop-up para Listar por Período e Saldo
class ListarPorPeriodoPopup(Toplevel):
    def __init__(self, parent, modo="listar"):
        # CORREÇÃO TKINTER
        super().__init__(parent)
        self.modo = modo
        if modo == "listar":
            self.title("Listar por Período")
        else:
            self.title("Saldo por Período")

        self.geometry("400x350")
        self.transient(parent)
        self.grab_set()

        self.inicio_var = tk.StringVar()
        self.fim_var = tk.StringVar()

        tk.Label(self, text="Data de Início (dd/mm/aaaa):").pack(pady=5)
        tk.Entry(self, textvariable=self.inicio_var, width=20).pack(pady=2)

        tk.Label(self, text="Data Final (dd/mm/aaaa):").pack(pady=5)
        tk.Entry(self, textvariable=self.fim_var, width=20).pack(pady=2)

        tk.Button(self, text="Processar", command=self.processar).pack(pady=10)

        self.resultado_area = scrolledtext.ScrolledText(self, wrap=tk.WORD, width=45, height=10)
        self.resultado_area.pack(pady=5, padx=10)

    def processar(self):
        inicio = self.inicio_var.get()
        fim = self.fim_var.get()

        if self.modo == "listar":
            logger.info(f"Listando transações no período: {inicio} a {fim}")
            resultado = fn.listar_por_periodo(inicio, fim)
        else:
            logger.info(f"Calculando saldo no período: {inicio} a {fim}")
            resultado = fn.saldo_por_periodo(inicio, fim)

        self.resultado_area.config(state=tk.NORMAL)
        self.resultado_area.delete(1.0, tk.END)
        self.resultado_area.insert(tk.INSERT, resultado)
        self.resultado_area.config(state=tk.DISABLED)


# Pop-up para Estatísticas e Gráficos
class PopupEstatisticas(Toplevel):
    def __init__(self, parent):
        # CORREÇÃO TKINTER
        super().__init__(parent)
        self.title("Estatísticas e Gráficos")
        self.geometry("450x400")
        self.transient(parent)
        self.grab_set()

        # Variáveis de controle para o período
        self.inicio_var = tk.StringVar()
        self.fim_var = tk.StringVar()

        tk.Label(self, text="Estatísticas por Período:", font=("Arial", 12, "bold")).pack(pady=5)

        # Entrada de Período
        frame_periodo = tk.Frame(self)
        frame_periodo.pack(pady=5)

        tk.Label(frame_periodo, text="Início (dd/mm/aaaa):").pack(side=tk.LEFT, padx=5)
        tk.Entry(frame_periodo, textvariable=self.inicio_var, width=15).pack(side=tk.LEFT, padx=5)

        tk.Label(frame_periodo, text="Fim (dd/mm/aaaa):").pack(side=tk.LEFT, padx=5)
        tk.Entry(frame_periodo, textvariable=self.fim_var, width=15).pack(side=tk.LEFT, padx=5)

        tk.Button(self, text="Calcular Receitas/Despesas do Período", command=self.mostrar_estatisticas_periodo).pack(
            pady=5)

        tk.Button(self, text="Média de Gastos por Categoria", command=self.mostrar_media_gastos).pack(pady=5)

        tk.Button(self, text="Gerar Gráfico de Pizza (Gastos)", command=self.gerar_grafico).pack(pady=10)

        # Área para exibir resultados de texto
        tk.Label(self, text="Resultados:", font=("Arial", 10, "italic")).pack(pady=2)
        self.resultado_area = scrolledtext.ScrolledText(self, wrap=tk.WORD, width=50, height=8)
        self.resultado_area.pack(pady=5, padx=10)

    def atualizar_resultado_area(self, texto):
        self.resultado_area.config(state=tk.NORMAL)
        self.resultado_area.delete(1.0, tk.END)
        self.resultado_area.insert(tk.INSERT, texto)
        self.resultado_area.config(state=tk.DISABLED)

    def mostrar_estatisticas_periodo(self):
        inicio = self.inicio_var.get()
        fim = self.fim_var.get()
        logger.info(f"Solicitado cálculo de estatísticas para o período: {inicio} a {fim}")

        resultado, _, _ = fnes.calcular_estatisticas_periodo(inicio, fim)

        if resultado.startswith("Erro"):
            logger.error(f"Erro ao calcular estatísticas. Detalhe: {resultado.split(':')[1].strip()}")

        self.atualizar_resultado_area(resultado)

    def mostrar_media_gastos(self):
        logger.info("Solicitado cálculo da média de gastos por categoria.")
        resultado = fnes.calcular_media_gastos_por_categoria()
        self.atualizar_resultado_area(resultado)

    def gerar_grafico(self):
        logger.info("Solicitada geração de gráfico de pizza de gastos.")
        resultado = fnes.gerar_grafico_pizza_gastos()

        if resultado.startswith("Não há"):
            logger.warning("Gráfico não gerado: Não há despesas registradas.")
        else:
            logger.info("Gráfico gerado com sucesso.")

        self.atualizar_resultado_area(resultado)


# --- Tela Principal do Sistema ---
class TelaSistema(tk.Frame):
    def __init__(self, parent, controller):
        # CORREÇÃO TKINTER
        super().__init__(parent)
        self.controller = controller

        center_frame = tk.Frame(self)
        center_frame.place(relx=0.5, rely=0.5, anchor='center')

        label_titulo = tk.Label(center_frame, text="Sistema de Controle Financeiro", font=("Arial", 16, "bold"))
        label_titulo.pack(pady=10)

        PAD_X = 50

        btn_adicionar = tk.Button(center_frame, text="Adicionar Transação",
                                  command=lambda: AdicionarTransacaoPopup(self.master))
        btn_adicionar.pack(pady=5, padx=PAD_X, fill='x')

        btn_listar_todas = tk.Button(
            center_frame,
            text="Listar Todas",
            command=lambda: ListarTodasPopup(self.master)
        )
        btn_listar_todas.pack(pady=5, padx=PAD_X, fill='x')

        btn_por_categoria = tk.Button(center_frame, text="Listar por Categoria",
                                      command=lambda: ListarPorCategoriaPopup(self.master))
        btn_por_categoria.pack(pady=5, padx=PAD_X, fill='x')

        btn_por_periodo = tk.Button(center_frame, text="Listar por Período",
                                    command=lambda: ListarPorPeriodoPopup(self.master, modo="listar"))
        btn_por_periodo.pack(pady=5, padx=PAD_X, fill='x')

        btn_saldo = tk.Button(center_frame, text="Saldo por Período",
                              command=lambda: ListarPorPeriodoPopup(self.master, modo="saldo"))
        btn_saldo.pack(pady=5, padx=PAD_X, fill='x')

        # Botão de Estatistica
        btn_estatisticas = tk.Button(center_frame, text="Estatísticas e Gráficos",
                                     command=lambda: PopupEstatisticas(self.master))
        btn_estatisticas.pack(pady=5, padx=PAD_X, fill='x')

        btn_remover = tk.Button(center_frame, text="Remover Transação",
                                command=lambda: RemoverTransacaoPopup(self.master))
        btn_remover.pack(pady=5, padx=PAD_X, fill='x')

        btn_sair = tk.Button(center_frame, text="Sair / Logout", command=lambda: controller.show_frame("TelaLogin"))
        btn_sair.pack(pady=15, padx=PAD_X, fill='x')


def inicializar():
    app = Aplicacao()
    app.mainloop()


inicializar()