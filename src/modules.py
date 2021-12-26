from dataclasses import dataclass
from typing import Optional

from .banking import Card
from .exceptions import AlreadyCardExistException
from .exceptions import EmptyCardException
from .exceptions import InvalidCashAmountException


@dataclass
class CardReader:
    card: Optional[Card] = None

    def insert(self, card: Card) -> Card:
        if not self._is_slot_empty():
            raise AlreadyCardExistException(self.card)

        print(f"'{card.name} Card' is inserted.")
        self.card = card
        return self.card

    def eject(self) -> None:
        if self._is_slot_empty():
            raise EmptyCardException()
        print(f"'{self.card.name} Card' is ejected.")  # type: ignore
        self.card = None

    def read_card_owner_info(self) -> str:
        if self._is_slot_empty():
            raise EmptyCardException()
        print(f"'{self.card.name} Card' reading...")  # type: ignore
        return self.card.account_uuid  # type: ignore

    def clear(self):
        if not self._is_slot_empty():
            self.eject()
        print("Card slot is empty")

    def _is_slot_empty(self) -> bool:
        return not self.card


@dataclass
class CashBin:
    cash: int

    def add(self, amount: int) -> int:
        self.cash += amount
        return self.cash

    def subtract(self, amount: int) -> int:
        if self.cash < amount:
            raise InvalidCashAmountException(self.cash, amount)

        self.cash -= amount
        return self.cash
