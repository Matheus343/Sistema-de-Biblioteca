import tkinter as tk
from tkinter import messagebox

class TelaReservaLivro:
    def __init__(self, master, cliente, sistema) -> None:
        self.master = master
        self.master.title("Reservar Livro")
        self.master.geometry("600x700")
        self.master.configure(bg="#f5f5f5")

        self.cliente = cliente
        self.sistema = sistema

        # Frame centralizado com bordas arredondadas
        self.frame = tk.Canvas(master, bg="#ffffff", highlightthickness=0)
        self.frame.place(relx=0.5, rely=0.5, anchor="center", width=500, height=400)
        self.create_rounded_rectangle(self.frame, 0, 0, 500, 400, radius=20, fill="#ffffff", outline="#cccccc")

        # Título da tela
        tk.Label(self.frame, text="Reservar Livro", font=("Helvetica", 20, "bold"), fg="#333333", bg="#ffffff").place(relx=0.5, rely=0.1, anchor="center")

        # Campo Título do Livro
        self.create_input(self.frame, "Título do Livro", 0.3)
        self.titulo_entry = self.create_entry(self.frame, 0.4)

        # Botão de Reservar
        self.create_button(self.frame, "Confirmar Reserva", 0.6, self.confirmar_reserva)

        # Botão de Voltar
        self.create_button(self.frame, "Voltar", 0.75, self.voltar)

    def create_rounded_rectangle(self, canvas, x1, y1, x2, y2, radius=25, **kwargs) -> None:
        points = [x1+radius, y1, x2-radius, y1, x2, y1, x2, y1+radius,
                  x2, y2-radius, x2, y2, x2-radius, y2, x1+radius, y2,
                  x1, y2, x1, y2-radius, x1, y1+radius, x1, y1]
        return canvas.create_polygon(points, **kwargs, smooth=True)

    def create_input(self, parent, text, rely) -> None:
        tk.Label(parent, text=text, font=("Helvetica", 12), bg="#ffffff", fg="#555555").place(relx=0.1, rely=rely, anchor="w")

    def create_entry(self, parent, rely) -> None:
        entry = tk.Entry(parent, font=("Helvetica", 12), relief="flat", bg="#eeeeee")
        entry.place(relx=0.1, rely=rely, width=350, height=30)
        return entry

    def create_button(self, parent, text, rely, command) -> None:
        button = tk.Button(parent, text=text, font=("Helvetica", 12), bg="#4CAF50", fg="#ffffff",
                           activebackground="#45a049", activeforeground="#ffffff", relief="flat", command=command)
        button.place(relx=0.5, rely=rely, anchor="center", width=250, height=40)

    def confirmar_reserva(self) -> None:
        titulo = self.titulo_entry.get().strip()
        if not titulo:
            messagebox.showerror("Erro", "Informe o título do livro.")
            return

        resultado = self.sistema.reservar_livro(self.cliente["matricula"], titulo)
        if "sucesso" in resultado.lower():
            messagebox.showinfo("Sucesso", resultado)
        else:
            messagebox.showerror("Erro", resultado)

    def voltar(self) -> None:
        from src.interface.painel_cliente import PainelCliente
        self.master.destroy()
        root = tk.Tk()
        PainelCliente(root, self.cliente)
