import tkinter as tk
from tkinter import messagebox
from src.sistema import Sistema

class PainelCliente:
    def __init__(self, master, cliente):
        self.master = master
        self.master.title("Painel do Cliente")
        self.master.geometry("400x400")

        self.sistema = Sistema()
        self.cliente = cliente  
        tk.Label(master, text=f"Bem-vindo, {cliente['nome']}!", font=("Arial", 14)).pack(pady=10)

        tk.Button(master, text="Visualizar Acervo", command=self.visualizar_acervo).pack(pady=5)
        tk.Button(master, text="Verificar Pendências", command=self.visualizar_pendencias).pack(pady=5)
        tk.Button(master, text="Reservar Livro", command=self.reservar_livro).pack(pady=5)
        tk.Button(master, text="Meus Livros Reservados", command=self.meus_livros_reservados).pack(pady=5)
        tk.Button(master, text="Sair", command=self.sair).pack(pady=5)

    def visualizar_acervo(self):
        livros = self.sistema.listar_livros()
        livros_disponiveis = [f"{livro['titulo']} - {livro['autor']}" for livro in livros if livro["disponibilidade"]]
        if livros_disponiveis:
            livros_str = "\n".join(livros_disponiveis)
            messagebox.showinfo("Livros Disponíveis", livros_str)
        else:
            messagebox.showinfo("Livros Disponíveis", "Nenhum livro disponível no momento.")

    def visualizar_pendencias(self):
        pendencias = self.sistema.listar_pendencias(self.cliente["matricula"])
        if pendencias:
            pendencias_str = "\n".join(pendencias)
            messagebox.showinfo("Pendências", pendencias_str)
        else:
            messagebox.showinfo("Pendências", "Nenhuma pendência encontrada.")

    def reservar_livro(self):
        reserva_window = tk.Toplevel(self.master)
        reserva_window.title("Reservar Livro")
        reserva_window.geometry("300x200")

        tk.Label(reserva_window, text="Título do Livro").pack(pady=5)
        titulo_entry = tk.Entry(reserva_window)
        titulo_entry.pack(pady=5)

        def confirmar_reserva():
            titulo = titulo_entry.get().strip()
            if not titulo:
                messagebox.showerror("Erro", "Informe o título do livro.")
                return

            resultado = self.sistema.reservar_livro(self.cliente["matricula"], titulo)
            if "já reservou" in resultado:
                messagebox.showerror("Erro", resultado)
            elif "reservado com sucesso" in resultado:
                messagebox.showinfo("Sucesso", resultado)
            else:
                messagebox.showinfo("Informação", resultado)
            reserva_window.destroy()

        tk.Button(reserva_window, text="Confirmar Reserva", command=confirmar_reserva).pack(pady=10)

    def meus_livros_reservados(self):
        clientes = self.sistema.banco_clientes.carregar()
        self.cliente = next((c for c in clientes if c["matricula"] == self.cliente["matricula"]), self.cliente)

        livros_reservados = self.cliente.get("livros_reservados", [])
        if livros_reservados:
            livros_str = "\n".join([f"{livro['titulo']} - Devolver até: {livro['data_devolucao']}" for livro in livros_reservados])
            messagebox.showinfo("Meus Livros Reservados", livros_str)
        else:
            messagebox.showinfo("Meus Livros Reservados", "Você não reservou nenhum livro.")

    def sair(self):
        from src.interface.login import TelaLogin
        self.master.destroy()
        root = tk.Tk()
        TelaLogin(root)
    