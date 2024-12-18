import json
#classe para gerenciamento do banco de dados em .json
class BancoDeDados:
    def __init__(self, arquivo) -> None:
        self.arquivo = arquivo

    def carregar(self) -> None:
        try:
            with open(self.arquivo, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def salvar(self, dados) -> None:
        with open(self.arquivo, 'w') as file:
            json.dump(dados, file, indent=4)

    def adicionar(self, item) -> None:
        dados = self.carregar()
        dados.append(item)
        self.salvar(dados)
