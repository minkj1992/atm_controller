from __future__ import annotations


class ATMState:
    def __init__(self, atm):
        self._atm = atm

    def read_card(self):
        ...

    def verify_pin(self):
        ...

    def select_transaction(self):
        ...

    def deposit(self):
        ...

    def withdraw(self):
        ...

    def cash_dispensed(self):
        ...

    def show_balance(self):
        ...

    def transaction_again(self):
        ...

    def exit(self):
        ...

    def return_card(self):
        ...


class ReadyState(ATMState):
    ...


class EnterPinState(ATMState):
    ...


class SelectTransactionState(ATMState):
    ...


class DepositState(ATMState):
    ...


class WithdrawState(ATMState):
    ...


class DisplayBalanceState(ATMState):
    ...


class InvalidCashReturnedState(ATMState):
    ...


class AtmController:
    _state = None

    def __init__(self, state: ATMState, available_cash: int = 100000):
        self.set_state(state)
        self.user = None
        self.available_cash = available_cash

    def set_state(self, state: ATMState):
        print(f"State change to {type(state).__name__}")
        self._state = state
        self._state._atm = self

    def execute(self):
        self._state.execute()


# atm = ATM(state=ReadyState(), available_cash=100)
# atm.execute()
# atm.execute()
# atm.execute()
