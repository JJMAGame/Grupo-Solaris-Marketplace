
# importa as funcoes dos outros arquivos
from funcoes_consumidor import cadastrar_consumidor, login_consumidor, listar_empresas, meus_orcamentos, comparar_orcamentos, remover_orcamento
from funcoes_empresa import cadastrar_empresa, login_empresa, enviar_orcamento, orcamentos_enviados, ver_consumidores
from funcoes_consumidor import cadastrar_consumidor, login_consumidor, listar_empresas, meus_orcamentos, comparar_orcamentos, remover_orcamento, solicitar_orcamento

# menu do consumidor que aparece depois que ele faz login
def menu_consumidor(usuario):
    while True:
        print("\n" + "-" * 40)
        print("  Ola, " + usuario["Nome"] + "!")
        print("-" * 40)
        print("  1. Buscar empresas")
        print("  2. Solicitar orcamento")
        print("  3. Meus orcamentos")
        print("  4. Comparar orcamentos")
        print("  5. Remover orcamento")
        print("  0. Sair da conta")
        opcao = input("Escolha: ")
        if opcao == "1":
            listar_empresas()
        elif opcao == "2":
            solicitar_orcamento(usuario["ID"])
        elif opcao == "3":
            meus_orcamentos(usuario["ID"])
        elif opcao == "4":
            comparar_orcamentos(usuario["ID"])
        elif opcao == "5":
            remover_orcamento(usuario["ID"])
        elif opcao == "0":
            print("Saindo da conta...")
            break
        else:
            print("Opcao invalida. Tente novamente.")

# menu da empresa que aparece depois que ela faz login
def menu_empresa(empresa):
    while True:
        print("\n----------------------------------------")
        print("  Painel: " + empresa["Nome"])
        print("----------------------------------------")
        print("  1. Ver consumidores")
        print("  2. Enviar orcamento")
        print("  3. Orcamentos enviados")
        print("  0. Sair da conta")
        opcao = input("Escolha: ")
        if opcao == "1":
            ver_consumidores()
        elif opcao == "2":
            enviar_orcamento(empresa["ID"])
        elif opcao == "3":
            orcamentos_enviados(empresa["ID"])
        elif opcao == "0":
            print("Saindo...")
            break
        else:
            print("Opcao invalida. Tente novamente.")

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

# Uma comentario legal para testar o commit
menu_principal()