import tkinter as tk
from tkinter import messagebox
from src.sistema import Sistema
from tkinter import simpledialog

class TelaLogin:
    def __init__(self, master):
        self.master = master
        self.master.title("Login")
        self.master.geometry("400x400")

        tk.Label(master, text="Matrícula").pack(pady=5)
        self.matricula = tk.Entry(master)
        self.matricula.pack(pady=5)

        tk.Label(master, text="Senha").pack(pady=5)
        self.senha = tk.Entry(master, show="*")
        self.senha.pack(pady=5)
        
        tk.Button(master, text="Redefinir Senha", command=self.redefinir_senha).pack(pady=10)

        self.perfil = tk.StringVar(value="cliente")
        tk.Radiobutton(master, text="Cliente", variable=self.perfil, value="cliente").pack()
        tk.Radiobutton(master, text="Bibliotecário", variable=self.perfil, value="bibliotecaria").pack()

        tk.Button(master, text="Login", command=self.realizar_login).pack(pady=10)
        tk.Button(master, text="Cadastrar Novo Usuário", command=self.abrir_tela_cadastro).pack()
        tk.Button(master, text="Visualizar Acervo (Anônimo)", command=self.abrir_acervo_anonimo).pack(pady=5)

        self.sistema = Sistema()

    def realizar_login(self):
        matricula = self.matricula.get()
        senha = self.senha.get()
        perfil = self.perfil.get()

        usuario = self.sistema.login(matricula, senha, perfil)
        if usuario:
            messagebox.showinfo("Login", f"Bem-vindo, {usuario['nome']}!")
            if perfil == "bibliotecaria":
                from src.interface.painel_biblio import PainelBibliotecario
                self.master.destroy()
                root = tk.Tk()
                PainelBibliotecario(root)
            else:  # Cliente
                from src.interface.painel_cliente import PainelCliente
                self.master.destroy()
                root = tk.Tk()
                PainelCliente(root, usuario)
        else:
            messagebox.showerror("Erro", "Credenciais inválidas!")

    def abrir_tela_cadastro(self):
        from src.interface.cadastro import TelaCadastro
        self.master.destroy()
        root = tk.Tk()
        TelaCadastro(root)

    def abrir_acervo_anonimo(self):
        livros = self.sistema.listar_livros()
        livros_disponiveis = [f"{livro['titulo']} - {livro['autor']} (Disponíveis: {livro['disponibilidade']})"
                            for livro in livros if livro["disponibilidade"]]
        if livros_disponiveis:
            livros_str = "\n".join(livros_disponiveis)
            messagebox.showinfo("Acervo da Biblioteca", livros_str)
        else:
            messagebox.showinfo("Acervo da Biblioteca", "Nenhum livro disponível no momento.")

    def redefinir_senha(self):
        redefinir_window = tk.Toplevel(self.master)
        redefinir_window.title("Redefinir Senha")
        redefinir_window.geometry("400x400")

        tk.Label(redefinir_window, text="Selecione o tipo de usuário").pack(pady=5)
        tipo_usuario = tk.StringVar(value="cliente")
        tk.Radiobutton(redefinir_window, text="Cliente", variable=tipo_usuario, value="cliente").pack()
        tk.Radiobutton(redefinir_window, text="Bibliotecário", variable=tipo_usuario, value="bibliotecario").pack()

        tk.Label(redefinir_window, text="Matrícula").pack(pady=5)
        matricula_entry = tk.Entry(redefinir_window)
        matricula_entry.pack(pady=5)

        tk.Label(redefinir_window, text="CPF (Formato: xxx.xxx.xxx-xx)").pack(pady=5)
        cpf_entry = tk.Entry(redefinir_window)
        cpf_entry.pack(pady=5)

        def validar_usuario():
            matricula = matricula_entry.get().strip()
            cpf = cpf_entry.get().strip()

            if tipo_usuario.get() == "cliente":
                usuarios = self.sistema.banco_clientes.carregar()
            else:
                usuarios = self.sistema.banco_bibliotecarios.carregar()

            usuario = next(
                (u for u in usuarios if u["matricula"] == matricula and u.get("cpf", "") == cpf), None
            )

            if not usuario:
                messagebox.showerror("Erro", "Matrícula ou CPF inválido!")
                return

            pergunta = usuario.get("pergunta_seguranca", "Pergunta não definida")
            tk.Label(redefinir_window, text=f"Pergunta de Segurança: {pergunta}").pack(pady=5)

            resposta_entry = tk.Entry(redefinir_window)
            resposta_entry.pack(pady=5)

            def redefinir():
                resposta = resposta_entry.get().strip()
                if resposta.lower() != usuario.get("resposta_seguranca", "").lower():
                    messagebox.showerror("Erro", "Resposta incorreta!")
                    return

                from tkinter import simpledialog
                nova_senha = simpledialog.askstring("Nova Senha", "Digite sua nova senha:", show="*")
                if not nova_senha:
                    messagebox.showerror("Erro", "A senha não pode estar vazia!")
                    return

                usuario["senha"] = nova_senha
                if tipo_usuario.get() == "cliente":
                    self.sistema.banco_clientes.salvar(usuarios)
                else:
                    self.sistema.banco_bibliotecarios.salvar(usuarios)
                messagebox.showinfo("Sucesso", "Senha redefinida com sucesso!")
                redefinir_window.destroy()

            tk.Button(redefinir_window, text="Confirmar Resposta", command=redefinir).pack(pady=10)

        tk.Button(redefinir_window, text="Validar", command=validar_usuario).pack(pady=10)
