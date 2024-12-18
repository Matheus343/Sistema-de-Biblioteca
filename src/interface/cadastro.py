import tkinter as tk
from tkinter import messagebox
from src.sistema import Sistema
import re

# UI para tela de cadastro, aqui os usuários são cadastrados no geral, tanto clientes como bibliotecários
# possui validação de CPF e matrícula

class TelaCadastro:
    def __init__(self, master) -> None:
        self.master = master
        self.master.title("Cadastro")
        self.master.geometry("600x900")
        self.master.configure(bg="#f5f5f5")

        # Frame centralizado com bordas arredondadas
        self.frame = tk.Canvas(master, bg="#ffffff", highlightthickness=0)
        self.frame.place(relx=0.5, rely=0.5, anchor="center", width=500, height=650)
        self.create_rounded_rectangle(self.frame, 0, 0, 500, 650, radius=20, fill="#ffffff", outline="#cccccc")

        # Título da tela
        tk.Label(self.frame, text="Cadastro", font=("Helvetica", 20, "bold"), fg="#333333", bg="#ffffff").place(relx=0.5, rely=0.05, anchor="center")

        # Campos de entrada organizados
        self.create_input(self.frame, "Nome", 0.1)
        self.nome = self.create_entry(self.frame, 0.14)

        self.create_input(self.frame, "Matrícula", 0.2)
        self.matricula = self.create_entry(self.frame, 0.24)

        self.create_input(self.frame, "Senha", 0.3)
        self.senha = self.create_entry(self.frame, 0.34, show="*")

        self.create_input(self.frame, "Escolha a Pergunta de Segurança", 0.4)
        self.pergunta_seguranca = tk.StringVar()
        perguntas = [
            "Qual sua cor favorita?",
            "Qual o nome do seu animal de estimação?",
            "Qual o nome da professora do primeiro ano do fundamental?",
            "Qual sua comida favorita?"
        ]
        self.pergunta_seguranca_menu = tk.OptionMenu(self.frame, self.pergunta_seguranca, *perguntas)
        self.pergunta_seguranca_menu.config(font=("Helvetica", 10), bg="#eeeeee", relief="flat")
        self.pergunta_seguranca_menu.place(relx=0.1, rely=0.44, width=350, height=30)

        self.create_input(self.frame, "Resposta à Pergunta", 0.5)
        self.resposta_seguranca = self.create_entry(self.frame, 0.54)

        self.create_input(self.frame, "CPF (Formato: xxx.xxx.xxx-xx)", 0.6)
        self.cpf = self.create_entry(self.frame, 0.64)

        # Tipo de Cadastro (Radio Buttons)
        tk.Label(self.frame, text="Tipo de Cadastro", font=("Helvetica", 10), bg="#ffffff", fg="#555555").place(relx=0.1, rely=0.7, anchor="w")
        self.tipo = tk.StringVar(value="cliente")
        tk.Radiobutton(self.frame, text="Cliente", variable=self.tipo, value="cliente", bg="#ffffff", fg="#333333").place(relx=0.3, rely=0.74, anchor="center")
        tk.Radiobutton(self.frame, text="Bibliotecário", variable=self.tipo, value="bibliotecario", bg="#ffffff", fg="#333333").place(relx=0.7, rely=0.74, anchor="center")

        # Botões
        self.create_button(self.frame, "Cadastrar", 0.85, self.cadastrar_usuario)
        self.create_button(self.frame, "Voltar", 0.92, self.voltar)

        self.sistema = Sistema()

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

    def create_input(self, parent, text, rely) -> None:
        tk.Label(parent, text=text, font=("Helvetica", 10), bg="#ffffff", fg="#555555").place(relx=0.1, rely=rely, anchor="w")

    def create_entry(self, parent, rely, **kwargs) -> None:
        entry = tk.Entry(parent, font=("Helvetica", 10), relief="flat", bg="#eeeeee", **kwargs)
        entry.place(relx=0.1, rely=rely, width=350, height=30)
        return entry

    def create_button(self, parent, text, rely, command) -> None:
        button = tk.Button(parent, text=text, font=("Helvetica", 10), bg="#4CAF50", fg="#ffffff",
                           activebackground="#45a049", activeforeground="#ffffff", relief="flat", command=command)
        button.place(relx=0.5, rely=rely, anchor="center", width=200, height=40)

    def cadastrar_usuario(self) -> None:
        nome = self.nome.get().strip()
        matricula = self.matricula.get().strip()
        senha = self.senha.get().strip()
        pergunta_seguranca = self.pergunta_seguranca.get().strip()
        resposta_seguranca = self.resposta_seguranca.get().strip()
        cpf = self.cpf.get().strip()

        if not nome or not matricula or not senha or not pergunta_seguranca or not resposta_seguranca or not cpf:
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos!")
            return

        # Validação do formato do CPF
        if not re.match(r'^\d{3}\.\d{3}\.\d{3}-\d{2}$', cpf):
            messagebox.showerror("Erro", "CPF inválido! Use o formato xxx.xxx.xxx-xx.")
            return

        # Cadastro e validação
        if self.tipo.get() == "cliente":
            mensagem = self.sistema.cadastrar_cliente(nome, matricula, senha, pergunta_seguranca, resposta_seguranca, cpf)
        elif self.tipo.get() == "bibliotecario":
            mensagem = self.sistema.cadastrar_bibliotecaria(nome, matricula, senha, pergunta_seguranca, resposta_seguranca, cpf)

        # Exibe mensagens de erro ou sucesso
        if "Erro" in mensagem:
            messagebox.showerror("Erro", mensagem)
        else:
            messagebox.showinfo("Sucesso", mensagem)
            # Limpar os campos
            self.nome.delete(0, tk.END)
            self.matricula.delete(0, tk.END)
            self.senha.delete(0, tk.END)
            self.pergunta_seguranca.set("")
            self.resposta_seguranca.delete(0, tk.END)
            self.cpf.delete(0, tk.END)

    def voltar(self) -> None:
        from src.interface.login import TelaLogin
        self.master.destroy()
        root = tk.Tk()
        TelaLogin(root)
        
