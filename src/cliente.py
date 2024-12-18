class Cliente:
    def __init__(self, nome, matricula, senha, pergunta_seguranca, resposta) -> None:
        self.nome = nome
        self.matricula = matricula
        self.senha = senha
        self.pergunta_seguranca = pergunta_seguranca
        self.resposta = resposta
        self.livros_reservados = []
#visualização de acervo para usuarios anonimos e cadastrados
    def visualizar_acervo(self, banco_livros) -> None:
        livros = banco_livros.carregar()
        return [livro for livro in livros if livro["disponibilidade"]]
#reserva de livros para clientes
    def reservar_livro(self, titulo, banco_livros) -> None:
        livros = banco_livros.carregar()
        for livro in livros:
            if livro["titulo"] == titulo and livro["disponibilidade"]:
                livro["disponibilidade"] = False
                livro["data_devolucao"] = "Data de exemplo"
                banco_livros.salvar(livros)
                self.livros_reservados.append(titulo)
                return f"Livro '{titulo}' reservado."
        return f"Livro '{titulo}' não disponível."
