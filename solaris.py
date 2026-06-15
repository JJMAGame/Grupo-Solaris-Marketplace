# importa as funcoes dos outros arquivos
from funcoes_empresa import cadastrar_empresa, login_empresa, enviar_orcamento, orcamentos_enviados, ver_consumidores, ver_solicitacoes_recebidas
from funcoes_consumidor import cadastrar_consumidor, login_consumidor, listar_empresas, meus_orcamentos, comparar_orcamentos, remover_orcamento, buscar_e_solicitar, minhas_solicitacoes, contar_overview, hub_orcamentos
from funcoes_arquivo import verificar_cabecalho


# menu do consumidor que aparece depois que ele faz login
def menu_consumidor(usuario):
    while True:
        qtd_orc, qtd_pend = contar_overview(usuario["ID"])
        print("\n" + "-" * 40)
        print("  Olá, " + usuario["Nome"] + "!")
        print("  Orçamentos recebidos: " + str(qtd_orc) + "  |  Solicitações pendentes: " + str(qtd_pend))
        if qtd_orc >= 2:
            print(" Você já pode comparar orçamentos! ")
        print("-" * 40)
        print("  1. Ver empresas e solicitar orçamento")
        print("  2. Minhas solicitações")
        print("  3. Meus orçamentos")
        print("  4. Comparar orçamentos")
        print("  5. Remover orçamento")
        print("  0. Sair da conta")
        opcao = input("Escolha: ")
        if opcao == "1":
            buscar_e_solicitar(usuario["ID"])
        elif opcao == "2":
            minhas_solicitacoes(usuario["ID"])
        elif opcao == "3":
            hub_orcamentos(usuario["ID"])
        elif opcao == "4":
            comparar_orcamentos(usuario["ID"])
        elif opcao == "5":
            remover_orcamento(usuario["ID"])
        elif opcao == "0":
            print("Saindo da conta...")
            break
        else:
            print("Opção inválida. Tente novamente.")

# menu da empresa que aparece depois que ela faz login
def menu_empresa(empresa):
    while True:
        print("\n--------------------------------------")
        print("  Painel: " + empresa["Nome"])
        print("----------------------------------------")
        print("  1. Ver solicitações recebidas")
        print("  2. Orçamentos enviados")
        print("  0. Sair da conta")
        opcao = input("Escolha: ")
        if opcao == "1":
            ver_solicitacoes_recebidas(empresa["ID"])
        elif opcao == "2":
            orcamentos_enviados(empresa["ID"])
        elif opcao == "0":
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")

# menu principal - primeira tela do sistema
def menu_principal():
    while True:
        print("\n----------------------------------------")
        print("  BEM-VINDO AO SOLARIS")
        print("  Marketplace de Energia Solar")
        print("----------------------------------------")
        print("  1. Entrar como consumidor")
        print("  2. Entrar como empresa")
        print("  3. Cadastrar")
        print("  0. Sair")
        opcao = input("Escolha: ")
        if opcao == "1":
            usuario = login_consumidor()
            if usuario != None:  # se o login deu certo
                menu_consumidor(usuario)
        elif opcao == "2":
            empresa = login_empresa()
            if empresa != None:  # se o login deu certo
                menu_empresa(empresa)
        elif opcao == "3":
            print("  1. Sou consumidor")
            print("  2. Sou empresa")
            tipo = input("Escolha: ")
            if tipo == "1":
                cadastrar_consumidor()
            elif tipo == "2":
                cadastrar_empresa()
            else:
                print("Opcao invalida.")
        elif opcao == "0":
            print("Obrigado por usar o Solaris!")
            break
        else:
            print("Opcao invalida. Tente novamente.")

# inicia o programa
menu_principal()