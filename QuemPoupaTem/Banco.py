import Cliente


class Banco:
    def __init__(self):
        self.arquivo = "clientes.txt" # nome do arquivo onde os dados serão armazenados
        open(self.arquivo, "a") # cria o arquivo caso ele não exista

    def novoCliente(self):
        razao_social = input("Razão Social: ") # recebe a razão social do cliente
        cnpj = input("CNPJ: ") # recebe o CNPJ do cliente
        tipo_de_conta = input("Tipo de Conta (comum/plus): ") # recebe o tipo de conta do cliente
        while tipo_de_conta not in ["comum", "plus"]: # verifica se o tipo de conta é válido
            print("Tipo de conta inválido. Deve ser comum ou plus.")
            tipo_de_conta = input("Tipo de Conta (comum/plus): ") # solicita novamente o tipo de conta
        saldo_inicial = input("Saldo Inicial: ") # recebe o saldo inicial do cliente
        while not saldo_inicial.isnumeric(): # verifica se o saldo inicial é válido
            print("Saldo inválido. Deve ser um valor numérico, sem pontuação.")
            saldo_inicial = input("Saldo Inicial: ") # solicita novamente o saldo inicial
        saldo_inicial = float(saldo_inicial) # converte o saldo inicial para float
        senha = input("Senha: ") # recebe a senha do cliente
        cliente = Cliente.Cliente(razao_social, cnpj, tipo_de_conta, saldo_inicial, senha) # cria um novo cliente com os dados recebidos
        cliente.salvarCliente(self.arquivo) # salva o cliente no arquivo
        print("Cliente cadastrado com sucesso!")
        print(cliente)

    def apagarCliente(self):
        cnpj = input("CNPJ do cliente a ser apagado: ") # recebe o CNPJ do cliente a ser apagado
        cliente = Cliente.Cliente("", cnpj, "", 0, "") # cria um novo cliente com os dados recebidos
        cliente.removerCliente(self.arquivo) # remove o cliente do arquivo

    def listarClientes(self):
        cliente = Cliente.Cliente("", "", "", 0, "") # cria um novo cliente vazio
        lista_de_clientes = cliente.listarClientes(self.arquivo) # lista todos os clientes do arquivo
        for cliente in lista_de_clientes: # imprime todos os clientes da lista
            print(cliente)

    def debito(self):
        cnpj = input("CNPJ do cliente: ") # recebe o CNPJ do cliente
        cliente = Cliente.Cliente("", cnpj, "", 0, "") # cria um novo cliente com os dados recebidos
        while not cliente.verificaCNPJ(self.arquivo): # verifica se o CNPJ é válido
            print("CNPJ inválido. Tente novamente.")
            cnpj = input("CNPJ do cliente: ")
            cliente = Cliente.Cliente("", cnpj, "", 0, "") # solicita novamente o CNPJ

        senha = input("Senha: ")

        while not cliente.verificaSenha(self.arquivo, senha): # verifica se a senha é válida para o cliente
            print(f"Senha inválida para o CNPJ {cnpj}. Tente novamente.")
            senha = input("Senha: ") # solicita novamente a senha
        print(f"Saldo atual: {cliente.getSaldo(self.arquivo)}")
        valor = input("Valor a ser debitado: ")
        while not valor.isnumeric(): # verifica se o valor é válido para o cliente
            print("Valor inválido. Deve ser um valor numérico, sem pontuação.")
            valor = input("Valor: ")
        if cliente.debito(self.arquivo, float(valor)):
            print(f"Débito realizado com sucesso! Saldo atual:{cliente.getSaldo(self.arquivo)}")

    def deposito(self):
        cnpj = input("CNPJ do cliente: ") # recebe o CNPJ do cliente
        cliente = Cliente.Cliente("", cnpj, "", 0, "") # cria um novo cliente com os dados recebidos
        while not cliente.verificaCNPJ(self.arquivo): # verifica se o CNPJ é válido
            print("CNPJ inválido. Tente novamente.")
            cnpj = input("CNPJ do cliente: ")
            cliente = Cliente.Cliente("", cnpj, "", 0, "") # solicita novamente o CNPJ
        print(f"Saldo atual: {cliente.getSaldo(self.arquivo)}")
        valor = input("Valor a ser depositado: ")
        while not valor.isnumeric(): # verifica se o valor é válido para o cliente
            print("Valor inválido. Deve ser um valor numérico, sem pontuação.")
            valor = input("Valor: ")

        cliente.deposito(self.arquivo, float(valor)) # deposita o valor no saldo do cliente
        print(f"Depósito realizado com sucesso! Saldo atual: {cliente.getSaldo(self.arquivo)}") # imprime o saldo atual do cliente

    def transferencia(self):
        cnpj_origem = input("CNPJ do cliente de origem: ") # recebe o CNPJ do cliente de origem
        cliente = Cliente.Cliente("", cnpj_origem, "", 0, "") # cria um novo cliente com os dados recebidos
        while not cliente.verificaCNPJ(self.arquivo): # verifica se o CNPJ é válido
            print("CNPJ inválido. Tente novamente.")
            cnpj_origem = input("CNPJ do cliente: ")
            cliente = Cliente.Cliente("", cnpj_origem, "", 0, "") # solicita novamente o CNPJ

        senha = input("Senha: ")

        while not cliente.verificaSenha(self.arquivo, senha): # verifica se a senha é válida para o cliente
            print(f"Senha inválida para o CNPJ {cnpj_origem}. Tente novamente.")
            senha = input("Senha: ")

        cnpj_destino = input("CNPJ do cliente de destino: ") # recebe o CNPJ do cliente de destino
        cliente_destino = Cliente.Cliente("", cnpj_destino, "", 0, "") # cria um novo cliente com os dados recebidos
        while not cliente_destino.verificaCNPJ(self.arquivo): # verifica se o CNPJ é válido
            print("CNPJ inválido. Tente novamente.")
            cnpj_destino = input("CNPJ do cliente: ")
            cliente_destino = Cliente.Cliente("", cnpj_destino, "", 0, "") # solicita novamente o CNPJ

        valor = input("Valor a ser transferido: ") # recebe o valor a ser transferido
        while not valor.isnumeric(): # verifica se o valor é válido para o cliente
            print("Valor inválido. Deve ser um valor numérico, sem pontuação.")
            valor = input("Valor: ")

        if cliente.transferencia(self.arquivo, cnpj_destino, float(valor)): # verifica se a transferencia foi realizada com sucesso
            print(f"Transferência realizada com sucesso!")


    def extrato(self):
        cnpj = input("CNPJ do cliente: ") # recebe o CNPJ do cliente
        cliente = Cliente.Cliente("", cnpj, "", 0, "") # cria um novo cliente com os dados recebidos
        while not cliente.verificaCNPJ(self.arquivo): # verifica se o CNPJ é válido
            print("CNPJ inválido. Tente novamente.")
            cnpj = input("CNPJ do cliente: ")
            cliente = Cliente.Cliente("", cnpj, "", 0, "") # solicita novamente o CNPJ

        senha = input("Senha: ") # recebe a senha do cliente
        while not cliente.verificaSenha(self.arquivo, senha): # verifica se a senha é válida para o cliente
            print(f"Senha inválida para o CNPJ {cnpj}. Tente novamente.")
            senha = input("Senha: ") # solicita novamente a senha

        print(f"Extrato do cliente de CNPJ {cnpj}:") # imprime o extrato do cliente
        print(f"Saldo Total: R${cliente.getSaldo(self.arquivo)}") # imprime o saldo total do cliente
        cliente.exibirOperacoes() # imprime todas as operaçães realizadas pelo cliente

