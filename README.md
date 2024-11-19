# Sistema de Biblioteca

Um sistema de biblioteca desenvolvido em Python com interface gráfica utilizando Tkinter e persistência de dados em arquivos JSON. O sistema foi projetado para gerenciar usuários (clientes e bibliotecários), livros, reservas e redefinição de senhas com segurança. Ideal para aprendizado e implementação de conceitos de Programação Orientada a Objetos (POO).

---

## **Funcionalidades**

### **Usuários Anônimos**
- Visualizam o acervo de livros disponíveis.

### **Clientes**
- Podem realizar login com matrícula e senha.
- Visualizam livros disponíveis no acervo.
- Reservam livros (se disponíveis) ou entram na fila de espera.
- Visualizam os livros reservados.
- Redefinem a senha utilizando CPF e pergunta de segurança.

### **Bibliotecários**
- Podem realizar login com matrícula e senha.
- Cadastram novos livros, clientes e outros bibliotecários.
- Gerenciam pendências de clientes, como devoluções atrasadas.
- Redefinem a senha utilizando CPF e pergunta de segurança.

---

## **Tecnologias Utilizadas**
- **Linguagem:** Python 3.x
- **Interface Gráfica:** Tkinter
- **Persistência de Dados:** JSON
- **Paradigma:** Programação Orientada a Objetos (POO)

---

## **Instalação**

### **Pré-requisitos**
- Python 3.x instalado.
- Ambiente de desenvolvimento configurado (ex.: VSCode, PyCharm, etc.).

### **Passos**
1. Clone este repositório:
   git clone https://github.com/seu-usuario/sistema-biblioteca.git

2. Navegue até o diretório do projeto:
    cd sistema-biblioteca
   
3. Instale as dependências (caso necessário):
    pip install -r requirements.txt
   
4. Execute o sistema:
    python main.py


---


### **Estrutura do Projeto**

sistemaBiblioteca/
├── data/                     # Diretório para arquivos JSON
│   ├── clientes.json         # Dados dos clientes
│   ├── livros.json           # Dados dos livros
│   └── bibliotecarios.json   # Dados dos bibliotecários
├── src/                      # Diretório do código-fonte
│   ├── interface/            # Interface gráfica com Tkinter
│   │   ├── cadastro.py       # Tela de cadastro
│   │   ├── login.py          # Tela de login e redefinição de senha
│   │   ├── painel_cliente.py # Painel do cliente
│   │   └── painel_biblio.py  # Painel do bibliotecário
│   ├── banco_de_dados.py     # Classe para manipulação de JSON
│   ├── sistema.py            # Classes principais do sistema
│   └── livro.py              # Classe Livro
├── main.py                   # Arquivo principal para executar o sistema
└── README.md                 # Documentação do projeto

Funcionalidades em Detalhes
1. Cadastro
    Clientes:
    Nome, matrícula, senha, pergunta de segurança, resposta e CPF.
    Armazenados no arquivo clientes.json.
   
    Bibliotecários:
    Nome, matrícula, senha, pergunta de segurança, resposta e CPF.
    Armazenados no arquivo bibliotecarios.json.
   
2. Login
    Clientes e bibliotecários acessam o sistema com matrícula e senha.
    Diferencia perfis para acessar os respectivos painéis.
   
3. Redefinição de Senha
    Usuários podem redefinir a senha utilizando:
    Matrícula.
    CPF.
    Resposta à pergunta de segurança.
   
4. Gestão de Livros
    Cadastrados por bibliotecários.
    Dados armazenados em livros.json:
    Título.
    Autor.
    Disponibilidade.
    Fila de espera (se houver).
   
5. Reservas e Fila de Espera
    Clientes podem reservar livros disponíveis.
    Caso o livro esteja indisponível, o cliente é adicionado à fila de espera.

6. Gerenciamento de Pendências
    Bibliotecários podem visualizar e remover pendências de clientes:
    Pendências geradas automaticamente para devoluções atrasadas.
    Calculadas com base na data de devolução.
   
### **Uso do Sistema**

1. Interface de Login
    A tela inicial permite:
    Login como cliente ou bibliotecário.
    Redefinição de senha.
2. Painel do Cliente
    Funcionalidades disponíveis:
    Visualizar acervo.
    Reservar livros.
    Verificar livros reservados.
    Redefinir senha.
3. Painel do Bibliotecário
    Funcionalidades disponíveis:
    Cadastrar novos livros, clientes e bibliotecários.
    Visualizar pendências de clientes.
    Redefinir senha.
   
### **Contribuições** 

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests.

Licença
Este projeto está licenciado sob a MIT License. Sinta-se livre para usá-lo e modificá-lo conforme necessário.

Contato
Se tiver dúvidas ou sugestões, entre em contato:

E-mail: matheus_xavier343@outlook.com
GitHub: Matheus343
