# Biblioteca e Empréstimos — Python + MongoDB

Projeto baseado no **Projeto 02** do material didático "MongoDB + Python — 10 Projetos Práticos".

## Funcionalidades

- Cadastro de livros por ISBN (sem duplicatas)
- Catálogo de livros e indicação de disponibilidade
- Empréstimo seguro: o mesmo exemplar não pode ser emprestado duas vezes ao mesmo tempo
- Devolução de livros
- **Desafio extra implementado:** nome do leitor, data do empréstimo e listagem dos empréstimos ativos

## Pré-requisitos

Python 3.11+ e MongoDB Community Server em execução (ou MongoDB Atlas com URI configurada). O MongoDB Compass é opcional para conferir os dados.

## Como executar no Windows (PowerShell)

Na raiz do projeto:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
.\.venv\Scripts\python.exe -m p02_biblioteca.main
```

Não é necessário ativar o ambiente virtual. Se usar MongoDB Atlas, edite o `.env` com sua URI privada. **Não publique o `.env`**.

## Modelo de dados

Banco: `laboratorio_python` • Coleção: `livros_p02`

```json
{
  "isbn": "9781234567890",
  "titulo": "Livro de exemplo",
  "autor": "Autor de exemplo",
  "disponivel": true,
  "leitor": null,
  "emprestado_em": null
}
```

O MongoDB cria também o campo `_id`. O índice único de `isbn` impede cadastros repetidos.

## Testes sugeridos

1. Cadastre um livro (opção 1).
2. Confira o catálogo (opção 2).
3. Empreste o livro, informando seu ISBN e o nome de um leitor (opção 3).
4. Tente emprestar o mesmo ISBN novamente: o sistema deve recusar.
5. Veja o empréstimo ativo e sua data (opção 5).
6. Devolva o livro (opção 4).
7. Empreste novamente: agora deve funcionar.
8. Tente cadastrar o mesmo ISBN de novo: deve ser recusado.

## Explicação resumida

- `conexao.py` lê a URI do `.env`, testa o MongoDB e seleciona o banco.
- `main.py` oferece as opções de menu e implementa operações sobre a coleção.
- `create_index(..., unique=True)` impede dois livros com o mesmo ISBN.
- `find_one_and_update()` altera a disponibilidade com uma condição: somente livros disponíveis podem ser emprestados e somente emprestados podem ser devolvidos.
- `datetime.now(timezone.utc)` registra o momento do empréstimo.

