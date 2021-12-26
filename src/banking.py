from __future__ import annotations

import random
import uuid
from dataclasses import dataclass
from dataclasses import field

from .exceptions import InvalidPinException
from .exceptions import NotEnoughBalanceException

BANKING_NAMES = ("카카오뱅크", "KB국민은행", "신한은행", "우리은행", "하나은행")


def generate_banking_name() -> str:
    return random.choice(BANKING_NAMES)


def generate_uuid() -> str:
    return str(uuid.uuid4())


@dataclass
class Pin:
    number: str


@dataclass
class Card:
    account_uuid: str
    name: str


@dataclass
class Account:
    name: str
    pin: Pin
    uuid: str = field(default_factory=generate_uuid)
    balance: int = 0

    def deposit(self, amount: int) -> int:
        self.balance += amount
        print(f"{self.name} made a deposit of ${amount}.")
        return self.balance

    def withdraw(self, amount: int) -> int:
        if amount > self.balance:
            raise NotEnoughBalanceException(self.balance, amount)

        self.balance -= amount
        print(f"{self.name} withdrew ${amount}.")
        return self.balance

    def get_pin_number(self) -> str:
        return self.pin.number


@dataclass
class Bank:
    accounts: dict[str, Account] = field(default_factory=dict)
    name: str = field(default_factory=generate_banking_name)

    def create_account(self, name: str, pin_number: str, balance: int) -> Account:
        pin = Pin(number=pin_number)
        account = Account(name=name, pin=pin, balance=balance)
        self.accounts[account.uuid] = account

        print(f'"{account.name}" is registered from "{self.name}"')
        return account

    def create_card(self, account_uuid: str) -> Card:
        return Card(account_uuid, self.name)

    def validate_pin(self, account_uuid: str, pin_number: str) -> Account:
        account = self._get_account(account_uuid)

        if account.get_pin_number() != pin_number:
            raise InvalidPinException()

        print(f"{account.name} identity has been verified")
        return account

    def _get_account(self, account_uuid: str) -> Account:
        return self.accounts[account_uuid]
