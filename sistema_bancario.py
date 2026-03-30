from abc import ABC, abstractmethod
from typing import List, Optional

class Cliente:
    """Classe para representar um cliente do banco."""

    def __init__(self, nome: str, cpf: str, endereco: str):
        if not self._validar_cpf(cpf):
            raise ValueError("CPF inválido. Deve ter 11 dígitos numéricos.")
        self._nome = nome
        self._cpf = cpf
        self._endereco = endereco
        self._contas: List['Conta'] = []

    @staticmethod
    def _validar_cpf(cpf: str) -> bool:
        """Valida se o CPF tem 11 dígitos numéricos."""
        return cpf.isdigit() and len(cpf) == 11

    @property
    def nome(self) -> str:
        return self._nome

    @property
    def cpf(self) -> str:
        return self._cpf

    @property
    def endereco(self) -> str:
        return self._endereco

    @property
    def contas(self) -> List['Conta']:
        return self._contas

    def adicionar_conta(self, conta: 'Conta') -> None:
        """Adiciona uma conta ao cliente."""
        self._contas.append(conta)

class Conta(ABC):
    """Classe abstrata para contas bancárias."""

    def __init__(self, numero: int, cliente: Cliente):
        self._numero = numero
        self._saldo = 0.0
        self._cliente = cliente

    @property
    def numero(self) -> int:
        return self._numero

    @property
    def saldo(self) -> float:
        return self._saldo

    @property
    def cliente(self) -> Cliente:
        return self._cliente

    def depositar(self, valor: float) -> None:
        """Deposita um valor na conta."""
        if valor <= 0:
            raise ValueError("Valor de depósito deve ser positivo.")
        self._saldo += valor
        print(f"Depósito de R${valor:.2f} realizado. Saldo atual: R${self._saldo:.2f}")

    @abstractmethod
    def sacar(self, valor: float) -> None:
        """Saca um valor da conta (método abstrato)."""
        pass

class ContaCorrente(Conta):
    """Classe para conta corrente com limite."""

    def __init__(self, numero: int, cliente: Cliente, limite: float = 500.0):
        super().__init__(numero, cliente)
        self._limite = limite

    @property
    def limite(self) -> float:
        return self._limite

    def sacar(self, valor: float) -> None:
        """Saca um valor da conta corrente."""
        if valor <= 0:
            raise ValueError("Valor de saque deve ser positivo.")
        if valor > self._saldo + self._limite:
            raise ValueError("Saldo insuficiente.")
        self._saldo -= valor
        print(f"Saque de R${valor:.2f} realizado. Saldo atual: R${self._saldo:.2f}")

class ContaPoupanca(Conta):
    """Classe para conta poupança com juros."""

    def __init__(self, numero: int, cliente: Cliente, taxa_juros: float = 0.02):
        super().__init__(numero, cliente)
        self._taxa_juros = taxa_juros

    @property
    def taxa_juros(self) -> float:
        return self._taxa_juros

    def sacar(self, valor: float) -> None:
        """Saca um valor da conta poupança."""
        if valor <= 0:
            raise ValueError("Valor de saque deve ser positivo.")
        if valor > self._saldo:
            raise ValueError("Saldo insuficiente.")
        self._saldo -= valor
        print(f"Saque de R${valor:.2f} realizado. Saldo atual: R${self._saldo:.2f}")

    def aplicar_juros(self) -> None:
        """Aplica juros à conta poupança."""
        juros = self._saldo * self._taxa_juros
        self._saldo += juros
        print(f"Juros de R${juros:.2f} aplicados. Saldo atual: R${self._saldo:.2f}")

class SistemaBancario:
    """Classe para gerenciar o sistema bancário."""

    def __init__(self):
        self._clientes: List[Cliente] = []

    def adicionar_cliente(self, cliente: Cliente) -> None:
        """Adiciona um cliente ao sistema, verificando CPF único."""
        if any(c.cpf == cliente.cpf for c in self._clientes):
            raise ValueError("CPF já cadastrado.")
        self._clientes.append(cliente)

    def encontrar_cliente(self, cpf: str) -> Optional[Cliente]:
        """Encontra um cliente pelo CPF."""
        return next((c for c in self._clientes if c.cpf == cpf), None)

    def transferir(self, cpf_origem: str, numero_conta_origem: int, cpf_destino: str, numero_conta_destino: int, valor: float) -> None:
        """Transfere valor entre contas."""
        cliente_origem = self.encontrar_cliente(cpf_origem)
        cliente_destino = self.encontrar_cliente(cpf_destino)
        if not cliente_origem or not cliente_destino:
            raise ValueError("Cliente não encontrado.")
        conta_origem = next((c for c in cliente_origem.contas if c.numero == numero_conta_origem), None)
        conta_destino = next((c for c in cliente_destino.contas if c.numero == numero_conta_destino), None)
        if not conta_origem or not conta_destino:
            raise ValueError("Conta não encontrada.")
        conta_origem.sacar(valor)
        conta_destino.depositar(valor)
        print("Transferência realizada com sucesso.")

    def listar_contas_cliente(self, cpf: str) -> None:
        """Lista as contas de um cliente."""
        cliente = self.encontrar_cliente(cpf)
        if not cliente:
            print("Cliente não encontrado.")
            return
        if not cliente.contas:
            print("Cliente não possui contas.")
            return
        for conta in cliente.contas:
            tipo = "Corrente" if isinstance(conta, ContaCorrente) else "Poupança"
            print(f"Conta {conta.numero} ({tipo}): Saldo R${conta.saldo:.2f}")

