import tkinter as tk
from tkinter import ttk
from src.interface.login import TelaLogin

class TelaInicial:
    def __init__(self, master) -> None:
        self.master = master
        self.master.title("Sistema de Gerenciamento para Bibliotecas")
        self.master.geometry("800x600")
        self.master.configure(bg="#f5f5f5")

        # Frame centralizado com bordas arredondadas
        frame = tk.Canvas(master, bg="#ffffff", highlightthickness=0)
        frame.place(relx=0.5, rely=0.5, anchor="center", width=600, height=400)
        frame.create_rounded_rectangle = self.create_rounded_rectangle(frame, 0, 0, 600, 400, radius=30, fill="#ffffff", outline="#000000")

        # Título no centro
        titulo = tk.Label(frame, text="Sistema de Gerenciamento para Bibliotecas",
                          font=("Helvetica", 20, "bold"), fg="#333333", bg="#ffffff")
        titulo.place(relx=0.5, rely=0.3, anchor="center")

        # Botão "Começar" com cor verde e bordas arredondadas
        btn_comecar = tk.Button(frame, text="Começar", font=("Helvetica", 12), bg="#4CAF50", fg="#ffffff",
                                activebackground="#45a049", activeforeground="#ffffff",
                                relief="flat", bd=0, command=self.ir_para_login)
        btn_comecar.place(relx=0.5, rely=0.6, anchor="center", width=150, height=40)

        # Adiciona comportamento de hover
        btn_comecar.bind("<Enter>", lambda e: btn_comecar.config(bg="#45a049"))
        btn_comecar.bind("<Leave>", lambda e: btn_comecar.config(bg="#4CAF50"))

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

    def ir_para_login(self) -> None:
        self.master.destroy()
        root = tk.Tk()
        TelaLogin(root)

# Teste direto da tela inicial
if __name__ == "__main__":
    root = tk.Tk()
    app = TelaInicial(root)
    root.mainloop()
