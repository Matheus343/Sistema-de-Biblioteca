import tkinter as tk
from tkinter import messagebox
from src.sistema import Sistema

class TelaCadastro:
    def __init__(self, master):
        self.master = master
        self.master.title("Cadastro")
        self.master.geometry("500x600")

        tk.Label(master, text="Nome").pack(pady=5)
        self.nome = tk.Entry(master)
        self.nome.pack(pady=5)

        tk.Label(master, text="Matrícula").pack(pady=5)
        self.matricula = tk.Entry(master)
        self.matricula.pack(pady=5)

        tk.Label(master, text="Senha").pack(pady=5)
        self.senha = tk.Entry(master, show="*")
        self.senha.pack(pady=5)
        
        tk.Label(master, text="Escolha a Pergunta de Segurança").pack(pady=5)
        self.pergunta_seguranca = tk.StringVar()
        perguntas = [
            "Qual sua cor favorita?",
            "Qual o nome do seu animal de estimação?",
            "Qual o nome da professora do primeiro ano do fundamental?",
            "Qual sua comida favorita?"
        ]
        self.pergunta_seguranca_menu = tk.OptionMenu(master, self.pergunta_seguranca, *perguntas)
        self.pergunta_seguranca_menu.pack(pady=5)

        tk.Label(master, text="Resposta à Pergunta").pack(pady=5)
        self.resposta_seguranca = tk.Entry(master)
        self.resposta_seguranca.pack(pady=5)

        tk.Label(master, text="CPF (Formato: xxx.xxx.xxx-xx)").pack(pady=5)
        self.cpf = tk.Entry(master)
        self.cpf.pack(pady=5)

        tk.Label(master, text="Tipo de Cadastro").pack(pady=5)
        self.tipo = tk.StringVar(value="cliente")
        tk.Radiobutton(master, text="Cliente", variable=self.tipo, value="cliente").pack()
        tk.Radiobutton(master, text="Bibliotecário", variable=self.tipo, value="bibliotecario").pack()

        tk.Button(master, text="Cadastrar", command=self.cadastrar_usuario).pack(pady=10)
        tk.Button(master, text="Voltar", command=self.voltar).pack()

        self.sistema = Sistema()
        
    def cadastrar_usuario(self):
        nome = self.nome.get().strip()
        matricula = self.matricula.get().strip()
        senha = self.senha.get().strip()
        pergunta_seguranca = self.pergunta_seguranca.get().strip()
        resposta_seguranca = self.resposta_seguranca.get().strip()
        cpf = self.cpf.get().strip()

        if not nome or not matricula or not senha or not pergunta_seguranca or not resposta_seguranca or not cpf:
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos!")
            return

        import re
        if not re.match(r'^\d{3}\.\d{3}\.\d{3}-\d{2}$', cpf):
            messagebox.showerror("Erro", "CPF inválido! Use o formato xxx.xxx.xxx-xx.")
            return

        if self.tipo.get() == "cliente":
            self.sistema.cadastrar_cliente(nome, matricula, senha, pergunta_seguranca, resposta_seguranca, cpf)
            messagebox.showinfo("Sucesso", f"Cliente '{nome}' cadastrado com sucesso!")
        elif self.tipo.get() == "bibliotecario":
            self.sistema.cadastrar_bibliotecaria(nome, matricula, senha, pergunta_seguranca, resposta_seguranca, cpf)
            messagebox.showinfo("Sucesso", f"Bibliotecário '{nome}' cadastrado com sucesso!")

        self.nome.delete(0, tk.END)
        self.matricula.delete(0, tk.END)
        self.senha.delete(0, tk.END)
        self.pergunta_seguranca.set("")
        self.resposta_seguranca.delete(0, tk.END)
        self.cpf.delete(0, tk.END)

    def voltar(self):
        from src.interface.login import TelaLogin
        self.master.destroy()
        root = tk.Tk()
        TelaLogin(root)
        
class TelaCadastroLivro:
    def __init__(self, master):
        self.master = master
        self.master.title("Cadastro de Livros")
        self.master.geometry("300x300")

        tk.Label(master, text="Título").pack(pady=5)
        self.titulo = tk.Entry(master)
        self.titulo.pack(pady=5)

        tk.Label(master, text="Autor").pack(pady=5)
        self.autor = tk.Entry(master)
        self.autor.pack(pady=5)

        tk.Button(master, text="Cadastrar Livro", command=self.cadastrar_livro).pack(pady=10)
        tk.Button(master, text="Voltar", command=self.voltar).pack()

        self.sistema = Sistema()

    def cadastrar_livro(self):
        titulo = self.titulo.get()
        autor = self.autor.get()

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

    def voltar(self):
        from src.interface.painel_biblio import PainelBibliotecario
        self.master.destroy()
        root = tk.Tk()
        PainelBibliotecario(root)
