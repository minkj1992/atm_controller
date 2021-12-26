from collections import defaultdict
from typing import DefaultDict
from typing import Optional

from .banking import Account
from .banking import Bank
from .banking import Card
from .commands import AddCash
from .commands import Batch
from .commands import Deposit
from .commands import SubtractCash
from .commands import Transaction
from .commands import Withdrawal
from .consts import MAX_PIN_RETRY_COUNT
from .exceptions import AccountNotFoundException
from .exceptions import ExceedMaxPinTryCountException
from .exceptions import InvalidPinException
from .modules import CardReader
from .modules import CashBin


class AtmController:
    def __init__(self, bank: Bank, cash_bin: CashBin, card_reader: CardReader):
        self.bank = bank
        self.cash_bin = cash_bin
        self.card_reader = card_reader

        self.current_account: Optional[Account] = None
        self.pin_try_cache: DefaultDict[str, int] = defaultdict(lambda: 0)

    def insert_card(self, card: Card) -> None:
        self.card_reader.insert(card)

    def eject_card(self) -> None:
        self.card_reader.eject()

    def enter_pin(self, pin_number: str) -> Account:  # type: ignore
        account_uuid = self.card_reader.read_card_owner_info()

        if self.pin_try_cache[account_uuid] >= MAX_PIN_RETRY_COUNT:
            self._exit()
            raise ExceedMaxPinTryCountException()

        self.pin_try_cache[account_uuid] += 1

        try:
            self.current_account = self.bank.validate_pin(account_uuid, pin_number)
            return self.current_account
        except InvalidPinException as err:
            print(err)
            print(f"Please re enter pin number (try count: {self.pin_try_cache[account_uuid]})")

    def get_account_balance(self) -> int:
        if not self.current_account:
            self._exit()
            raise AccountNotFoundException()
        return self.current_account.balance

    def deposit(self, amount: int):
        self._execute(
            Batch(
                commands=[
                    AddCash(cash_bin=self.cash_bin, amount=amount),
                    Deposit(bank=self.bank, account=self.current_account, amount=amount),  # type: ignore
                ]
            )
        )

    def withdraw(self, amount: int):
        self._execute(
            Batch(
                commands=[
                    Withdrawal(bank=self.bank, amount=amount, account=self.current_account),  # type: ignore
                    SubtractCash(cash_bin=self.cash_bin, amount=amount),
                ]
            )
        )

    def _exit(self):
        print("Exit ATM process!")
        self.card_reader.clear()
        self.current_account = None

    def _execute(self, transaction: Transaction) -> None:
        if not self.current_account:
            self._exit()
            raise AccountNotFoundException()
        transaction.execute()
