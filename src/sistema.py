from src.banco_de_dados import BancoDeDados
from src.cliente import Cliente
from src.livro import Livro
from src.bibliotecaria import Bibliotecaria
from datetime import datetime
from src.banco_de_dados import BancoDeDados
from datetime import datetime, timedelta  

class Sistema:
    #carrega os bancos de dados .json
    def __init__(self) -> None:
        self.banco_clientes = BancoDeDados("data/clientes.json")
        self.banco_livros = BancoDeDados("data/livros.json")
        self.banco_bibliotecarios = BancoDeDados("data/bibliotecarios.json")
        
    def cpf_existe(self, cpf) -> None:
        """
        Verifica se o CPF já existe entre os clientes ou bibliotecários.
        """
        #verifica nos clientes
        clientes = self.banco_clientes.carregar()
        if any(cliente.get("cpf") == cpf for cliente in clientes):
            return True
        
        #verifica nos bibliotecários
        bibliotecarios = self.banco_bibliotecarios.carregar()
        if any(bibliotecario.get("cpf") == cpf for bibliotecario in bibliotecarios):
            return True

        return False
    
    def matricula_existe(self, matricula) -> None:
        """
        Verifica se a matrícula já existe entre os clientes ou bibliotecários.
        """
        clientes = self.banco_clientes.carregar()
        if any(cliente.get("matricula") == matricula for cliente in clientes):
            return True

        bibliotecarios = self.banco_bibliotecarios.carregar()
        if any(bibliotecario.get("matricula") == matricula for bibliotecario in bibliotecarios):
            return True

        return False
    
    #classe para cadastro dos clientes, salva os valores atribuidos a nome, matricula, senha e etc ao clientes.json
    def cadastrar_cliente(self, nome, matricula, senha, pergunta_seguranca, resposta_seguranca, cpf) -> None:
        if self.cpf_existe(cpf):
            return f"Erro: O CPF {cpf} já está cadastrado."
        if self.matricula_existe(matricula):
            return f"Erro: A matrícula {matricula} já está cadastrada."

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

    #classe para cadastro dos bibliotecarios, salva os valores atribuidos a nome, matricula, senha e etc ao bibliotecarios.json   
    def cadastrar_bibliotecaria(self, nome, matricula, senha, pergunta_seguranca, resposta_seguranca, cpf) -> None:
        if self.cpf_existe(cpf):
            return f"Erro: O CPF {cpf} já está cadastrado."
        if self.matricula_existe(matricula):
            return f"Erro: A matrícula {matricula} já está cadastrada."

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

#função de login, utiliza os dados carregados no .json para validar o login
    def login(self, matricula, senha, perfil="cliente") -> None:
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
#listagem de livros já cadastrados
    def listar_livros(self) -> None:
        return self.banco_livros.carregar()
    
#listagem de clientes já cadastrados
    def listar_clientes(self) -> None:
        return self.banco_clientes.carregar()
    
#função para reserva de livros, associa um datetime a eles para verificar pendências
    def reservar_livro(self, matricula_cliente, titulo) -> None:
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
#lista as pendências
    def listar_pendencias(self, matricula_cliente) -> None:
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