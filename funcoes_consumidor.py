# === FUNCOES DO CONSUMIDOR ===
# tudo que o consumidor faz no sistema

from funcoes_arquivo import ler_arquivo, gravar_linha, proximo_id

# cadastro de novo consumidor - pede os dados e grava no txt
def cadastrar_consumidor():
    print("CADASTRO DE CONSUMIDOR:")
    nome = input("Nome completo: ")
    email = input("Email: ")
    senha = input("Senha: ")
    cep = input("CEP: ")
    valor = input("Valor medio da conta de luz (R$): ")
    tipo = input("Tipo de imovel (Casa/Apartamento/Comercial/Rural): ")

    # monta o dicionario com os dados do novo consumidor
    novo = {
        "ID": str(proximo_id("banco_consumidores.txt")),
        "Nome": nome,
        "Email": email,
        "Senha": senha,
        "CEP": cep,
        "Valor_Conta": valor,
        "Tipo_Imovel": tipo
    }
    gravar_linha("banco_consumidores.txt", novo)  # grava no arquivo
    print("Conta criada com sucesso!")

# login do consumidor - verifica email e senha no txt
def login_consumidor():
    print("LOGIN CONSUMIDOR:")
    email = input("Email: ")
    senha = input("Senha: ")
    lista = ler_arquivo("banco_consumidores.txt")  # le todos os consumidores

    encontrou = False
    # percorre cada pessoa pra ver se email e senha batem
    for pessoa in lista:
        if pessoa["Email"] == email and pessoa["Senha"] == senha:
            encontrou = True
            print("Bem-vindo, " + pessoa["Nome"] + "!")
            return pessoa  # retorna os dados da pessoa logada

    if encontrou == False:
        print("Email ou senha incorretos.")
        return None

# lista as empresas disponiveis com filtro por cidade
def listar_empresas():
    print("EMPRESAS DISPONIVEIS:")
    filtro = input("Filtrar por cidade (ou Enter para todas): ")
    lista = ler_arquivo("banco_empresas.txt")

    encontrou = False
    for emp in lista:
        # mostra a empresa se o filtro estiver vazio ou se a cidade bater
        if filtro == "" or emp["Cidade"].lower() == filtro.lower():
            encontrou = True
            print("[" + emp["ID"] + "] " + emp["Nome"] + " - " + emp["Cidade"] + ", " + emp["UF"])
            print("    " + emp["Descricao"])
            print()

    if encontrou == False:
        print("Nenhuma empresa encontrada nessa cidade.")

# consumidor solicita orcamento a uma empresa
def solicitar_orcamento(consumidor_id):
    print("\n=== SOLICITAR ORCAMENTO ===")
    
    # Verifica se a  existe no banco de dados exclusivo para empresas
    
    consumidores = ler_arquivo("banco_consumidores.txt")
    consumidor_atual = None
    for cons in consumidores:
        if cons["ID"] == consumidor_id:
            consumidor_atual = cons
            break
    
    if consumidor_atual is None:
        print("Consumidor nao encontrado.")
        return

    # mostra as empresas disponiveis
    lista = ler_arquivo("banco_empresas.txt")
    for emp in lista:
        print("[" + emp["ID"] + "] " + emp["Nome"] + " - " + emp["Cidade"] + ", " + emp["UF"])
        print("    " + emp["Descricao"])
        print()
    
    escolha = input("Digite o ID da empresa (ou 0 para voltar): ")
    if escolha == "0":
        return
    
    # verifica se a empresa existe
    empresa_escolhida = None
    nome_emp = ""
    for emp in lista:
        if emp["ID"] == escolha:
            empresa_escolhida = emp
            nome_emp = emp["Nome"]
    
    if empresa_escolhida is None:
        print("Empresa nao encontrada.")
        return
    
    
    # verifica se ja existe solicitaçãoo pendente desse consumidor para essa empresa
    if arquivo_existe("banco_solicitacoes.txt"):
        solicitacoes_existentes = ler_arquivo("banco_solicitacoes.txt")
        for sol in solicitacoes_existentes:
            if sol["Consumidor_ID"] == consumidor_id and sol["Empresa_ID"] == escolha and sol["Status"] == "pendente":
                print("Você ja tem uma solicitação pendente para " + nome_emp + ". Aguarde a resposta.")
                return
            

    # Gera um ID para a solicitação de orçamento
    from datetime import datetime
    solicitacoes = ler_arquivo("banco_solicitacoes.txt") if arquivo_existe("banco_solicitacoes.txt") else []
    novo_id = str(proximo_id("banco_solicitacoes.txt"))

    # Monta a solicitação com os dados do consumidor
    solicitacao = {
        "ID": novo_id,
        "Consumidor_ID": consumidor_id,
        "Empresa_ID": escolha,
        "Data_Solicitacao": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Status": "pendente",
        "CEP": consumidor_atual["CEP"],
        "Valor_Conta": consumidor_atual["Valor_Conta"],
        "Tipo_Imovel": consumidor_atual["Tipo_Imovel"]
    }      
    
    # Grava a solicitação no arquivo
    gravar_linha("banco_solicitacoes.txt", solicitacao)

    print("===== Solicitação envida com sucesso =====")
    print(f"Empresa: {empresa_escolhida['Nome']}")
    print(f"Data: {solicitacao['Data_Solicitacao']}")
    print("\n A empresa foi notificada e enviara o orçamento em breve. Fique atento a notificação")
    print("=" * 50)

