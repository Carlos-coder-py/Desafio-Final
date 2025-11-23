import matplotlib.pyplot as plt
import funcoes1 as fn
from datetime import datetime
from collections import defaultdict


def calcular_estatisticas_periodo(inicio, fim):
    if not fn.validar_data(inicio) or not fn.validar_data(fim):
        return "Erro: Data de início ou fim inválida! Use o formato dd/mm/aaaa.", None, None

    try:
        di = datetime.strptime(inicio, "%d/%m/%Y")
        df = datetime.strptime(fim, "%d/%m/%Y")
    except ValueError:
        return "Erro: Formato de data incorreto.", None, None

    if di > df:
        return "Erro: Data de início não pode ser posterior à data final.", None, None

    transacoes = fn.carregar_dados()
    total_receitas = 0.0
    total_despesas = 0.0

    for t in transacoes:
        try:
            data_t = datetime.strptime(t["data"], "%d/%m/%Y")
            if di <= data_t <= df:
                if t["tipo"] == "entrada":
                    total_receitas += t["valor"]
                elif t["tipo"] == "saida":
                    total_despesas += t["valor"]
        except:
            pass

    saldo = total_receitas - total_despesas

    resultado = (
        f"Estatísticas no Período ({inicio} a {fim}):\n"
        f"-----------------------------------------\n"
        f"Total de Receitas: R$ {total_receitas:.2f}\n"
        f"Total de Despesas: R$ {total_despesas:.2f}\n"
        f"Saldo Líquido: R$ {saldo:.2f}"
    )

    return resultado, total_receitas, total_despesas


def calcular_media_gastos_por_categoria():
    transacoes = fn.carregar_dados()

    gastos_por_categoria = defaultdict(lambda: {'soma': 0.0, 'contagem': 0})

    for t in transacoes:
        if t["tipo"] == "saida":
            categoria = t["categoria"].capitalize()
            gastos_por_categoria[categoria]['soma'] += t["valor"]
            gastos_por_categoria[categoria]['contagem'] += 1

    if not gastos_por_categoria:
        return "Nenhuma despesa (saída) encontrada para calcular a média por categoria."

    resultado = "Média de Gastos (Saídas) por Categoria:\n"
    resultado += "-----------------------------------------\n"

    for categoria, dados in gastos_por_categoria.items():
        media = dados['soma'] / dados['contagem']
        resultado += f"Categoria '{categoria}': R$ {media:.2f} (Baseado em {dados['contagem']} transações)\n"

    return resultado


def gerar_grafico_pizza_gastos():
    transacoes = fn.carregar_dados()

    gastos_por_categoria = defaultdict(float)
    total_gastos = 0.0

    for t in transacoes:
        if t["tipo"] == "saida":
            categoria = t["categoria"].capitalize()
            gastos_por_categoria[categoria] += t["valor"]
            total_gastos += t["valor"]

    if total_gastos == 0.0:
        return "Não há despesas (saídas) registradas para gerar o gráfico."

    categorias = list(gastos_por_categoria.keys())
    valores = list(gastos_por_categoria.values())

    # Configuração do gráfico
    plt.figure(figsize=(5, 5))

    plt.pie(valores, labels=categorias, autopct='%1.1f%%', startangle=90, shadow=True,
            wedgeprops={'edgecolor': 'black'})

    plt.title('Proporção de Gastos por Categoria (Saídas)')

    plt.axis('equal')

    # Exibe o gráfico em uma nova janela
    plt.show()


    return "Gráfico de pizza gerado com sucesso!"
