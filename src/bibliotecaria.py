class Bibliotecaria:
    def __init__(self, nome, matricula, senha) -> None:
        self.nome = nome
        self.matricula = matricula
        self.senha = senha
#criação de livros no sistema
    def cadastrar_livro(self, titulo, autor, banco_livros) -> None:
        novo_livro = {
            "titulo": titulo,
            "autor": autor,
            "disponibilidade": True,
            "data_devolucao": None
        }
        banco_livros.adicionar(novo_livro)
        return f"Livro '{titulo}' cadastrado com sucesso."
#criação de clientes no sistema 
    def cadastrar_cliente(self, nome, matricula, senha, pergunta, resposta, banco_clientes) -> None:
        novo_cliente = {
            "nome": nome,
            "matricula": matricula,
            "senha": senha,
            "pergunta_seguranca": pergunta,
            "resposta": resposta,
            "livros_reservados": []
        }
        banco_clientes.adicionar(novo_cliente)
        return f"Cliente '{nome}' cadastrado com sucesso."
#delete de cliente no sistema
    def remover_cliente(self, matricula, banco_clientes) -> None:
        clientes = banco_clientes.carregar()
        clientes = [c for c in clientes if c["matricula"] != matricula]
        banco_clientes.salvar(clientes)
        return f"Cliente com matrícula {matricula} removido."