class TelaCadastroLivro:
    def __init__(self, master) -> None:
        self.master = master
        self.master.title("Cadastro de Livros")
        self.master.geometry("600x700")
        self.master.configure(bg="#f5f5f5")

        self.sistema = Sistema()

        # Frame centralizado com bordas arredondadas
        self.frame = tk.Canvas(master, bg="#ffffff", highlightthickness=0)
        self.frame.place(relx=0.5, rely=0.5, anchor="center", width=500, height=600)
        self.create_rounded_rectangle(self.frame, 0, 0, 500, 600, radius=20, fill="#ffffff", outline="#cccccc")

        # Título
        tk.Label(self.frame, text="Cadastro de Livros", font=("Helvetica", 20, "bold"), fg="#333333", bg="#ffffff").place(relx=0.5, rely=0.08, anchor="center")

        # Campos de entrada
        self.create_input(self.frame, "Título do Livro", 0.2)
        self.titulo = self.create_entry(self.frame, 0.25)

        self.create_input(self.frame, "Autor do Livro", 0.35)
        self.autor = self.create_entry(self.frame, 0.4)

        # Botões estilizados
        self.create_button(self.frame, "Cadastrar Livro", 0.6, self.cadastrar_livro)
        self.create_button(self.frame, "Voltar", 0.7, self.voltar)

    def create_rounded_rectangle(self, canvas, x1, y1, x2, y2, radius=25, **kwargs) -> None:
        points = [x1+radius, y1, x2-radius, y1, x2, y1, x2, y1+radius,
                  x2, y2-radius, x2, y2, x2-radius, y2, x1+radius, y2,
                  x1, y2, x1, y2-radius, x1, y1+radius, x1, y1]
        return canvas.create_polygon(points, **kwargs, smooth=True)

    def create_input(self, parent, text, rely) -> None:
        tk.Label(parent, text=text, font=("Helvetica", 12), bg="#ffffff", fg="#555555").place(relx=0.1, rely=rely, anchor="w")

    def create_entry(self, parent, rely, **kwargs) -> None:
        entry = tk.Entry(parent, font=("Helvetica", 10), relief="flat", bg="#eeeeee", **kwargs)
        entry.place(relx=0.1, rely=rely, width=350, height=30)
        return entry

    def create_button(self, parent, text, rely, command) -> None:
        button = tk.Button(parent, text=text, font=("Helvetica", 12), bg="#4CAF50", fg="#ffffff",
                           activebackground="#45a049", activeforeground="#ffffff", relief="flat", command=command)
        button.place(relx=0.5, rely=rely, anchor="center", width=250, height=40)

    def cadastrar_livro(self) -> None:
        titulo = self.titulo.get().strip()
        autor = self.autor.get().strip()

        if titulo and autor:
            novo_livro = {
                "titulo": titulo,
                "autor": autor,
                "disponibilidade": True,
                "data_devolucao": None
            }
            self.sistema.banco_livros.adicionar(novo_livro)
            messagebox.showinfo("Sucesso", f"Livro '{titulo}' cadastrado com sucesso!")
            self.titulo.delete(0, tk.END)
            self.autor.delete(0, tk.END)
        else:
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos!")

    def voltar(self) -> None:
        from src.interface.painel_biblio import PainelBibliotecario
        self.master.destroy()
        root = tk.Tk()
        PainelBibliotecario(root)