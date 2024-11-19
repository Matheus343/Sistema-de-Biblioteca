from src.banco_de_dados import BancoDeDados

clientes_db = BancoDeDados("./data/clientes.json")

novo_cliente = {
    "nome": "João Silva",
    "matricula": "12345",
    "senha": "senha123",
    "pergunta_seguranca": "Qual sua cor favorita?",
    "resposta": "Azul",
    "livros_reservados": []
}

clientes_db.adicionar(novo_cliente)

print(clientes_db.carregar())
