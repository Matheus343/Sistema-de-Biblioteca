class Livro:
    def __init__(self, titulo, autor, disponibilidade=True, data_devolucao=None) -> None:
        self.titulo = titulo
        self.autor = autor
        self.disponibilidade = disponibilidade
        self.data_devolucao = data_devolucao
#função para realizar o aluguel do livro com uma data de devolução
    def emprestar_livro(self, data_devolucao) -> None:
        if self.disponibilidade:
            self.disponibilidade = False
            self.data_devolucao = data_devolucao
            return True
        return False
#função para quando o livro é devolvido
    def devolver_livro(self) -> None:
        self.disponibilidade = True
        self.data_devolucao = None
