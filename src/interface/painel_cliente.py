import tkinter as tk
from src.interface.acervo import TelaAcervo  # Importa a tela de Acervo
from src.sistema import Sistema
from src.interface.pendencias import TelaPendencias
from src.interface.reserva_livro import TelaReservaLivro

class PainelCliente:
    def __init__(self, master, cliente) -> None:
        self.master = master
        self.master.title("Painel do Cliente")
        self.master.geometry("600x700")
        self.master.configure(bg="#f5f5f5")

        self.sistema = Sistema()
        self.cliente = cliente  

        # Frame centralizado com estilo
        self.frame = tk.Canvas(master, bg="#ffffff", highlightthickness=0)
        self.frame.place(relx=0.5, rely=0.5, anchor="center", width=500, height=600)
        self.create_rounded_rectangle(self.frame, 0, 0, 500, 600, radius=20, fill="#ffffff", outline="#cccccc")

        # Título
        tk.Label(self.frame, text=f"Bem-vindo, {cliente['nome']}!", font=("Helvetica", 18, "bold"), bg="#ffffff", fg="#333333").place(relx=0.5, rely=0.1, anchor="center")

        # Botões estilizados
        self.create_button(self.frame, "Visualizar Acervo", 0.25, self.abrir_acervo)
        self.create_button(self.frame, "Verificar Pendências", 0.35, self.visualizar_pendencias)
        self.create_button(self.frame, "Reservar Livro", 0.45, self.reservar_livro)
        self.create_button(self.frame, "Meus Livros Reservados", 0.55, self.meus_livros_reservados)
        self.create_button(self.frame, "Sair", 0.75, self.sair)

    def create_rounded_rectangle(self, canvas, x1, y1, x2, y2, radius=25, **kwargs) -> None:
        points = [x1+radius, y1,
                  x2-radius, y1, x2, y1, x2, y1+radius,
                  x2, y2-radius, x2, y2, x2-radius, y2,
                  x1+radius, y2, x1, y2, x1, y2-radius,
                  x1, y1+radius, x1, y1]
        return canvas.create_polygon(points, **kwargs, smooth=True)

    def create_button(self, parent, text, rely, command) -> None:
        button = tk.Button(parent, text=text, font=("Helvetica", 12), bg="#4CAF50", fg="#ffffff",
                           activebackground="#45a049", activeforeground="#ffffff", relief="flat", command=command)
        button.place(relx=0.5, rely=rely, anchor="center", width=250, height=40)

    def abrir_acervo(self) -> None:
        self.master.destroy()
        root = tk.Tk()
        TelaAcervo(root, self.cliente, self.sistema)  # Passa cliente e sistema


    def visualizar_pendencias(self) -> None:
        pendencias = self.sistema.listar_pendencias(self.cliente["matricula"])
        self.master.destroy()
        root = tk.Tk()
        TelaPendencias(root, self.cliente, pendencias)
        
    from src.interface.reserva_livro import TelaReservaLivro

    def reservar_livro(self) -> None:
        self.master.destroy()
        root = tk.Tk()
        self.TelaReservaLivro(root, self.cliente, self.sistema)

    def meus_livros_reservados(self) -> None:
        clientes = self.sistema.banco_clientes.carregar()
        self.cliente = next((c for c in clientes if c["matricula"] == self.cliente["matricula"]), self.cliente)

        livros_reservados = self.cliente.get("livros_reservados", [])
        if livros_reservados:
            livros_str = "\n".join([f"{livro['titulo']} - Devolver até: {livro['data_devolucao']}" for livro in livros_reservados])
            tk.messagebox.showinfo("Meus Livros Reservados", livros_str)
        else:
            tk.messagebox.showinfo("Meus Livros Reservados", "Você não reservou nenhum livro.")

    def sair(self) -> None:
        from src.interface.login import TelaLogin
        self.master.destroy()
        root = tk.Tk()
        TelaLogin(root)
