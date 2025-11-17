import json
from datetime import datetime

ARQUIVO = "transacoes.json"

def carregar_dados():
    try:
        with open(ARQUIVO, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def salvar_dados(transacoes):
    with open(ARQUIVO, "w") as f:
        json.dump(transacoes, f, indent=4)

def validar_data(data_str):
    try:
        datetime.strptime(data_str, "%d/%m/%Y")
        return True
    except:
        return False

def adicionar_transacao():
    data = input("Data (dd/mm/aaaa):")
    while not validar_data(data):
        print("Data inválida!")
        data = input("Data (dd/mm/aaaa):")

    tipo = input("Tipo (entrada/saida):").lower()
    while tipo not in ["entrada", "saida"]:
        print("Tipo inválido!")
        tipo = input("Tipo (entrada/saida):").lower()

    categoria = input("Categoria:")
    descricao = input("Descrição:")

    valor = input("Digite o valor:")
    try:
        valor = float(valor)
    except:
        print("Valor inválido")
        valor = 0.0

    transacoes = carregar_dados()

    transacoes.append({
        "data": data,
        "tipo": tipo,
        "categoria": categoria,
        "descricao": descricao,
        "valor": valor
    })

    salvar_dados(transacoes)
    print("Transação salva e adicionada com sucesso!")


def remover_transacao():
    transacoes = carregar_dados()
    listar_todas(transacoes)

    idx = int(input("Digite o número da transação para remover:"))
    if 0 <= idx < len(transacoes):
        transacoes.pop(idx)
        salvar_dados(transacoes)
        print("Transação removida!")
    else:
        print("Índice inválido.")


def listar_todas(transacoes):
    print("Segue todas as transações:")
    for i, t in enumerate(transacoes):
        print(f"{i} - {t['data']} | {t['tipo']} | {t['categoria']} | {t['valor']} | {t['descricao']}")
    print()


def listar_por_categoria():
    cat = input("Categoria desejada:")

    transacoes = carregar_dados()

    print(f"Transações da Categoria: {cat}")
    for t in transacoes:
        if t["categoria"].lower() == cat.lower():
            print(t)
    print()


def listar_por_periodo():
    inicio = input("Digite a data de início (dd/mm/aaaa):")
    fim = input("Digite a data final (dd/mm/aaaa):")

    transacoes = carregar_dados()

    print(f"Transações entre {inicio} e {fim}")
    for t in transacoes:
        data_t = datetime.strptime(t["data"], "%d/%m/%Y")
        di = datetime.strptime(inicio, "%d/%m/%Y")
        df = datetime.strptime(fim, "%d/%m/%Y")
        if di <= data_t <= df:
            print(t)
    print()


def saldo_por_periodo():
    inicio = input("Digite a data de início (dd/mm/aaaa):")
    fim = input("Digite a data final (dd/mm/aaaa):")

    transacoes = carregar_dados()

    saldo = 0
    for t in transacoes:
        data_t = datetime.strptime(t["data"], "%d/%m/%Y")
        di = datetime.strptime(inicio, "%d/%m/%Y")
        df = datetime.strptime(fim, "%d/%m/%Y")

        if di <= data_t <= df:
            if t["tipo"] == "entrada":
                saldo += t["valor"]
            else:
                saldo -= t["valor"]

    print(f"Saldo no período: R$ {saldo:.2f}")