# Função auxiliar para verificar se um arquivo existe
def arquivo_existe(nome_arquivo):
    try:
        with open(nome_arquivo, "r", encoding="utf-8") as f:
            return True
    except FileNotFoundError:
        return False

# Mostra as coicitacoes de orçamento que o consumidor fez e os status de cada uma
def minhas_solicitacoes(consumidor_id):
    print("SUAS SOLICITACOES DE ORCAMENTO:")

    if not arquivo_existe("banco_solicitacoes.txt"):
        print("Voce ainda nao fez nenhuma solicitação.")
        return
    
    solicitacoes = ler_arquivo("banco_solicitacoes.txt")
    empresas = ler_arquivo("banco_empresas.txt")

    encontrou = False
    for sol in solicitacoes:
        if sol["Consumidor_ID"] == consumidor_id:
            encontrou = True

            # Busca nome da empresa
            nome_emp = "Empresa " + sol["Empresa_ID"]
            for emp in empresas:
                if emp["ID"] == sol["Empresa_ID"]:
                    nome_emp = emp["Nome"]
                    break

            print("[" + sol["ID"] + "] " + nome_emp + " - Status: " + sol["Status"])
            print("    Data: " + sol["Data_Solicitacao"])
            print()

    if encontrou == False:
        print("Você ainda não fez nenhuma solicitação. Solicite um orçamento para receber propostas de empresas.")


# mostra os orcamentos que o consumidor recebeu
def meus_orcamentos(consumidor_id):
    print("SEUS ORCAMENTOS:")

    # Verifica se o arquivo existe
    if not arquivo_existe("banco_orcamentos.txt"):
        print("Voce ainda nao recebeu orcamentos.")
        return
    
    lista = ler_arquivo("banco_orcamentos.txt")
    empresas = ler_arquivo("banco_empresas.txt")

    encontrou = False
    for orc in lista:
        # so mostra orcamentos desse consumidor que estao ativos
        if orc["Consumidor_ID"] == consumidor_id and orc["Status"] == "ativo":
            encontrou = True

            # busca o nome da empresa que enviou esse orcamento
            nome_emp = "Empresa " + orc["Empresa_ID"]
            for emp in empresas:
                if emp["ID"] == orc["Empresa_ID"]:
                    nome_emp = emp["Nome"]

            # printa as informacoes resumidas do orcamento
            print("[" + orc["ID"] + "] " + nome_emp + " - R$ " + orc["Valor_Total"] + " - R$ " + orc["RS_por_Wp"] + "/Wp - " + orc["Potencia_kWp"] + " kWp")
            print("    Paineis: R$ " + orc["Custo_Paineis"] + " | Inversor: R$ " + orc["Custo_Inversor"] + " | Mao obra: R$ " + orc["Custo_Mao_Obra"] + " | Taxas: R$ " + orc["Custo_Taxas"])
            print()

    if encontrou == False:
        print("Você ainda não recebeu orcamentos.")

