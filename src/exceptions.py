# Card Reader Exceptions
class AlreadyCardExistException(Exception):
    def __init__(self, card):
        self._card = card

    def __str__(self):
        return f"Card Slot is already occupied with {self._card}. Please eject your card."


class EmptyCardException(Exception):
    def __str__(self):
        return "Card Slot is empty. Please insert your card."


# CashBin Exceptions
class InvalidCashAmountException(Exception):
    def __init__(self, cash, amount):
        self._cash = cash
        self._amount = amount

    def __str__(self):
        return f"Invalid Cash Amount is given. current cash: {self._cash}, amount: {self._amount}"


# Bank Exceptions
class NotEnoughBalanceException(Exception):
    def __init__(self, balance, amount):
        self._balance = balance
        self._amount = amount

    def __str__(self):
        return f"Your account balance is insufficient. (balance: {self._balance}, amount: {self._amount})"


# Pin Exceptions
class InvalidPinException(Exception):
    def __str__(self):
        return "Invalid pin number is given."


class ExceedMaxPinTryCountException(Exception):
    def __str__(self):
        return "You exceeded pin try count."


# Atm Exceptions
class AccountNotFoundException(Exception):
    def __str__(self):
        return "Your account info does not recorded on atm machine. Please insert your Card first and enter pin."
