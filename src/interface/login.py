import tkinter as tk
from tkinter import messagebox
from src.sistema import Sistema
from src.interface.acervo_anonimo import TelaAcervoAnonimo
from tkinter import simpledialog

# UI de login do sistema, valida os dados cadastrados para realização de login de clientes e bibliotecarios
# cada tipo de login (cliente/bibliotecario) leva a determinada area do sistema que possui diferentes funções

class TelaLogin:
    def __init__(self, master) -> None:
        self.master = master
        self.master.title("Login")
        self.master.geometry("600x700")  # Tela maior verticalmente
        self.master.configure(bg="#f5f5f5")

        # Frame centralizado com bordas arredondadas
        self.frame = tk.Canvas(master, bg="#ffffff", highlightthickness=0)
        self.frame.place(relx=0.5, rely=0.5, anchor="center", width=500, height=600)
        self.create_rounded_rectangle(self.frame, 0, 0, 500, 600, radius=20, fill="#ffffff", outline="#cccccc")

        # Título da tela de login
        tk.Label(self.frame, text="Login", font=("Helvetica", 20, "bold"), fg="#333333", bg="#ffffff").place(relx=0.5, rely=0.05, anchor="center")

        # Campos de entrada com espaço adequado
        self.create_input(self.frame, "Matrícula", 0.15)
        self.matricula = self.create_entry(self.frame, 0.2)

        self.create_input(self.frame, "Senha", 0.3)
        self.senha = self.create_entry(self.frame, 0.35, show="*")

        # Botão redefinir senha
        self.create_button(self.frame, "Redefinir Senha", 0.45, self.redefinir_senha)

        # Radio Buttons
        self.perfil = tk.StringVar(value="cliente")
        tk.Radiobutton(self.frame, text="Cliente", variable=self.perfil, value="cliente", bg="#ffffff", fg="#333333").place(relx=0.3, rely=0.55, anchor="center")
        tk.Radiobutton(self.frame, text="Bibliotecário", variable=self.perfil, value="bibliotecaria", bg="#ffffff", fg="#333333").place(relx=0.7, rely=0.55, anchor="center")

        # Espaçamento harmonioso entre os botões
        self.create_button(self.frame, "Login", 0.65, self.realizar_login)
        self.create_button(self.frame, "Cadastrar Novo Usuário", 0.75, self.abrir_tela_cadastro)
        self.create_button(self.frame, "Visualizar Acervo (Anônimo)", 0.85, self.abrir_acervo_anonimo)

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
        button.place(relx=0.5, rely=rely, anchor="center", width=250, height=40)

    def realizar_login(self) -> None:
        matricula = self.matricula.get()
        senha = self.senha.get()
        perfil = self.perfil.get()

        usuario = self.sistema.login(matricula, senha, perfil)
        if usuario:
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

    def abrir_tela_cadastro(self) -> None:
        from src.interface.cadastro import TelaCadastro
        self.master.destroy()
        root = tk.Tk()
        TelaCadastro(root)

    def abrir_acervo_anonimo(self) -> None:
        self.master.destroy()
        root = tk.Tk()
        TelaAcervoAnonimo(root)

    def redefinir_senha(self) -> None:
        redefinir_window = tk.Toplevel(self.master)
        redefinir_window.title("Redefinir Senha")
        redefinir_window.geometry("600x700")  # Tela maior verticalmente
        redefinir_window.configure(bg="#f5f5f5")

        # Frame centralizado com bordas arredondadas
        frame = tk.Canvas(redefinir_window, bg="#ffffff", highlightthickness=0)
        frame.place(relx=0.5, rely=0.5, anchor="center", width=500, height=600)
        self.create_rounded_rectangle(frame, 0, 0, 500, 600, radius=20, fill="#ffffff", outline="#cccccc")

        # Título da tela
        tk.Label(frame, text="Redefinir Senha", font=("Helvetica", 20, "bold"), fg="#333333", bg="#ffffff").place(relx=0.5, rely=0.05, anchor="center")

        # Tipo de usuário
        tk.Label(frame, text="Selecione o tipo de usuário", font=("Helvetica", 10), bg="#ffffff", fg="#555555").place(relx=0.1, rely=0.15, anchor="w")
        tipo_usuario = tk.StringVar(value="cliente")
        tk.Radiobutton(frame, text="Cliente", variable=tipo_usuario, value="cliente", bg="#ffffff", fg="#333333").place(relx=0.3, rely=0.2, anchor="center")
        tk.Radiobutton(frame, text="Bibliotecário", variable=tipo_usuario, value="bibliotecario", bg="#ffffff", fg="#333333").place(relx=0.7, rely=0.2, anchor="center")

        # Matrícula
        self.create_input(frame, "Matrícula", 0.3)
        matricula_entry = self.create_entry(frame, 0.35)

        # CPF
        self.create_input(frame, "CPF (Formato: xxx.xxx.xxx-xx)", 0.45)
        cpf_entry = self.create_entry(frame, 0.5)

        # Botão Validar
        def validar_usuario() -> None:
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
            tk.Label(frame, text=f"Pergunta de Segurança: {pergunta}", font=("Helvetica", 10), bg="#ffffff", fg="#555555").place(relx=0.1, rely=0.6, anchor="w")

            resposta_entry = self.create_entry(frame, 0.68)

            def redefinir() -> None:
                resposta = resposta_entry.get().strip()
                if resposta.lower() != usuario.get("resposta_seguranca", "").lower():
                    messagebox.showerror("Erro", "Resposta incorreta!")
                    return

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

            self.create_button(frame, "Confirmar Resposta", 0.8, redefinir)

        self.create_button(frame, "Validar", 0.6, validar_usuario)
