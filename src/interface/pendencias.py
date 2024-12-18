import tkinter as tk
from tkinter import messagebox

class TelaPendencias:
    def __init__(self, master, cliente, pendencias) -> None:
        self.master = master
        self.master.title("Pendências")
        self.master.geometry("600x700")
        self.master.configure(bg="#f5f5f5")
        self.cliente = cliente

        # Frame centralizado com bordas arredondadas
        self.frame = tk.Canvas(master, bg="#ffffff", highlightthickness=0)
        self.frame.place(relx=0.5, rely=0.5, anchor="center", width=500, height=600)
        self.create_rounded_rectangle(self.frame, 0, 0, 500, 600, radius=20, fill="#ffffff", outline="#cccccc")

        # Título da tela
        tk.Label(self.frame, text="Pendências", font=("Helvetica", 20, "bold"), fg="#333333", bg="#ffffff").place(relx=0.5, rely=0.05, anchor="center")

        # Subtítulo com nome do cliente
        tk.Label(self.frame, text=f"Cliente: {cliente['nome']}", font=("Helvetica", 12), fg="#555555", bg="#ffffff").place(relx=0.5, rely=0.12, anchor="center")

        # Área de Lista
        self.lista_pendencias = tk.Listbox(self.frame, font=("Helvetica", 10), bg="#f0f0f0", fg="#333333", relief="flat", selectbackground="#4CAF50")
        self.lista_pendencias.place(relx=0.5, rely=0.5, anchor="center", width=400, height=400)

        # Preencher pendências
        if pendencias:
            for pendencia in pendencias:
                self.lista_pendencias.insert(tk.END, pendencia)
        else:
            self.lista_pendencias.insert(tk.END, "Nenhuma pendência encontrada.")

        # Botão de voltar
        self.create_button(self.frame, "Voltar", 0.9, self.voltar)

    def create_rounded_rectangle(self, canvas, x1, y1, x2, y2, radius=25, **kwargs) -> None:
        points = [x1+radius, y1, x2-radius, y1, x2, y1, x2, y1+radius,
                  x2, y2-radius, x2, y2, x2-radius, y2, x1+radius, y2,
                  x1, y2, x1, y2-radius, x1, y1+radius, x1, y1]
        return canvas.create_polygon(points, **kwargs, smooth=True)

    def create_button(self, parent, text, rely, command) -> None:
        button = tk.Button(parent, text=text, font=("Helvetica", 12), bg="#4CAF50", fg="#ffffff",
                           activebackground="#45a049", activeforeground="#ffffff", relief="flat", command=command)
        button.place(relx=0.5, rely=rely, anchor="center", width=200, height=40)

    def voltar(self) -> None:
        from src.interface.painel_cliente import PainelCliente
        self.master.destroy()
        root = tk.Tk()
        PainelCliente(root, self.cliente)  # Passa o cliente para a tela de cliente

