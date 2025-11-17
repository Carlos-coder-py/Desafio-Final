from funcoes1 import (
    adicionar_transacao,
    remover_transacao,
    listar_por_categoria,
    listar_por_periodo,
    saldo_por_periodo
)

def exibir_menu():
    print("Seja bem vindo(a)!")
    print("1 - Adicionar transação")
    print("2 - Remover transação")
    print("3 - Listar por categoria")
    print("4 - Listar por período")
    print("5 - Calcular saldo por período")
    print("6 - Sair")

while True:
    exibir_menu()  # <-- AGORA O MENU APARECE!
    opcao = input("Escolha uma das opções: ")

    if opcao == "1":
        adicionar_transacao()
    elif opcao == "2":
        remover_transacao()
    elif opcao == "3":
        listar_por_categoria()
    elif opcao == "4":
        listar_por_periodo()
    elif opcao == "5":
        saldo_por_periodo()
    elif opcao == "6":
        print("Saindo...")
        break
    else:
        print("Opção inválida, tente novamente.")
