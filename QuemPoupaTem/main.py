import Banco
import os

class Menu:
    def __init__(self):
        self.banco = Banco.Banco() # Instancia o banco
        self.opcoes = { # Cria um dicionário com as opções do menu
            "1": ("Adicionar cliente", self.adicionarCliente),
            "2": ("Apagar cliente (CNPJ)", self.apagarCliente),
            "3": ("Listar clientes", self.listarClientes),
            "4": ("Débito em conta", self.debito),
            "5": ("Depósito em conta", self.deposito),
            "6": ("Extrato", self.extrato),
            "7": ("Transferência", self.transferencia),
            "0": ("Sair", self.sair)
        }
        self.confirmar_saida = { # Cria um dicionário com as opções de confirmação de saída
            "1": ("Sim", self.exibir),
            "2": ("Encerrar o programa", self.sair)
        }

    def exibir(self):
        while True:
            self.limparTela() # Limpa a tela
            print("Bem-vindo ao Banco QuemPoupaTem!\n")
            for opcao, descricao in self.opcoes.items(): # Imprime as opções do menu e sua descrição
                print(f"{opcao}. {descricao[0]}")
            escolha = input("\nEscolha uma opção: ")
            if escolha in self.opcoes: # Se a opcao for valida
                self.opcoes[escolha][1]() # Chama a função correspondente
            else:
                input("Opção inválida! Pressione Enter para continuar...")

    def limparTela(self):
        os.system('clear') # Limpa a tela

    def confirmarSaida(self):
        print("Deseja retornar ao menu principal?")
        for opcao, descricao in self.confirmar_saida.items(): # Imprime as opççães de confirmação de saída e sua descrição
            print(f"{opcao}. {descricao[0]}")
        escolha = input() # Recebe a escolha do usuário
        if escolha in self.confirmar_saida: # Se a opcao for valida
            self.confirmar_saida[escolha][1]() # Chama a função correspondente

    def adicionarCliente(self):
        self.banco.novoCliente() # Chama a função de adicionar cliente
        self.confirmarSaida() # Confirma a saída
        pass

    def apagarCliente(self):
        self.banco.apagarCliente() # Chama a função de apagar cliente
        self.confirmarSaida() # Confirma a saída
        pass

    def listarClientes(self):
        self.banco.listarClientes() # Chama a função de listar cliente
        self.confirmarSaida() # Confirma a saída
        pass

    def debito(self):
        self.banco.debito() # Chama a função de debito
        self.confirmarSaida() # Confirma a saída
        pass

    def deposito(self):
        self.banco.deposito() # Chama a função de deposito
        self.confirmarSaida() # Confirma a saída
        pass

    def extrato(self):
        self.banco.extrato() # Chama a função de extrato
        self.confirmarSaida() # Confirma a saída
        pass

    def transferencia(self):
        self.banco.transferencia() # Chama a função de transferencia
        self.confirmarSaida() # Confirma a saída
        pass
    def sair(self):
        self.limparTela() # Limpa a tela
        print("Obrigado por usar o Banco QuemPoupaTem!") # Imprime a mensagem de saída
        exit(0) # Encerra o programa


if __name__ == '__main__':
    menu = Menu() # Instancia o menu
    menu.exibir() # Exibe o menu
