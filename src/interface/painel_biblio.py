import tkinter as tk
from tkinter import messagebox
from src.sistema import Sistema
from src.interface.cadastro import TelaCadastroLivro, TelaCadastro

class PainelBibliotecario:
    def __init__(self, master) -> None:
        self.master = master
        self.master.title("Painel do Bibliotecário")
        self.master.geometry("600x700")
        self.master.configure(bg="#f5f5f5")

        self.sistema = Sistema()

        # Frame centralizado com bordas arredondadas
        self.frame = tk.Canvas(master, bg="#ffffff", highlightthickness=0)
        self.frame.place(relx=0.5, rely=0.5, anchor="center", width=500, height=600)
        self.create_rounded_rectangle(self.frame, 0, 0, 500, 600, radius=20, fill="#ffffff", outline="#cccccc")

        # Título da tela
        tk.Label(self.frame, text="Painel do Bibliotecário", font=("Helvetica", 18, "bold"), fg="#333333", bg="#ffffff").place(relx=0.5, rely=0.05, anchor="center")

        # Seção Gerenciar Livros
        tk.Label(self.frame, text="Gerenciar Livros", font=("Helvetica", 12, "bold"), fg="#555555", bg="#ffffff").place(relx=0.5, rely=0.15, anchor="center")
        self.create_button(self.frame, "Cadastrar Livro", 0.22, self.cadastrar_livro)
        self.create_button(self.frame, "Listar Livros", 0.29, self.listar_livros)

        # Seção Gerenciar Clientes
        tk.Label(self.frame, text="Gerenciar Clientes", font=("Helvetica", 12, "bold"), fg="#555555", bg="#ffffff").place(relx=0.5, rely=0.38, anchor="center")
        self.create_button(self.frame, "Cadastrar Cliente", 0.45, self.cadastrar_cliente)
        self.create_button(self.frame, "Listar Clientes", 0.52, self.listar_clientes)

        # Gerenciar Pendências
        self.create_button(self.frame, "Gerenciar Pendências", 0.62, self.gerenciar_pendencias)

        # Botão de sair
        self.create_button(self.frame, "Sair", 0.80, self.sair)

    def create_rounded_rectangle(self, canvas, x1, y1, x2, y2, radius=25, **kwargs) -> None:
        points = [x1+radius, y1, x2-radius, y1, x2, y1, x2, y1+radius,
                  x2, y2-radius, x2, y2, x2-radius, y2, x1+radius, y2,
                  x1, y2, x1, y2-radius, x1, y1+radius, x1, y1]
        return canvas.create_polygon(points, **kwargs, smooth=True)

    def create_button(self, parent, text, rely, command) -> None:
        button = tk.Button(parent, text=text, font=("Helvetica", 12), bg="#4CAF50", fg="#ffffff",
                           activebackground="#45a049", activeforeground="#ffffff", relief="flat", command=command)
        button.place(relx=0.5, rely=rely, anchor="center", width=250, height=40)

    def cadastrar_livro(self) -> None:
        self.master.destroy()
        root = tk.Tk()
        TelaCadastroLivro(root)

    def listar_livros(self) -> None:
        livros = self.sistema.listar_livros()
        livros_str = "\n".join([f"{livro['titulo']} - {livro['autor']}" for livro in livros])
        messagebox.showinfo("Livros Cadastrados", livros_str or "Nenhum livro cadastrado.")

    def cadastrar_cliente(self) -> None:
        self.master.destroy()
        root = tk.Tk()
        TelaCadastro(root)

    def listar_clientes(self) -> None:
        clientes = self.sistema.listar_clientes()
        clientes_str = "\n".join([f"{cliente['nome']} - {cliente['matricula']}" for cliente in clientes])
        messagebox.showinfo("Clientes Cadastrados", clientes_str or "Nenhum cliente cadastrado.")

    def gerenciar_pendencias(self) -> None:
        pendencias_window = tk.Toplevel(self.master)
        pendencias_window.title("Gerenciar Pendências")
        pendencias_window.geometry("400x400")

        clientes = self.sistema.banco_clientes.carregar()
        for cliente in clientes:
            pendencias = self.sistema.listar_pendencias(cliente["matricula"])
            if pendencias:
                tk.Label(pendencias_window, text=f"Cliente: {cliente['nome']}", font=("Helvetica", 10, "bold")).pack(pady=5)
                for pendencia in pendencias:
                    tk.Label(pendencias_window, text=f"  {pendencia}", font=("Helvetica", 9)).pack()
                tk.Button(
                    pendencias_window,
                    text="Remover Pendências",
                    font=("Helvetica", 10),
                    command=lambda c=cliente: self.remover_pendencias(c)
                ).pack(pady=10)
            else:
                tk.Label(pendencias_window, text=f"Cliente: {cliente['nome']} (Sem pendências)").pack(pady=5)

    def remover_pendencias(self, cliente) -> None:
        for livro in cliente["livros_reservados"]:
            if "data_devolucao" in livro:
                livro["data_devolucao"] = None
        self.sistema.banco_clientes.salvar(self.sistema.banco_clientes.carregar())
        messagebox.showinfo("Sucesso", f"Pendências removidas para o cliente {cliente['nome']}.")

    def sair(self) -> None:
        from src.interface.login import TelaLogin
        self.master.destroy()
        root = tk.Tk()
        TelaLogin(root)
