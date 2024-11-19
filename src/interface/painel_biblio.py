import tkinter as tk
from tkinter import messagebox
from src.sistema import Sistema

class PainelBibliotecario:
    def __init__(self, master):
        self.master = master
        self.master.title("Painel do Bibliotecário")
        self.master.geometry("400x400")

        tk.Label(master, text="Gerenciar Livros").pack(pady=10)
        tk.Button(master, text="Cadastrar Livro", command=self.cadastrar_livro).pack(pady=5)
        tk.Button(master, text="Listar Livros", command=self.listar_livros).pack(pady=5)

        tk.Label(master, text="Gerenciar Clientes").pack(pady=10)
        tk.Button(master, text="Cadastrar Cliente", command=self.cadastrar_cliente).pack(pady=5)
        tk.Button(master, text="Listar Clientes", command=self.listar_clientes).pack(pady=5)
        tk.Button(master, text="Gerenciar Pendências", command=self.gerenciar_pendencias).pack(pady=5)

        self.sistema = Sistema()

    def cadastrar_livro(self):
        from src.interface.cadastro import TelaCadastroLivro
        self.master.destroy()
        root = tk.Tk()
        TelaCadastroLivro(root)

    def listar_livros(self):
        livros = self.sistema.listar_livros()
        livros_str = "\n".join([f"{livro['titulo']} - {livro['autor']}" for livro in livros])
        messagebox.showinfo("Livros Cadastrados", livros_str or "Nenhum livro cadastrado.")

    def cadastrar_cliente(self):
        from src.interface.cadastro import TelaCadastro
        self.master.destroy()
        root = tk.Tk()
        TelaCadastro(root)

    def listar_clientes(self):
        clientes = self.sistema.listar_clientes()
        clientes_str = "\n".join([f"{cliente['nome']} - {cliente['matricula']}" for cliente in clientes])
        messagebox.showinfo("Clientes Cadastrados", clientes_str or "Nenhum cliente cadastrado.")

    def gerenciar_pendencias(self):
        pendencias_window = tk.Toplevel(self.master)
        pendencias_window.title("Gerenciar Pendências")
        pendencias_window.geometry("400x400")

        clientes = self.sistema.banco_clientes.carregar()
        for cliente in clientes:
            pendencias = self.sistema.listar_pendencias(cliente["matricula"])
            if pendencias:
                tk.Label(pendencias_window, text=f"Cliente: {cliente['nome']}").pack(pady=5)
                for pendencia in pendencias:
                    tk.Label(pendencias_window, text=f"  {pendencia}").pack()
                tk.Button(
                    pendencias_window,
                    text="Remover Pendências",
                    command=lambda c=cliente: self.remover_pendencias(c)
                ).pack(pady=10)
            else:
                tk.Label(pendencias_window, text=f"Cliente: {cliente['nome']} (Sem pendências)").pack(pady=5)

    def remover_pendencias(self, cliente):
        for livro in cliente["livros_reservados"]:
            if "data_devolucao" in livro:
                livro["data_devolucao"] = None
        self.sistema.banco_clientes.salvar(self.sistema.banco_clientes.carregar())
        messagebox.showinfo("Sucesso", f"Pendências removidas para o cliente {cliente['nome']}.")
