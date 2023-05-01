import Banco
import os

class Menu:
    def __init__(self):
        self.banco = Banco.Banco()
        self.opcoes = {
            "1": ("Adicionar cliente", self.adicionarCliente),
            "2": ("Apagar cliente (CNPJ)", self.apagarCliente),
            "3": ("Listar clientes", self.listarClientes),
            "4": ("Débito em conta", self.debito),
            "5": ("Depósito em conta", self.deposito),
            "6": ("Extrato", self.extrato),
            "7": ("Transferência", self.transferencia),
            "0": ("Sair", self.sair)
        }
        self.confirmar_saida = {
            "1": ("Sim", self.exibir),
            "2": ("Encerrar o programa", self.sair)
        }

    def exibir(self):
        while True:
            self.limparTela()
            print("Bem-vindo ao Banco QuemPoupaTem!\n")
            for opcao, descricao in self.opcoes.items():
                print(f"{opcao}. {descricao[0]}")
            escolha = input("\nEscolha uma opção: ")
            if escolha in self.opcoes:
                self.opcoes[escolha][1]()
            else:
                input("Opção inválida! Pressione Enter para continuar...")

    def limparTela(self):
        os.system('clear')

    def confirmarSaida(self):
        print("Deseja retornar ao menu principal?")
        for opcao, descricao in self.confirmar_saida.items():
            print(f"{opcao}. {descricao[0]}")
        escolha = input()
        if escolha in self.confirmar_saida:
            self.confirmar_saida[escolha][1]()

    def adicionarCliente(self):
        self.banco.novoCliente()
        self.confirmarSaida()
        pass

    def apagarCliente(self):
        self.banco.apagarCliente()
        self.confirmarSaida()
        pass

    def listarClientes(self):
        self.banco.listarClientes()
        self.confirmarSaida()
        pass

    def debito(self):
        self.banco.debito()
        self.confirmarSaida()
        pass

    def deposito(self):
        self.banco.deposito()
        self.confirmarSaida()
        pass

    def extrato(self):
        self.banco.extrato()
        self.confirmarSaida()
        pass

    def transferencia(self):
        self.banco.transferencia()
        self.confirmarSaida()
        pass
    def sair(self):
        self.limparTela()
        print("Obrigado por usar o Banco QuemPoupaTem!")
        exit(0)


if __name__ == '__main__':
    menu = Menu()
    menu.exibir()
