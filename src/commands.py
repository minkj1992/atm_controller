from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field
from typing import Protocol

from .banking import Account
from .banking import Bank
from .modules import CashBin


class Transaction(Protocol):
    def execute(self) -> None:
        ...

    def undo(self) -> None:
        ...

    def redo(self) -> None:
        ...


@dataclass
class Deposit:
    bank: Bank
    account: Account
    amount: int

    @property
    def details(self) -> str:
        return f"${self.amount} to account {self.account.name}(bank: {self.bank.name})."

    def execute(self) -> None:
        self.account.deposit(self.amount)
        print(f"Deposited {self.details}")

    def undo(self) -> None:
        self.account.withdraw(self.amount)
        print(f"Undid deposit of {self.details}")

    def redo(self) -> None:
        self.account.deposit(self.amount)
        print(f"Redid deposit of {self.details}")


@dataclass
class Withdrawal:
    bank: Bank
    account: Account
    amount: int

    @property
    def details(self) -> str:
        return f"${self.amount} from account {self.account.name}(bank: {self.bank.name})."

    def execute(self) -> None:
        self.account.withdraw(self.amount)
        print(f"Withdrawn {self.details}")

    def undo(self) -> None:
        self.account.deposit(self.amount)
        print(f"Undid withdrawal of {self.details}")

    def redo(self) -> None:
        self.account.withdraw(self.amount)
        print(f"Redid withdrawal of {self.details}")


@dataclass
class AddCash:
    cash_bin: CashBin
    amount: int

    @property
    def details(self) -> str:
        return f"${self.amount} (total balance: {self.cash_bin.cash})"

    def execute(self) -> None:
        self.cash_bin.add(self.amount)
        print(f"Add Cash {self.details}")

    def undo(self) -> None:
        self.cash_bin.subtract(self.amount)
        print(f"Undid Add Cash {self.details}")

    def redo(self) -> None:
        self.cash_bin.add(self.amount)
        print(f"Redid Add Cash {self.details}")


@dataclass
class SubtractCash:
    cash_bin: CashBin
    amount: int

    @property
    def details(self) -> str:
        return f"${self.amount} (total balance: {self.cash_bin.cash})"

    def execute(self) -> None:
        self.cash_bin.subtract(self.amount)
        print(f"Subtract cash {self.details}")

    def undo(self) -> None:
        self.cash_bin.add(self.amount)
        print(f"Undid Subtract cash {self.details}")

    def redo(self) -> None:
        self.cash_bin.subtract(self.amount)
        print(f"Redid Subtract cash {self.details}")


@dataclass
class Batch:
    commands: list[Transaction] = field(default_factory=list)

    def execute(self) -> None:
        completed_commands: list[Transaction] = []
        try:
            for command in self.commands:
                command.execute()
                completed_commands.append(command)
        except Exception:
            for command in reversed(completed_commands):
                command.undo()
            raise

    def undo(self) -> None:
        for command in reversed(self.commands):
            command.undo()

    def redo(self) -> None:
        for command in self.commands:
            command.redo()
