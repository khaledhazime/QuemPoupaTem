from datetime import datetime
from typing import List, Union


class Cliente:
    """
    Classe que representa um cliente.
    """

    def __init__(self, razao_social: str, cnpj: str, tipo_de_conta: str, saldo: float, senha: str):
        self.razao_social = razao_social
        self.cnpj = cnpj
        self.tipo_de_conta = tipo_de_conta
        self.saldo = saldo
        self.senha = senha


    def getTipoDeConta(self, arquivo) -> Union[str, bool]:
        with open(arquivo, "r") as f:
            lines = f.readlines()

        for line in lines:
            partes = line.split(";")
            if partes[1] == self.cnpj:
                return str(partes[2])

        return False

    def setSaldo(self, arquivo: str, saldo: float) -> bool:
        # Abre o arquivo em modo leitura
        with open(arquivo, "r") as f:
            lines = f.readlines()

        # Percorre as linhas do arquivo
        for i, line in enumerate(lines):
            partes = line.split(";")
            if partes[1] == self.cnpj:
                # Altera o saldo na linha correspondente
                partes[3] = str(saldo)
                lines[i] = ";".join(partes)
                self.saldo = saldo

        # Abre o arquivo em modo escrita e reescreve as linhas com o saldo atualizado
        with open(arquivo, "w") as f:
            f.writelines(lines)

        return True if self.saldo == saldo else False

    def getSaldo(self, arquivo: str) -> float:
        with open(arquivo, "r") as f:
            lines = f.readlines()

        for line in lines:
            partes = line.split(";")
            if partes[1] == self.cnpj:
                return float(partes[3])

        return False

    def salvarCliente(self, arquivo: str):
        with open(arquivo, "a") as f:
            f.write(f"{self.razao_social};{self.cnpj};{self.tipo_de_conta};{self.saldo};{self.senha}\n")

    def removerCliente(self, arquivo: str):
        with open(arquivo, "r") as f:
            lines = f.readlines()

        with open(arquivo, "w") as f:
            cliente_encontrado = False
            for line in lines:
                if line.split(";")[1] == self.cnpj:
                    cliente_encontrado = True
                    continue
                f.write(line)

            if cliente_encontrado:
                print("Cliente removido com sucesso!")
            else:
                print("Cliente não encontrado.")

    def listarClientes(self, arquivo: str) -> List['Cliente']:
        clientes = []
        with open(arquivo, "r") as f:
            for line in f:
                if not line.strip():
                    continue
                parts = line.strip().split(';')
                cliente = Cliente(parts[0], parts[1], parts[2], float(parts[3]), parts[4])
                clientes.append(cliente)
        return clientes

    def verificaCNPJ(self, arquivo: str) -> bool:
        with open(arquivo, "r") as f:
            lines = f.readlines()

        for line in lines:
            if line.split(";")[1] == self.cnpj:
                return True

        return False

    def verificaSenha(self, arquivo: str, senha: str) -> bool:
        with open(arquivo, "r") as f:
            lines = f.readlines()

        for line in lines:
            partes = line.strip().split(";")
            if partes[1] == self.cnpj and partes[4] == senha:
                return True

        return False

    def debito(self, arquivo: str, valor: float, registro: bool = True, taxa: bool = True) -> bool:
        saldo = self.getSaldo(arquivo)

        if self.getTipoDeConta(arquivo) == "comum":
            valor = valor + valor * 0.05 if taxa else valor
            saldo -= valor
            if saldo < -1000:
                return False
        if self.getTipoDeConta(arquivo) == "plus":
            valor = valor + valor * 0.03 if taxa else valor
            saldo -= valor
            if saldo < -5000:
                return False

        if self.setSaldo(arquivo, saldo):
            if registro:
                self.registrarOperacao("debito", valor, self.cnpj)
            return True
        return False

    def deposito(self, arquivo: str, valor: float, registro: bool = True) -> bool:
        saldo = self.getSaldo(arquivo)
        saldo += valor

        if self.setSaldo(arquivo, saldo):
            if registro:
                self.registrarOperacao("deposito", valor, self.cnpj)
            return True

        return False

    def transferencia(self, arquivo: str, cnpj_destino: str, valor: float) -> bool:
        cnpj_origem = self.cnpj
        if self.debito(arquivo, valor, registro=False, taxa=False):
            self.registrarOperacao(f"Transf. para {cnpj_destino}", valor,  cnpj_origem)
            for cliente in self.listarClientes(arquivo):
                if cliente.cnpj == cnpj_destino:
                    if cliente.deposito(arquivo, valor, registro=False):
                        self.registrarOperacao(f"Transf. de {cnpj_origem}", valor, cnpj_destino)
                        return True
                    else:
                        self.deposito(arquivo, valor, registro=False)
                        return False

        return False

    def registrarOperacao(self, tipoOperacao: str, valor: float, cnpj: str):
        # Obter data e hora atuais
        dataHora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Adicionar a operação ao arquivo de operações
        with open("operacoes.txt", "a") as arquivo:
            # Escrever informações no formato cnpj;data_hora;tipo_de_operacao;valor
            arquivo.write(f"{cnpj};{dataHora};{tipoOperacao};{valor}\n")

    def exibirOperacoes(self):
        with open("operacoes.txt", "r") as arquivo:
            for line in arquivo:
                if line.split(";")[0] == self.cnpj:
                    print(f"{line.split(';')[1]} :"
                          f"\t{line.split(';')[2].ljust(20)} -> "
                          f"R${line.split(';')[3]}")

    def __str__(self):
        return (
            "\n{\n"
            f"Razão social:\t{self.razao_social}\n"
            f"CNPJ:\t\t{self.cnpj}\n"
            f"Tipo de conta:\t{self.tipo_de_conta}\n"
            f"Saldo:\t\tR${self.saldo}"
            "\n}\n"
        )
