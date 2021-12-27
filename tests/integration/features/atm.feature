Feature: Simple Atm Controller
  As an ATM software engineer.
  I want to implement a simple ATM controller.
  ATM should be able to execute the following simple flow.
    1. Insert a Card
    2. Get Pin Number
    3. Verify Pin
    4. Get Account from banking system
    5. Display next command options
      5-1. See Balance
      5-2. Deposit Cash
      5-3. Withdraw Cash
  - Rules:
    - There are only 1 dollar bills, which infers balance can be represented in integer.
    - The detailed banking system should not be considered, but will be considered in the future. -> Abstract Banking System with API.
      - create account
      - register card
      - verify pin number
    - Currently, I don't need to interface with an ATM's hardware modules, but will in the future. -> Abstract Card-Reader, Cash-Bin.
    - Test everything! exclude banking system and ATM hardware (e.g cash bin, card reader)
    - ATM should not remember PIN number but banking system should verify whether the PIN number is correct or not.
    - Other engineers should be able to implement the UI part, without any conversation (exclude code).

  Scenario: Insert a Card to ATM.
    Given customer has 2 cards
    When 1 card are inserted to ATM's Card Reader
    Then the Card Reader contains 1 card

  Scenario: Get Pin Number.
    Given a
    When b
    Then c

  Scenario: Verify Pin Number.
    Given a
    When b
    Then c

  Scenario: Get Account from banking system.
    Given a
    When b
    Then c

  Scenario: Display next command options.
    Given a
    When b
    Then c

  Scenario: [Option 1] See Balance.
    Given a
    When b
    Then c

  Scenario: [Option 2] Deposit Cash.
    Given a
    When b
    Then c

  Scenario: [Option 3] Withdraw Cash.
    Given a
    When b
    Then c
