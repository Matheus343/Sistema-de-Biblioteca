from src.cliente import Cliente
from src.livro import Livro

cliente = Cliente("Maria Souza", "67890", "senha456", "Cidade natal?", "São Paulo")
livro = Livro("1984", "George Orwell")

if cliente.reservar_livro(livro):
    print(f"{cliente.nome} reservou o livro '{livro.titulo}'")
else:
    print("Não foi possível reservar o livro.")
