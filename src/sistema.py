from src.banco_de_dados import BancoDeDados
from src.cliente import Cliente
from src.livro import Livro
from src.bibliotecaria import Bibliotecaria
from datetime import datetime
from src.banco_de_dados import BancoDeDados
from datetime import datetime, timedelta

class Sistema:
    def __init__(self):
        self.banco_clientes = BancoDeDados("data/clientes.json")
        self.banco_livros = BancoDeDados("data/livros.json")
        self.banco_bibliotecarios = BancoDeDados("data/bibliotecarios.json")

    def cadastrar_cliente(self, nome, matricula, senha, pergunta_seguranca, resposta_seguranca, cpf):
        novo_cliente = {
            "nome": nome,
            "matricula": matricula,
            "senha": senha,
            "pergunta_seguranca": pergunta_seguranca,
            "resposta_seguranca": resposta_seguranca,
            "cpf": cpf,
            "livros_reservados": []
        }
        self.banco_clientes.adicionar(novo_cliente)
        return f"Cliente '{nome}' cadastrado com sucesso."

    def cadastrar_bibliotecaria(self, nome, matricula, senha, pergunta_seguranca, resposta_seguranca, cpf):
        nova_bibliotecaria = {
            "nome": nome,
            "matricula": matricula,
            "senha": senha,
            "pergunta_seguranca": pergunta_seguranca,
            "resposta_seguranca": resposta_seguranca,
            "cpf": cpf
        }
        self.banco_bibliotecarios.adicionar(nova_bibliotecaria)
        return f"Bibliotecária '{nome}' cadastrada com sucesso."

    def login(self, matricula, senha, perfil="cliente"):
        if perfil == "cliente":
            usuarios = self.banco_clientes.carregar()
        elif perfil == "bibliotecaria":
            usuarios = self.banco_bibliotecarios.carregar()
        else:
            return None

        for usuario in usuarios:
            if usuario["matricula"] == matricula and usuario["senha"] == senha:
                return usuario
        return None

    def listar_livros(self):
        return self.banco_livros.carregar()

    def listar_clientes(self):
        return self.banco_clientes.carregar()
    
    from datetime import datetime, timedelta

    def reservar_livro(self, matricula_cliente, titulo):
        clientes = self.banco_clientes.carregar()
        livros = self.banco_livros.carregar()

        cliente = next((c for c in clientes if c["matricula"] == matricula_cliente), None)
        livro = next((l for l in livros if l["titulo"].lower() == titulo.lower()), None)

        if not cliente or not livro:
            return "Livro ou cliente não encontrado."

        for reservado in cliente["livros_reservados"]:
            if isinstance(reservado, dict) and reservado["titulo"].lower() == titulo.lower():
                return f"Você já reservou o livro '{titulo}'."

        if livro["disponibilidade"]:
            data_devolucao = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
            livro["disponibilidade"] = False
            livro["data_devolucao"] = data_devolucao
            cliente["livros_reservados"].append({
                "titulo": titulo,
                "data_devolucao": data_devolucao
            })

            self.banco_livros.salvar(livros)
            self.banco_clientes.salvar(clientes)
            return f"Livro '{titulo}' reservado com sucesso! Data de devolução: {data_devolucao}."
        else:
            if "fila_espera" not in livro:
                livro["fila_espera"] = []
            livro["fila_espera"].append(cliente["matricula"])
            self.banco_livros.salvar(livros)
            return f"Livro '{titulo}' não disponível. Você foi adicionado à fila de espera."

    def listar_pendencias(self, matricula_cliente):
        clientes = self.banco_clientes.carregar()
        cliente = next((c for c in clientes if c["matricula"] == matricula_cliente), None)

        if not cliente:
            return None

        pendencias = []
        hoje = datetime.now().date()
        for livro in cliente["livros_reservados"]:
            if "data_devolucao" in livro:
                data_devolucao = datetime.strptime(livro["data_devolucao"], "%Y-%m-%d").date()
                if hoje > data_devolucao:
                    dias_atraso = (hoje - data_devolucao).days
                    pendencias.append(f"Livro: {livro['titulo']} - Atraso: {dias_atraso} dias")
        return pendencias