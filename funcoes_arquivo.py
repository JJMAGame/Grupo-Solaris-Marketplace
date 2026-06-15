# FUNCOES DE ARQUIVO: funcoes que leem e escrevem nos arquivos txt

# funcao que le um arquivo txt e transforma numa lista de dicionarios:
def ler_arquivo(nome):
    lista = []  # cria lista vazia pra guardar os registros
    arquivo = open(nome, "r", encoding="utf-8")  # abre o arquivo pra leitura
    linhas = arquivo.readlines()  # le todas as linhas e guarda numa lista
    arquivo.close()  # fecha o arquivo

    # pega a primeira linha (q é o cabecalho) e separa pelo ponto e virgula:
    cabecalho = linhas[0].strip().split(";")

    # percorre todas as linhas a partir da segunda (pula o cabecalho):
    for linha in linhas[1:]:
        if linha.strip() == "":  # se a linha estiver vazia, pula
            continue
        valores = linha.strip().split(";")  # separa os valores pelo ponto e virgula
        registro = {}  # cria um dicionario vazio pra esse registro

        # associa cada campo do cabecalho com o valor correspondente
        for i in range(len(cabecalho)):
            registro[cabecalho[i]] = valores[i]

        lista.append(registro)  # adiciona o dicionario na lista

    return lista  # retorna a lista completa

# função que adiciona uma nova linha no final de um arquivo txt:
def gravar_linha(nome, registro):
    import os

    # Verifica se o arquivo existe
    arquivo_existe = os.path.exists(nome)

    if not arquivo_existe:
        # Cria arquivo com cabeçalho
        cabecalho = list(registro.keys())
        with open(nome, "w", encoding="utf-8") as f:
            f.write(";".join(cabecalho) + "\n")  # Garante a quebra de linha
    else:
        # Le o cabeçalho existente
        with open(nome, "r", encoding="utf-8") as f:
            cabecalho = f.readline().strip().split(";")

    # Monta a linha com os valores
    valores = []
    for campo in cabecalho:
        if campo in registro:
            valores.append(str(registro[campo]))
        else:
            valores.append("")

    linha = ";".join(valores)

    # Adiciona a linha no final
    with open(nome, "a", encoding="utf-8") as f:
        f.write(linha + "\n")  # Garante a quebra de linha no final

def verificar_cabecalho(nome_arquivo, cabecalho_correto):
    try:
        with open(nome_arquivo, "r", encoding="utf-8") as f:
            primeira_linha = f.readline().strip()
        
        if primeira_linha != cabecalho_correto:
            # Se o cabeçalho está errado, recria o arquivo
            with open(nome_arquivo, "w", encoding="utf-8") as f:
                f.write(cabecalho_correto + "\n")
            print(f"Arquivo {nome_arquivo} corrigido!")
            return True
        return False
    except FileNotFoundError:
        # Arquivo não existe, cria com cabeçalho correto
        with open(nome_arquivo, "w", encoding="utf-8") as f:
            f.write(cabecalho_correto + "\n")
        print(f"Arquivo {nome_arquivo} criado!")
        return True

# funcao que descobre o prox ID disponivel:
def proximo_id(nome):
    lista = ler_arquivo(nome)
    if len(lista) == 0:  # se nao tem ninguem cadastrado
        return 1
    else:
        maior = 0
        # percorre todos os registros pra achar o maior ID
        for registro in lista:
            if int(registro["ID"]) > maior:
                maior = int(registro["ID"])
        return maior + 1  # retorna o maior + 1
    
def arquivar_solicitacao_respondida(solicitacao, empresa_nome):
    """Arquiva a solicitação respondida em outro arquivo"""
    try:
        with open("banco_solicitacoes_respondidas.txt", "a", encoding="utf-8") as f:
            from datetime import datetime
            data_resposta = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            linha = f"{solicitacao['ID']};{solicitacao['Consumidor_ID']};{solicitacao['Empresa_ID']};{solicitacao['Data_Solicitacao']};respondida;{data_resposta};{empresa_nome}\n"
            f.write(linha)
    except:
        pass

