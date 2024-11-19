from src.livro import Livro

livro = Livro("1984", "George Orwell")

print(f"Disponível? {livro.disponibilidade}")
livro.emprestar_livro("2024-12-01")
print(f"Disponível após emprestado? {livro.disponibilidade}")
livro.devolver_livro()
print(f"Disponível após devolução? {livro.disponibilidade}")
