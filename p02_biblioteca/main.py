"""Projeto 02: cadastro de livros e controle seguro de empréstimos."""
from datetime import datetime, timezone
from pymongo import ReturnDocument
from pymongo.errors import DuplicateKeyError, PyMongoError
from conexao import banco

livros = banco['livros_p02']
livros.create_index('isbn', unique=True)


def cadastrar():
    isbn = input('ISBN: ').strip()
    titulo = input('Título: ').strip()
    autor = input('Autor: ').strip()
    if not all([isbn, titulo, autor]):
        print('Preencha todos os campos.')
        return
    try:
        livros.insert_one({
            'isbn': isbn, 'titulo': titulo, 'autor': autor,
            'disponivel': True, 'leitor': None, 'emprestado_em': None
        })
        print('Livro cadastrado com sucesso!')
    except DuplicateKeyError:
        print('Este ISBN já está cadastrado.')


def catalogo():
    encontrados = False
    for livro in livros.find({}, {'_id': 0}).sort('titulo', 1):
        encontrados = True
        situacao = 'Disponível' if livro['disponivel'] else 'Emprestado'
        print(f"{livro['isbn']} | {livro['titulo']} | {livro['autor']} | {situacao}")
        if not livro['disponivel']:
            print(f"    Leitor: {livro.get('leitor') or 'Não informado'}")
    if not encontrados:
        print('Nenhum livro cadastrado.')


def emprestar():
    isbn = input('ISBN do livro: ').strip()
    leitor = input('Nome do leitor: ').strip()
    if not isbn or not leitor:
        print('Informe o ISBN e o nome do leitor.')
        return
    resultado = livros.find_one_and_update(
        {'isbn': isbn, 'disponivel': True},
        {'$set': {
            'disponivel': False,
            'leitor': leitor,
            'emprestado_em': datetime.now(timezone.utc)
        }},
        return_document=ReturnDocument.AFTER
    )
    print('Empréstimo realizado!' if resultado else 'Livro inexistente ou indisponível.')


def devolver():
    isbn = input('ISBN do livro: ').strip()
    resultado = livros.find_one_and_update(
        {'isbn': isbn, 'disponivel': False},
        {'$set': {'disponivel': True, 'leitor': None, 'emprestado_em': None}},
        return_document=ReturnDocument.AFTER
    )
    print('Devolução registrada!' if resultado else 'Livro inexistente ou não emprestado.')


def listar_emprestados():
    encontrou = False
    for livro in livros.find({'disponivel': False}).sort('titulo', 1):
        encontrou = True
        data = livro.get('emprestado_em')
        data_texto = data.strftime('%d/%m/%Y %H:%M UTC') if data else 'Não informada'
        print(f"{livro['titulo']} | ISBN: {livro['isbn']} | Leitor: {livro.get('leitor') or 'Não informado'} | Data: {data_texto}")
    if not encontrou:
        print('Nenhum livro emprestado.')


def main():
    while True:
        print('\n=== BIBLIOTECA ===')
        print('[1] Cadastrar livro')
        print('[2] Listar catálogo')
        print('[3] Emprestar livro')
        print('[4] Devolver livro')
        print('[5] Listar empréstimos ativos')
        print('[0] Sair')
        opcao = input('Escolha: ').strip()
        try:
            if opcao == '1':
                cadastrar()
            elif opcao == '2':
                catalogo()
            elif opcao == '3':
                emprestar()
            elif opcao == '4':
                devolver()
            elif opcao == '5':
                listar_emprestados()
            elif opcao == '0':
                print('Até logo!')
                break
            else:
                print('Opção inválida.')
        except PyMongoError as erro:
            print(f'Erro ao acessar o MongoDB: {erro}')


if __name__ == '__main__':
    main()