def deletar_linha(nome_arquivo, id_valor, campo_id="ID"):
    try:
        with open(nome_arquivo, "r", encoding="utf-8") as f:
            linhas = f.readlines()
        
        if len(linhas) == 0:
            print(f"Arquivo {nome_arquivo} está vazio.")
            return False
        
        cabecalho = linhas[0]
        novas_linhas = [cabecalho]
        deletou = False

        for linha in linhas[1:]:
            if linha.strip():
                # Pega o primeiro campo (ID)
                valores = linha.strip().split(";")
                if len(valores) > 0 and valores[0] != str(id_valor):
                    novas_linhas.append(linha)
                else:
                    deletou = True
                    print(f"  -> Linha com ID {id_valor} removida de {nome_arquivo}")
        
        if deletou:
            with open(nome_arquivo, "w", encoding="utf-8") as f:
                f.writelines(novas_linhas)
            return True
        else:
            print(f"  -> ID {id_valor} não encontrado em {nome_arquivo}")
            return False
            
    except FileNotFoundError:
        print(f"Arquivo {nome_arquivo} não encontrado.")
        return False
    except Exception as e:
        print(f"Erro ao deletar linha: {e}")
        return False

def arquivar_linha(nome_arquivo_origem, nome_arquivo_destino, id_valor, campos_extras=None):
    try:
        # Lê o arquivo de origem
        with open(nome_arquivo_origem, "r", encoding="utf-8") as f:
            linhas = f.readlines()
        
        if len(linhas) == 0:
            print(f"Arquivo {nome_arquivo_origem} está vazio.")
            return False
        
        cabecalho_origem = linhas[0].strip().split(";")
        linha_arquivar = None
        novas_linhas = [linhas[0]]

        # Procura a linha com o ID
        for linha in linhas[1:]:
            if linha.strip():
                valores = linha.strip().split(";")
                if len(valores) > 0 and valores[0] == str(id_valor):
                    linha_arquivar = valores
                else:
                    novas_linhas.append(linha)
        
        if linha_arquivar is None:
            print(f"ID {id_valor} não encontrado em {nome_arquivo_origem}")
            return False
        
        # Prepara os dados para o arquivo de destino
        # Verifica se o arquivo de destino existe e tem cabeçalho
        import os
        if not os.path.exists(nome_arquivo_destino):
            # Cria cabeçalho para o arquivo de destino
            with open(nome_arquivo_destino, "w", encoding="utf-8") as f:
                # Cabeçalho básico + campos extras
                cabecalho_destino = cabecalho_origem.copy()
                if campos_extras:
                    for campo in campos_extras.keys():
                        if campo not in cabecalho_destino:
                            cabecalho_destino.append(campo)
                f.write(";".join(cabecalho_destino) + "\n")

        # Lê o cabeçalho do destino
        with open(nome_arquivo_destino, "r", encoding="utf-8") as f:
            cabecalho_destino = f.readline().strip().split(";")
        
        # Monta o dicionário da linha a ser arquivada
        registro = {}
        for i, campo in enumerate(cabecalho_origem):
            if i < len(linha_arquivar):
                registro[campo] = linha_arquivar[i]
        
        # Adiciona campos extras
        if campos_extras:
            for campo, valor in campos_extras.items():
                registro[campo] = valor
        
        # Monta a linha no formato do destino
        valores_destino = []
        for campo in cabecalho_destino:
            if campo in registro:
                valores_destino.append(str(registro[campo]))
            else:
                valores_destino.append("")
        
        linha_destino = ";".join(valores_destino)
        
        # Adiciona a linha no arquivo de destino
        with open(nome_arquivo_destino, "a", encoding="utf-8") as f:
            # Verifica se precisa de quebra de linha
            f.seek(0, 2)  # Vai para o final
            pos = f.tell()
            if pos > 0:
                f.write("\n")
            f.write(linha_destino)
        
        # Reescreve o arquivo de origem sem a linha arquivada
        with open(nome_arquivo_origem, "w", encoding="utf-8") as f:
            f.writelines(novas_linhas)

        print(f"✅ Linha ID {id_valor} arquivada de {nome_arquivo_origem} para {nome_arquivo_destino}")
        return True
        
    except FileNotFoundError:
        print(f"Arquivo {nome_arquivo_origem} ou {nome_arquivo_destino} não encontrado.")
        return False
    except Exception as e:
        print(f"Erro ao arquivar linha: {e}")
        return False


# atualiza o status de uma solicitacao (ex: de "pendente" para "respondido")
def atualizar_status_solicitacao(solicitacao_id, novo_status):
    arquivo = open("banco_solicitacoes.txt", "r", encoding="utf-8")
    linhas = arquivo.readlines()
    arquivo.close()

    novas = [linhas[0]]  # mantem o cabecalho
    atualizou = False

    for linha in linhas[1:]:
        if linha.strip() == "":
            continue
        valores = linha.strip().split(";")
        if valores[0] == solicitacao_id:
            valores[4] = novo_status
            atualizou = True
        novas.append(";".join(valores) + "\n")

    arquivo = open("banco_solicitacoes.txt", "w", encoding="utf-8")
    arquivo.writelines(novas)
    arquivo.close()

    return atualizou