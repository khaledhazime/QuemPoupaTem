import Cliente


class Banco:
    def __init__(self):
        self.arquivo = "clientes.txt"
        open(self.arquivo, "a")

    def novoCliente(self):
        razao_social = input("Razão Social: ")
        cnpj = input("CNPJ: ")
        tipo_de_conta = input("Tipo de Conta (comum/plus): ")
        while tipo_de_conta not in ["comum", "plus"]:
            print("Tipo de conta inválido. Deve ser comum ou plus.")
            tipo_de_conta = input("Tipo de Conta (comum/plus): ")
        saldo_inicial = input("Saldo Inicial: ")
        while not saldo_inicial.isnumeric():
            print("Saldo inválido. Deve ser um valor numérico, sem pontuação.")
            saldo_inicial = input("Saldo Inicial: ")
        saldo_inicial = float(saldo_inicial)
        senha = input("Senha: ")
        cliente = Cliente.Cliente(razao_social, cnpj, tipo_de_conta, saldo_inicial, senha)
        cliente.salvarCliente(self.arquivo)
        print("Cliente cadastrado com sucesso!")
        print(cliente)

    def apagarCliente(self):
        cnpj = input("CNPJ do cliente a ser apagado: ")
        cliente = Cliente.Cliente("", cnpj, "", 0, "")
        cliente.removerCliente(self.arquivo)

    def listarClientes(self):
        cliente = Cliente.Cliente("", "", "", 0, "")
        lista_de_clientes = cliente.listarClientes(self.arquivo)
        for cliente in lista_de_clientes:
            print(cliente)

    def debito(self):
        cnpj = input("CNPJ do cliente: ")
        cliente = Cliente.Cliente("", cnpj, "", 0, "")
        while not cliente.verificaCNPJ(self.arquivo):
            print("CNPJ inválido. Tente novamente.")
            cnpj = input("CNPJ do cliente: ")
            cliente = Cliente.Cliente("", cnpj, "", 0, "")

        senha = input("Senha: ")

        while not cliente.verificaSenha(self.arquivo, senha):
            print(f"Senha inválida para o CNPJ {cnpj}. Tente novamente.")
            senha = input("Senha: ")
        print(f"Saldo atual: {cliente.getSaldo(self.arquivo)}")
        valor = input("Valor a ser debitado: ")
        while not valor.isnumeric():
            print("Valor inválido. Deve ser um valor numérico, sem pontuação.")
            valor = input("Valor: ")
        if cliente.debito(self.arquivo, float(valor)):
            print(f"Débito realizado com sucesso! Saldo atual:{cliente.getSaldo(self.arquivo)}")

    def deposito(self):
        cnpj = input("CNPJ do cliente: ")
        cliente = Cliente.Cliente("", cnpj, "", 0, "")
        while not cliente.verificaCNPJ(self.arquivo):
            print("CNPJ inválido. Tente novamente.")
            cnpj = input("CNPJ do cliente: ")
            cliente = Cliente.Cliente("", cnpj, "", 0, "")
        print(f"Saldo atual: {cliente.getSaldo(self.arquivo)}")
        valor = input("Valor a ser depositado: ")
        while not valor.isnumeric():
            print("Valor inválido. Deve ser um valor numérico, sem pontuação.")
            valor = input("Valor: ")

        cliente.deposito(self.arquivo, float(valor))
        print(f"Depósito realizado com sucesso! Saldo atual: {cliente.getSaldo(self.arquivo)}")

    def transferencia(self):
        cnpj_origem = input("CNPJ do cliente de origem: ")
        cliente = Cliente.Cliente("", cnpj_origem, "", 0, "")
        while not cliente.verificaCNPJ(self.arquivo):
            print("CNPJ inválido. Tente novamente.")
            cnpj = input("CNPJ do cliente: ")
            cliente = Cliente.Cliente("", cnpj_origem, "", 0, "")

        senha = input("Senha: ")

        while not cliente.verificaSenha(self.arquivo, senha):
            print(f"Senha inválida para o CNPJ {cnpj_origem}. Tente novamente.")
            senha = input("Senha: ")

        cnpj_destino = input("CNPJ do cliente de destino: ")
        cliente_destino = Cliente.Cliente("", cnpj_destino, "", 0, "")
        while not cliente_destino.verificaCNPJ(self.arquivo):
            print("CNPJ inválido. Tente novamente.")
            cnpj = input("CNPJ do cliente: ")
            cliente_destino = Cliente.Cliente("", cnpj_destino, "", 0, "")

        valor = input("Valor a ser transferido: ")
        while not valor.isnumeric():
            print("Valor inválido. Deve ser um valor numérico, sem pontuação.")
            valor = input("Valor: ")

        if cliente.transferencia(self.arquivo, cnpj_destino, float(valor)):
            print(f"Transferência realizada com sucesso!")


    def extrato(self):
        cnpj = input("CNPJ do cliente: ")
        cliente = Cliente.Cliente("", cnpj, "", 0, "")
        while not cliente.verificaCNPJ(self.arquivo):
            print("CNPJ inválido. Tente novamente.")
            cnpj = input("CNPJ do cliente: ")
            cliente = Cliente.Cliente("", cnpj, "", 0, "")

        senha = input("Senha: ")
        while not cliente.verificaSenha(self.arquivo, senha):
            print(f"Senha inválida para o CNPJ {cnpj}. Tente novamente.")
            senha = input("Senha: ")

        print(f"Extrato do cliente de CNPJ {cnpj}:")
        print(f"Saldo Total: R${cliente.getSaldo(self.arquivo)}")
        cliente.exibirOperacoes()

