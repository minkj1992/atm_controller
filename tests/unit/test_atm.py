from unittest import mock

import pytest

from src.atm import AtmController
from src.banking import Account
from src.banking import Card
from src.consts import DEFAULT_CASH_BIN_BALANCE
from src.consts import MAX_PIN_RETRY_COUNT
from src.exceptions import AccountNotFoundException
from src.exceptions import AlreadyCardExistException
from src.exceptions import EmptyCardException
from src.exceptions import ExceedMaxPinTryCountException
from src.exceptions import InvalidCashAmountException
from src.exceptions import NotEnoughBalanceException


def test_insert_card_success(card: Card, simple_atm: AtmController):
    # then
    try:
        simple_atm.insert_card(card)
    except Exception as err:
        pytest.fail(f"Expect not to raise any err but occurred. {str(err)}")


def test_insert_card_when_card_already_exist(card: Card, simple_atm: AtmController):
    # when
    simple_atm.insert_card(card)

    # then
    with pytest.raises(AlreadyCardExistException) as err:
        simple_atm.insert_card(card)
    print(err.value)


def test_eject_card_success(card: Card, simple_atm: AtmController):
    # when
    simple_atm.insert_card(card)

    try:
        simple_atm.eject_card()
    except Exception as err:
        pytest.fail(f"Expect not to raise any err but occurred. {str(err)}")


def test_eject_card_before_card_insert(simple_atm: AtmController):
    # then
    with pytest.raises(EmptyCardException) as err:
        simple_atm.eject_card()
    print(err.value)


def test_enter_pin_success(card: Card, account: Account, simple_atm: AtmController):
    # given
    correct_pin_number = account.get_pin_number()

    # when
    simple_atm.insert_card(card)
    simple_atm.enter_pin(correct_pin_number)

    # then
    assert account == simple_atm.current_account


def test_enter_pin_exceed_max_try_count(account: Account, card: Card, simple_atm: AtmController):
    # given
    wrong_pin_number = "-1"

    # when
    simple_atm.insert_card(card)

    # then
    with pytest.raises(ExceedMaxPinTryCountException) as err:
        for _ in range(MAX_PIN_RETRY_COUNT + 1):
            simple_atm.enter_pin(wrong_pin_number)
    print(err.value)
    assert simple_atm.card_reader._is_slot_empty() is True  # noqa
    assert simple_atm.current_account is None
    assert simple_atm.pin_try_cache[account.uuid] == MAX_PIN_RETRY_COUNT


def test_get_account_balance_success(card: Card, account: Account, simple_atm: AtmController):
    # when
    simple_atm.insert_card(card)
    simple_atm.enter_pin(account.get_pin_number())

    # then
    assert account.balance == simple_atm.get_account_balance()


def test_get_account_balance_without_inserted_card(simple_atm: AtmController):
    # then
    with pytest.raises(AccountNotFoundException) as err:
        simple_atm.get_account_balance()
    print(err.value)
    assert simple_atm.card_reader._is_slot_empty() is True  # noqa
    assert simple_atm.current_account is None


def test_get_account_balance_without_enter_pin(card: Card, simple_atm: AtmController):
    # when
    simple_atm.insert_card(card)

    # then
    with pytest.raises(AccountNotFoundException) as err:
        simple_atm.get_account_balance()
    print(err.value)
    assert simple_atm.card_reader._is_slot_empty() is True  # noqa
    assert simple_atm.current_account is None


def test_deposit_success(account: Account, card: Card, simple_atm: AtmController):
    # given
    deposit_money = 1000

    # when
    simple_atm.insert_card(card)
    simple_atm.enter_pin(account.get_pin_number())
    simple_atm.deposit(amount=deposit_money)

    # then
    assert account.balance == (10000 + deposit_money)
    assert simple_atm.cash_bin.cash == (DEFAULT_CASH_BIN_BALANCE + deposit_money)


def test_deposit_when_forced_exception_happen_rollback_every_commands(
    account: Account, card: Card, simple_atm: AtmController
):
    # given
    before_cash_bin_balance = simple_atm.cash_bin.cash
    before_account_balance = account.balance
    deposit_money = 1000

    # when
    simple_atm.insert_card(card)
    simple_atm.enter_pin(account.get_pin_number())

    with mock.patch("src.commands.Deposit.execute", side_effect=Exception("Forced Exception Occured")):
        with pytest.raises(Exception) as err:
            simple_atm.deposit(amount=deposit_money)
    print(err.value)
    # then
    assert account.balance == before_account_balance
    assert simple_atm.cash_bin.cash == before_cash_bin_balance


def test_withdraw_success(account: Account, card: Card, simple_atm: AtmController):
    # given
    withdraw_money = 1000

    # when
    simple_atm.insert_card(card)
    simple_atm.enter_pin(account.get_pin_number())
    simple_atm.withdraw(amount=withdraw_money)

    # then
    assert account.balance == (10000 - withdraw_money)
    assert simple_atm.cash_bin.cash == (DEFAULT_CASH_BIN_BALANCE - withdraw_money)


def test_withdraw_more_than_cash_bin_balance(account: Account, card: Card, simple_atm: AtmController):
    # given
    withdraw_money = DEFAULT_CASH_BIN_BALANCE + 1000
    account.balance = withdraw_money + 1000
    before_cash_bin_balance = simple_atm.cash_bin.cash
    before_account_balance = account.balance

    # when
    simple_atm.insert_card(card)
    simple_atm.enter_pin(account.get_pin_number())

    # then
    with pytest.raises(InvalidCashAmountException) as err:
        simple_atm.withdraw(amount=withdraw_money)
    print(err.value)
    # rollback check
    assert before_cash_bin_balance == simple_atm.cash_bin.cash
    assert before_account_balance == account.balance


def test_withdraw_less_than_account_balance(account: Account, card: Card, simple_atm: AtmController):
    # given
    before_cash_bin_balance = simple_atm.cash_bin.cash
    before_account_balance = account.balance
    withdraw_money = account.balance + 1000

    # when
    simple_atm.insert_card(card)
    simple_atm.enter_pin(account.get_pin_number())

    # then
    with pytest.raises(NotEnoughBalanceException) as err:
        simple_atm.withdraw(amount=withdraw_money)
    print(err.value)

    # rollback check
    assert before_cash_bin_balance == simple_atm.cash_bin.cash
    assert before_account_balance == account.balance