# funcao principal do projeto - compara 2 ou mais orcamentos lado a lado
def comparar_orcamentos(consumidor_id):
    print("COMPARAR ORCAMENTOS:")
    meus_orcamentos(consumidor_id)  # primeiro mostra os orcamentos disponiveis
    ids = input("Digite os IDs dos orcamentos separados por virgula: ").split(",")

    lista = ler_arquivo("banco_orcamentos.txt")
    empresas = ler_arquivo("banco_empresas.txt")

    # filtra so os orcamentos que o consumidor escolheu
    selecionados = []
    for orc in lista:
        if orc["ID"].strip() in [x.strip() for x in ids] and orc["Consumidor_ID"] == consumidor_id and orc["Status"] == "ativo":
            # busca o nome da empresa
            for emp in empresas:
                if emp["ID"] == orc["Empresa_ID"]:
                    orc["Nome_Empresa"] = emp["Nome"]
            selecionados.append(orc)

    # precisa de exatamente 2 pra comparar
    if len(selecionados) != 2:
        print("Selecione exatamente 2 orcamentos ativos para comparar.")
    else:
        # pega os dois orcamentos (a = primeiro, b = segundo)
        a = selecionados[0]
        b = selecionados[1]
        nome_a = a.get("Nome_Empresa", "Empresa A")
        nome_b = b.get("Nome_Empresa", "Empresa B")

        print("\n" + "=" * 50)
        print("COMPARACAO: " + nome_a + "  x  " + nome_b)
        print("=" * 50)

        # lista de criterios: (nome na tela, campo no arquivo, quem ganha)
        criterios = [
            ("Valor total (R$)", "Valor_Total", "menor"),
            ("R$/Wp", "RS_por_Wp", "menor"),
            ("Potencia (kWp)", "Potencia_kWp", "maior"),
            ("Custo paineis (R$)", "Custo_Paineis", "menor"),
            ("Custo inversor (R$)", "Custo_Inversor", "menor"),
            ("Custo mao de obra (R$)", "Custo_Mao_Obra", "menor"),
            ("Custo taxas (R$)", "Custo_Taxas", "menor")
        ]

        # passa por cada criterio e calcula a diferenca
        for nome, campo, regra in criterios:
            valor_a = float(a[campo])
            valor_b = float(b[campo])
            diferenca = abs(valor_a - valor_b)
            # calcula o percentual da diferenca em cima do menor valor
            menor_valor = min(valor_a, valor_b)
            if menor_valor > 0:
                percentual = round((diferenca / menor_valor) * 100, 1)
            else:
                percentual = 0

            # decide quem ganha nesse criterio
            if valor_a == valor_b:
                melhor = "Empate"
            elif regra == "menor":
                if valor_a < valor_b:
                    melhor = nome_a
                else:
                    melhor = nome_b
            else:
                if valor_a > valor_b:
                    melhor = nome_a
                else:
                    melhor = nome_b

            print("\n" + nome + ":")
            print("  " + nome_a + ": " + str(valor_a) + "  |  " + nome_b + ": " + str(valor_b))
            print("  Diferenca: " + str(round(diferenca, 2)) + " (" + str(percentual) + "%)  ->  Melhor: " + melhor)

        print("\n" + "=" * 50)


# funcao que muda o status de um orcamento pra "removido" no txt
def atualizar_status(orc_id, consumidor_id):
    arquivo = open("banco_orcamentos.txt", "r", encoding="utf-8")
    linhas = arquivo.readlines()
    arquivo.close()

    novas = [linhas[0]]  # mantem o cabecalho
    removeu = False

    for linha in linhas[1:]:
        valores = linha.strip().split(";")
        # verifica se eh o orcamento certo desse consumidor
        if len(valores) > 14 and valores[0] == orc_id and valores[2] == consumidor_id:
            valores[14] = "removido"  # muda o status
            removeu = True
        novas.append(";".join(valores) + "\n")

    # reescreve o arquivo inteiro com a mudanca
    arquivo = open("banco_orcamentos.txt", "w", encoding="utf-8")
    arquivo.writelines(novas)
    arquivo.close()

    if removeu == True:
        print("Orcamento removido!")
    else:
        print("Orcamento nao encontrado.")

# funcao que o consumidor usa pra remover um orcamento da lista
def remover_orcamento(consumidor_id):
    meus_orcamentos(consumidor_id)  # mostra os orcamentos primeiro
    orc_id = input("ID do orcamento para remover: ")
    atualizar_status(orc_id, consumidor_id)