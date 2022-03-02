from pytest_bdd import given
from pytest_bdd import scenario
from pytest_bdd import then
from pytest_bdd import when

from src.atm import AtmController
from src.banking import Account
from src.banking import Card


@scenario("../features/atm.feature")
def step_impl():
    raise NotImplementedError("STEP: Given customer has 2 cards")


@when("1 card are inserted to ATM's Card Reader")
def step_impl():
    raise NotImplementedError("STEP: When 1 card are inserted to ATM's Card Reader")


@then("the Card Reader contains 1 card")
def step_impl():
    raise NotImplementedError("STEP: Then the Card Reader contains 1 card")


@given("a")
def step_impl():
    raise NotImplementedError("STEP: Given a")


@when("b")
def step_impl():
    raise NotImplementedError("STEP: When b")


@then("c")
def step_impl():
    raise NotImplementedError("STEP: Then c")
