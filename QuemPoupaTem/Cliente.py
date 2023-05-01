from datetime import datetime
from typing import List, Union


class Cliente:
    """
    Classe que representa um cliente e contém métodos para manipulação de dados do cliente
    """

    def __init__(self, razao_social: str, cnpj: str, tipo_de_conta: str, saldo: float, senha: str):
        self.razao_social = razao_social  # Razão social do cliente
        self.cnpj = cnpj  # CNPJ do cliente
        self.tipo_de_conta = tipo_de_conta  # Tipo de conta do cliente
        self.saldo = saldo  # Saldo do cliente
        self.senha = senha  # Senha do cliente

    def getTipoDeConta(self, arquivo) -> Union[str, bool]:

        with open(arquivo, "r") as f:  # Abre o arquivo em modo leitura
            lines = f.readlines()  # Pega todas as linhas do arquivo

        for line in lines:  # Percorre as linhas do arquivo
            partes = line.split(";")  # Divide as linhas em partes
            if partes[1] == self.cnpj:  # Se o CNPJ da linha for igual ao do cliente
                return str(partes[2])  # Retorna o tipo de conta

        return False

    def setSaldo(self, arquivo: str, saldo: float) -> bool:

        with open(arquivo, "r") as f:  # Abre o arquivo em modo leitura
            lines = f.readlines()  # Pega todas as linhas do arquivo

        for i, line in enumerate(
                lines):  # Percorre as linhas do arquivo, utiliza enumerate para pegar o indice da linha
            partes = line.split(";")  # Divide as linhas em partes
            if partes[1] == self.cnpj:  # Se o CNPJ da linha for igual ao do cliente
                partes[3] = str(saldo)  # Atualiza o saldo do cliente
                lines[i] = ";".join(partes)  # Reescreve a linha com o saldo atualizado
                self.saldo = saldo  # Atualiza o saldo do cliente

        with open(arquivo, "w") as f:  # Abre o arquivo em modo escrita
            f.writelines(lines)  # Reescreve as linhas com o saldo atualizado

        return True if self.saldo == saldo else False  # Retorna True se o saldo for atualizado

    def getSaldo(self, arquivo: str) -> float:
        with open(arquivo, "r") as f:  # Abre o arquivo em modo leitura
            lines = f.readlines()  # Pega todas as linhas do arquivo

        for line in lines:  # Percorre as linhas do arquivo
            partes = line.split(";")  # Divide as linhas em partes
            if partes[1] == self.cnpj:  # Se o CNPJ da linha for igual ao do cliente
                return float(partes[3])  # Retorna o saldo do cliente

        return False

    def salvarCliente(self, arquivo: str):
        with open(arquivo, "a") as f:  # Abre o arquivo em modo escrita
            f.write(
                f"{self.razao_social};{self.cnpj};{self.tipo_de_conta};{self.saldo};{self.senha}\n")  # Escreve o cliente no arquivo

    def removerCliente(self, arquivo: str):
        with open(arquivo, "r") as f:  # Abre o arquivo em modo leitura
            lines = f.readlines()  # Pega todas as linhas do arquivo

        with open(arquivo, "w") as f:  # Abre o arquivo em modo escrita
            cliente_encontrado = False  # Variável que indica se o cliente foi encontrado
            for line in lines:  # Percorre as linhas do arquivo
                if line.split(";")[1] == self.cnpj:  # Se o CNPJ da linha for igual ao do cliente
                    cliente_encontrado = True  # Atualiza a variável indicando que o cliente foi encontrado
                    continue  # Sai do laço
                f.write(line)  # Escreve a linha no arquivo

            if cliente_encontrado:  # Se o cliente foi encontrado
                print("Cliente removido com sucesso!")  # Exibe mensagem de sucesso
            else:
                print("Cliente não encontrado.")

    def listarClientes(self, arquivo: str) -> List['Cliente']:
        clientes = []  # Lista de clientes
        with open(arquivo, "r") as f:  # Abre o arquivo em modo leitura
            for line in f:  # Percorre as linhas do arquivo
                if not line.strip():  # Se a linha não estiver vazia
                    continue  # Sai do laço
                parts = line.strip().split(";")  # Divide as linhas em partes
                cliente = Cliente(parts[0], parts[1], parts[2], float(parts[3]), parts[4])  # Cria um cliente
                clientes.append(cliente)  # Adiciona o cliente na lista de clientes
        return clientes  # Retorna a lista de clientes

    def verificaCNPJ(self, arquivo: str) -> bool:
        with open(arquivo, "r") as f:  # Abre o arquivo em modo leitura
            lines = f.readlines()  # Pega todas as linhas do arquivo

        for line in lines:  # Percorre as linhas do arquivo
            if line.split(";")[1] == self.cnpj:  # Se o CNPJ da linha for igual ao do cliente
                return True  # Retorna True

        return False

    def verificaSenha(self, arquivo: str, senha: str) -> bool:
        with open(arquivo, "r") as f:  # Abre o arquivo em modo leitura
            lines = f.readlines()  # Pega todas as linhas do arquivo

        for line in lines:
            partes = line.strip().split(";")  # Divide as linhas em partes, utiliza strip para remover os espaços
            if partes[1] == self.cnpj and partes[
                4] == senha:  # Se o CNPJ da linha for igual ao do cliente e a senha for igual a informada
                return True  # Retorna True

        return False

    def debito(self, arquivo: str, valor: float, registro: bool = True, taxa: bool = True) -> bool:
        saldo = self.getSaldo(arquivo)  # Pega o saldo do cliente

        if self.getTipoDeConta(arquivo) == "comum":  # Se o tipo de conta for comum
            valor = valor + valor * 0.05 if taxa else valor  # Calcula o valor com taxa se taxa = True
            saldo -= valor  # Subtrai o valor do saldo do cliente
            if saldo < -1000:  # Se o saldo for menor que -1000
                return False  # Retorna False

        if self.getTipoDeConta(arquivo) == "plus":  # Se o tipo de conta for plus
            valor = valor + valor * 0.07 if taxa else valor  # Calcula o valor com taxa se taxa = True
            saldo -= valor  # Subtrai o valor do saldo do cliente
            if saldo < -5000:  # Se o saldo for menor que -5000
                return False  # Retorna False

        if self.setSaldo(arquivo, saldo):  # Se o saldo for alterado com sucesso
            if registro:  # Se registro = True
                self.registrarOperacao("debito", valor, self.cnpj)  # Registra a operação no arquivo de operaçãe
            return True  # Retorna True
        return False

    def deposito(self, arquivo: str, valor: float, registro: bool = True) -> bool:
        saldo = self.getSaldo(arquivo)  # Pega o saldo do cliente
        saldo += valor  # Soma o valor ao saldo do cliente

        if self.setSaldo(arquivo, saldo):  # Se o saldo for alterado com sucesso
            if registro:  # Se registro = True
                self.registrarOperacao("deposito", valor, self.cnpj)  # Registra a operação no arquivo de operaçãe
            return True  # Retorna True
        return False

    def transferencia(self, arquivo: str, cnpj_destino: str, valor: float) -> bool:
        cnpj_origem = self.cnpj  # Obtém o CNPJ do cliente
        if self.debito(arquivo, valor, registro=False, taxa=False):  # Se o cliente debitar o valor com sucesso
            self.registrarOperacao(f"Transf. para {cnpj_destino}", valor,
                                   cnpj_origem)  # Registra a operação no arquivo de operaçãe
            for cliente in self.listarClientes(arquivo):  # Percorre a lista de clientes
                if cliente.cnpj == cnpj_destino:  # Se o CNPJ do cliente for igual ao do destino
                    if cliente.deposito(arquivo, valor, registro=False):  # Se o cliente depositar o valor com sucesso
                        self.registrarOperacao(f"Transf. de {cnpj_origem}", valor,
                                               cnpj_destino)  # Registra a operação no arquivo de operaçãe
                        return True  # Retorna True
                    else:  # Se o cliente não depositar o valor com sucesso
                        self.deposito(arquivo, valor, registro=False)  # Retorna o saldo do cliente
                        return False  # Retorna False

        return False

    def registrarOperacao(self, tipoOperacao: str, valor: float, cnpj: str):
        dataHora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Obtem data e hora atuais

        with open("operacoes.txt", "a") as arquivo:  # Adiciona a operação ao arquivo de operações

            arquivo.write(
                f"{cnpj};{dataHora};{tipoOperacao};{valor}\n")  # Escreve informações no formato cnpj;data_hora;tipo_de_operacao;valor

    def exibirOperacoes(self):
        with open("operacoes.txt", "r") as arquivo:  # Abre o arquivo em modo leitura
            for line in arquivo:  # Percorre as linhas do arquivo
                if not line.strip():  # Se a linha não estiver vazia
                    continue  # Sai do laço
                if line.split(";")[0] == self.cnpj:  # Se o CNPJ da linha for igual ao do cliente
                    print(f"{line.split(';')[1]} :"  # Exibe a data e hora
                          f"\t{line.split(';')[2].ljust(20)} -> "  # Exibe o tipo de operação, usa ljust para alinhar
                          f"R${line.split(';')[3]}")  # Exibe a operação

    def __str__(self):
        return (
            "\n{\n"
            f"Razão social:\t{self.razao_social}\n"
            f"CNPJ:\t\t{self.cnpj}\n"
            f"Tipo de conta:\t{self.tipo_de_conta}\n"
            f"Saldo:\t\tR${self.saldo}"
            "\n}\n"
        )
