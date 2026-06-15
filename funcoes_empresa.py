# === FUNCOES DA EMPRESA ===
# tudo que a empresa integradora faz no sistema

from funcoes_arquivo import ler_arquivo, gravar_linha,deletar_linha, arquivar_linha ,proximo_id, atualizar_status_solicitacao

def arquivo_existe(nome_arquivo):
    try:
        with open(nome_arquivo, "r") as f:
            return True
    except FileNotFoundError:
        return False

# cadastro de nova empresa, pede os dados e grava no txt
def cadastrar_empresa():
    print("CADASTRO DE EMPRESA:")
    nome = input("Nome da empresa: ")
    cnpj = input("CNPJ: ")
    email = input("Email corporativo: ")
    senha = input("Senha: ")
    cidade = input("Cidade: ")
    uf = input("UF: ")
    desc = input("Descricao curta: ")

    # monta o dicionario com os dados da nova empresa
    novo = {
        "ID": str(proximo_id("banco_empresas.txt")),
        "Nome": nome,
        "CNPJ": cnpj,
        "Email": email,
        "Senha": senha,
        "Cidade": cidade,
        "UF": uf,
        "Descricao": desc
    }
    gravar_linha("banco_empresas.txt", novo)  # grava no arquivo
    print("Empresa cadastrada com sucesso!")

# login da empresa - verifica email e senha no txt de empresas
def login_empresa():
    print("\n=== LOGIN EMPRESA ===")
    email = input("Email: ")
    senha = input("Senha: ")
    lista = ler_arquivo("banco_empresas.txt")

    encontrou = False
    for emp in lista:
        if emp["Email"] == email and emp["Senha"] == senha:
            encontrou = True
            print("Bem-vindo, " + emp["Nome"] + "!")
            return emp  # retorna os dados da empresa logada

    if encontrou == False:
        print("Email ou senha incorretos.")
        return None

# mostra os consumidores cadastrados pra empresa saber pra quem enviar
def ver_consumidores():
    print("CONSUMIDORES CADASTRADOS:")
    lista = ler_arquivo("banco_consumidores.txt")

    if len(lista) == 0:
        print("Nenhum consumidor cadastrado.")
    else:
        for c in lista:
            print("[" + c["ID"] + "] " + c["Nome"] + " - CEP: " + c["CEP"] + " - Conta: R$ " + c["Valor_Conta"] + "/mes - " + c["Tipo_Imovel"])

# mostra as solicitacoes que a empresa recebeu e deixa responder uma delas
def ver_solicitacoes_recebidas(empresa_id):
    print("SOLICITACOES RECEBIDAS:")

    if not arquivo_existe("banco_solicitacoes.txt"):
        print("Nenhuma solicitacao recebida ainda.")
        return

    solicitacoes = ler_arquivo("banco_solicitacoes.txt")
    consumidores = ler_arquivo("banco_consumidores.txt")

    # filtra so as solicitacoes pendentes dessa empresa
    minhas = []
    for sol in solicitacoes:
        if sol["Empresa_ID"] == empresa_id and sol["Status"] == "pendente":
            minhas.append(sol)

    if len(minhas) == 0:
        print("Nenhuma solicitacao pendente.")
        return

    print("Total de solicitacoes pendentes: " + str(len(minhas)))
    print("-" * 50)

    # PASSO 1: mostra a lista inteira, sem interromper
    for sol in minhas:
        # busca o nome do consumidor que enviou a solicitacao
        nome_cons = "Consumidor " + sol["Consumidor_ID"]
        for cons in consumidores:
            if cons["ID"] == sol["Consumidor_ID"]:
                nome_cons = cons["Nome"]
                break

        print("[" + sol["ID"] + "] De: " + nome_cons + " - " + sol["Data_Solicitacao"])
        print("    CEP: " + sol["CEP"] + " | Conta: R$ " + sol["Valor_Conta"] + " | Imovel: " + sol["Tipo_Imovel"])
        print()

    # PASSO 2: pergunta UMA vez se quer responder alguma
    escolha = input("Digite o ID da solicitacao que deseja responder (0 para voltar): ")
    if escolha == "0" or escolha.strip() == "":
        return

    # verifica se o ID digitado esta na lista de pendentes dessa empresa
    solicitacao_escolhida = None
    for sol in minhas:
        if sol["ID"] == escolha:
            solicitacao_escolhida = sol
            break

    if solicitacao_escolhida is None:
        print("Solicitacao nao encontrada.")
    else:
        enviar_orcamento_para_solicitacao(empresa_id, solicitacao_escolhida["Consumidor_ID"], solicitacao_escolhida["ID"])