# ---------------- MENU ----------------
sistema = SistemaBancario()

def criar_cliente():
    """Cria um novo cliente."""
    try:
        nome = input("Nome: ").strip()
        if not nome:
            raise ValueError("Nome não pode ser vazio.")
        cpf = input("CPF (11 dígitos): ").strip()
        endereco = input("Endereço: ").strip()
        cliente = Cliente(nome, cpf, endereco)
        sistema.adicionar_cliente(cliente)
        print("Cliente criado com sucesso!")
    except ValueError as e:
        print(f"Erro: {e}")

def criar_conta():
    """Cria uma nova conta para um cliente."""
    try:
        cpf = input("CPF do cliente: ").strip()
        cliente = sistema.encontrar_cliente(cpf)
        if not cliente:
            print("Cliente não encontrado.")
            return
        tipo = input("Tipo (corrente/poupanca): ").strip().lower()
        if tipo not in ["corrente", "poupanca"]:
            raise ValueError("Tipo inválido.")
        numero = len(cliente.contas) + 1
        if tipo == "corrente":
            conta = ContaCorrente(numero, cliente)
        else:
            conta = ContaPoupanca(numero, cliente)
        cliente.adicionar_conta(conta)
        print(f"Conta {tipo} criada com sucesso!")
    except ValueError as e:
        print(f"Erro: {e}")

def selecionar_conta(cliente: Cliente) -> Optional[Conta]:
    """Permite ao usuário selecionar uma conta."""
    if not cliente.contas:
        print("Cliente não possui contas.")
        return None
    sistema.listar_contas_cliente(cliente.cpf)
    try:
        numero = int(input("Número da conta: "))
        conta = next((c for c in cliente.contas if c.numero == numero), None)
        if not conta:
            print("Conta não encontrada.")
            return None
        return conta
    except ValueError:
        print("Número inválido.")
        return None

def depositar():
    """Realiza depósito."""
    try:
        cpf = input("CPF do cliente: ").strip()
        cliente = sistema.encontrar_cliente(cpf)
        if not cliente:
            print("Cliente não encontrado.")
            return
        conta = selecionar_conta(cliente)
        if not conta:
            return
        valor = float(input("Valor do depósito: "))
        conta.depositar(valor)
    except ValueError as e:
        print(f"Erro: {e}")

def sacar():
    """Realiza saque."""
    try:
        cpf = input("CPF do cliente: ").strip()
        cliente = sistema.encontrar_cliente(cpf)
        if not cliente:
            print("Cliente não encontrado.")
            return
        conta = selecionar_conta(cliente)
        if not conta:
            return
        valor = float(input("Valor do saque: "))
        conta.sacar(valor)
    except ValueError as e:
        print(f"Erro: {e}")

def aplicar_juros():
    """Aplica juros às contas poupança."""
    try:
        cpf = input("CPF do cliente: ").strip()
        cliente = sistema.encontrar_cliente(cpf)
        if not cliente:
            print("Cliente não encontrado.")
            return
        for conta in cliente.contas:
            if isinstance(conta, ContaPoupanca):
                conta.aplicar_juros()
    except ValueError as e:
        print(f"Erro: {e}")

def transferir():
    """Realiza transferência."""
    try:
        cpf_origem = input("CPF de origem: ").strip()
        numero_origem = int(input("Número da conta de origem: "))
        cpf_destino = input("CPF de destino: ").strip()
        numero_destino = int(input("Número da conta de destino: "))
        valor = float(input("Valor: "))
        sistema.transferir(cpf_origem, numero_origem, cpf_destino, numero_destino, valor)
    except ValueError as e:
        print(f"Erro: {e}")

def listar_contas():
    """Lista contas de um cliente."""
    cpf = input("CPF do cliente: ").strip()
    sistema.listar_contas_cliente(cpf)

def menu():
    """Menu principal."""
    while True:
        print("\n--- MENU ---")
        print("1 - Criar Cliente")
        print("2 - Criar Conta")
        print("3 - Depositar")
        print("4 - Sacar")
        print("5 - Aplicar Juros (Poupança)")
        print("6 - Transferir")
        print("7 - Listar Contas")
        print("0 - Sair")

        opcao = input("Escolha: ").strip()

        if opcao == "1":
            criar_cliente()
        elif opcao == "2":
            criar_conta()
        elif opcao == "3":
            depositar()
        elif opcao == "4":
            sacar()
        elif opcao == "5":
            aplicar_juros()
        elif opcao == "6":
            transferir()
        elif opcao == "7":
            listar_contas()
        elif opcao == "0":
            break
        else:
            print("Opção inválida.")

# Executar menu
if __name__ == "__main__":
    menu()
