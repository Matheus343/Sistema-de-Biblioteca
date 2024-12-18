import tkinter as tk
from tkinter import ttk
from src.sistema import Sistema

# UI de visualização do acervo da biblioteca
class TelaAcervoAnonimo:
    def __init__(self, master) -> None:
        self.master = master
        self.master.title("Acervo da Biblioteca")
        self.master.geometry("600x700")  # Tela maior verticalmente
        self.master.configure(bg="#f5f5f5")

        # Sistema e dados
        self.sistema = Sistema()
        self.livros = self.sistema.listar_livros()

        # Frame centralizado com bordas arredondadas
        self.frame = tk.Canvas(master, bg="#ffffff", highlightthickness=0)
        self.frame.place(relx=0.5, rely=0.5, anchor="center", width=500, height=600)
        self.create_rounded_rectangle(self.frame, 0, 0, 500, 600, radius=20, fill="#ffffff", outline="#cccccc")

        # Título da tela
        tk.Label(self.frame, text="Acervo da Biblioteca", font=("Helvetica", 20, "bold"), fg="#333333", bg="#ffffff").place(relx=0.5, rely=0.05, anchor="center")

        # Cria uma lista para exibir os livros
        self.lista_livros = tk.Listbox(self.frame, font=("Helvetica", 10), bg="#f0f0f0", fg="#333333", relief="flat")
        self.lista_livros.place(relx=0.5, rely=0.5, anchor="center", width=400, height=400)

        # Carregar os livros no Listbox
        self.carregar_livros()

        # Botão de voltar
        self.create_button(self.frame, "Voltar", 0.9, self.voltar)

    def carregar_livros(self) -> None:
        self.lista_livros.delete(0, tk.END)
        for livro in self.livros:
            status = "Disponível" if livro["disponibilidade"] else "Indisponível"
            self.lista_livros.insert(tk.END, f"{livro['titulo']} - {livro['autor']} ({status})")

    def create_rounded_rectangle(self, canvas, x1, y1, x2, y2, radius=25, **kwargs) -> None:
        points = [x1+radius, y1,
                  x1+radius, y1,
                  x2-radius, y1,
                  x2-radius, y1,
                  x2, y1,
                  x2, y1+radius,
                  x2, y2-radius,
                  x2, y2-radius,
                  x2, y2,
                  x2-radius, y2,
                  x1+radius, y2,
                  x1+radius, y2,
                  x1, y2,
                  x1, y2-radius,
                  x1, y1+radius,
                  x1, y1+radius,
                  x1, y1]
        return canvas.create_polygon(points, **kwargs, smooth=True)

    def create_button(self, parent, text, rely, command) -> None:
        button = tk.Button(parent, text=text, font=("Helvetica", 10), bg="#4CAF50", fg="#ffffff",
                           activebackground="#45a049", activeforeground="#ffffff", relief="flat", command=command)
        button.place(relx=0.5, rely=rely, anchor="center", width=250, height=40)

    def voltar(self) -> None:
        from src.interface.login import TelaLogin
        self.master.destroy()
        root = tk.Tk()
        TelaLogin(root)  # Passa o cliente para a tela de cliente

if __name__ == "__main__":
    root = tk.Tk()
    app = TelaAcervo(root)
    root.mainloop()