def enviar_orcamento_para_solicitacao(empresa_id, consumidor_id, solicitacao_id):
        print(f"\n=== RESPONDENDO SOLICITACAO #{solicitacao_id} ===")

        # Busca dados do consumidor
        consumidores = ler_arquivo("banco_consumidores.txt")
        consumidor = None
        for cons in consumidores:
            if cons["ID"] == consumidor_id:
                consumidor = cons
                break
        if consumidor is None:
            print("Consumidor não encontrado.")
            return
        
        print(f"Enviando orçamento para: {consumidor['Nome']}")
        print(f"Dados do consumidor:")
        print(f"CEP: {consumidor['CEP']}")
        print(f"Valor da conta: R$ {consumidor['Valor_Conta']}")
        print(f"Tipo de imóvel: {consumidor['Tipo_Imovel']}")
        
        # Pede os dados técnicos do sistema solar
        print("\nPreencha os dados do orçamento:")
        pot = input("Potência total (kWp): ")
        qtd = input("Qtd painéis: ")
        painel = input("Marca e modelo do painel: ")
        inversor = input("Marca e modelo do inversor: ")
        tipo_inv = input("Tipo inversor (String/Microinversor/Híbrido): ")

        # Pede os 4 custos discriminados
        cp = float(input("Custo painéis (R$): "))
        ci = float(input("Custo inversor (R$): "))
        cm = float(input("Custo mão de obra (R$): "))
        ct = float(input("Custo taxas (R$): "))

        #calcula o valor total e o R$/Wp automaticamente
        total = cp + ci + cm + ct
        rs_wp = round(total / (float(pot) * 1000), 2)

        print(f"\n>>> Valor total calculado: R$ {total}")
        print(f">>> R$/Wp calculado: R$ {rs_wp}")

        # Monta o dicionário do orçamento
        novo_orcamento = {
        "ID": str(proximo_id("banco_orcamentos.txt")),
        "Empresa_ID": empresa_id,
        "Consumidor_ID": consumidor_id,
        "Potencia_kWp": pot,
        "Qtd_Paineis": qtd,
        "Painel": painel,
        "Inversor": inversor,
        "Tipo_Inversor": tipo_inv,
        "Custo_Paineis": str(cp),
        "Custo_Inversor": str(ci),
        "Custo_Mao_Obra": str(cm),
        "Custo_Taxas": str(ct),
        "Valor_Total": str(total),
        "RS_por_Wp": str(rs_wp),
        "Status": "ativo"
       }
        gravar_linha("banco_orcamentos.txt", novo_orcamento)

        # marca a solicitacao como respondida (em vez de deletarr, pra manter o historico)
        atualizar_status_solicitacao(solicitacao_id, "respondido")

        print("\nOrçamento enviado com sucesso!")
        print("A solicitação foi marcada como respondida.")

# funcao onde a empresa preenche e envia um orcamento personalizado
def enviar_orcamento(empresa_id):
    print("\n=== ENVIAR ORCAMENTO ===")

    cancelar = input("Deseja enviar um orçamento livre?(s/n): ")
    if cancelar.lower() != "s":
        print("Orçamento livre cancelado.")
        return

    ver_consumidores()  # mostra os consumidores disponiveis
    cons_id = input("\nPara qual consumidor? (ID): ")

    if cons_id.strip() == "" or cons_id == "0":
        print("ID do consumidor é obrigatório. Orçamento cancelado.")
        return

    # pede os dados tecnicos do sistema solar
    print("\nPreencha os dados do orcamento:")
    pot = input("Potencia total (kWp): ")
    qtd = input("Qtd paineis: ")
    painel = input("Marca e modelo do painel: ")
    inversor = input("Marca e modelo do inversor: ")
    tipo_inv = input("Tipo inversor (String/Microinversor/Hibrido): ")

    # pede os 4 custos discriminados (diferencial do nosso projeto)
    cp = float(input("Custo paineis (R$): "))
    ci = float(input("Custo inversor (R$): "))
    cm = float(input("Custo mao de obra (R$): "))
    ct = float(input("Custo taxas (R$): "))

    # calcula o valor total e o R$/Wp automaticamente
    total = cp + ci + cm + ct
    rs_wp = round(total / (float(pot) * 1000), 2)
    print(">>> Valor total calculado: R$ " + str(total))
    print(">>> R$/Wp calculado: R$ " + str(rs_wp))

    # monta o dicionario do orcamento
    novo = {
    "ID": str(proximo_id("banco_orcamentos.txt")),
    "Empresa_ID": empresa_id,
    "Consumidor_ID": cons_id,
    "Potencia_kWp": pot,
    "Qtd_Paineis": qtd,
    "Painel": painel,
    "Inversor": inversor,
    "Tipo_Inversor": tipo_inv,
    "Custo_Paineis": str(cp),
    "Custo_Inversor": str(ci),
    "Custo_Mao_Obra": str(cm),
    "Custo_Taxas": str(ct),
    "Valor_Total": str(total),
    "RS_por_Wp": str(rs_wp),
    "Status": "ativo"
    }

    gravar_linha("banco_orcamentos.txt", novo)  # grava no arquivo
    print("Orcamento enviado com sucesso!")

# mostra os orcamentos que a empresa ja enviou
def orcamentos_enviados(empresa_id):
    print("ORÇAMENTOS ENVIADOS:")
    lista = ler_arquivo("banco_orcamentos.txt")
    consumidores = ler_arquivo("banco_consumidores.txt")

    encontrou = False
    for orc in lista:
        if orc["Empresa_ID"] == empresa_id:
            encontrou = True
            # busca o nome do consumidor que recebeu
            nome_cons = "Consumidor " + orc["Consumidor_ID"]
            for c in consumidores:
                if c["ID"] == orc["Consumidor_ID"]:
                    nome_cons = c["Nome"]
            print("[" + orc["ID"] + "] Para: " + nome_cons + " - R$ " + orc["Valor_Total"] + " - " + orc["Status"])

    if encontrou == False:
        print("Nenhum orçamento enviado ainda.")