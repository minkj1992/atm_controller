import pytest

from src import consts
from src.atm import AtmController
from src.banking import Account
from src.banking import Bank
from src.banking import Card
from src.modules import CardReader
from src.modules import CashBin
from tests.utils import generate_pin_number


def pytest_configure():
    try:
        import rich
    except ImportError:
        pass
    else:
        rich.get_console()  # this is new !
        rich.reconfigure(soft_wrap=False)


@pytest.fixture()
def bank() -> Bank:
    return Bank()


@pytest.fixture()
def account(bank: Bank) -> Account:
    return bank.create_account(name="leoo.j", pin_number=generate_pin_number(), balance=10000)


@pytest.fixture()
def card(bank: Bank, account: Account) -> Card:
    return bank.create_card(account.uuid)


@pytest.fixture()
def card_reader() -> CardReader:
    return CardReader()


@pytest.fixture()
def cash_bin() -> CashBin:
    return CashBin(cash=consts.DEFAULT_CASH_BIN_BALANCE)


@pytest.fixture()
def simple_atm(bank: Bank, card_reader: CardReader, cash_bin: CashBin) -> AtmController:
    return AtmController(bank, cash_bin, card_reader)
