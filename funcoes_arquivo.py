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
    # abre o arquivo so pra ler o cabecalho e saber a ordem dos campos
    arquivo = open(nome, "r", encoding="utf-8")
    cabecalho = arquivo.readline().strip().split(";")
    conteudo = arquivo.read()  # le o resto do arquivo
    arquivo.close()

    # monta a linha com os valores na ordem certa:
    valores = []
    for campo in cabecalho:
        # Verifica se o campo existe no registro
        if campo in registro:
            valores.append(str(registro[campo]))
        else:
            # Se não existir, adiciona vazio (evita KeyError)
            valores.append("")
            print(f"Aviso: Campo '{campo}' não encontrado no registro!")
    linha = ";".join(valores)
    
    # abre o arquivo em modo append (adiciona no final sem apagar):
    arquivo = open(nome, "a", encoding="utf-8")
    if conteudo != "" and conteudo[-1] != "\n":
        arquivo.write("\n")
    arquivo.write(linha + "\n")
    arquivo.close()

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