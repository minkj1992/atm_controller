# Atm Controller
> Simple Atm Controller

## 1. Run
- `pipenv`
```bash
$ brew install pipenv
$ pipenv install --dev
$ pipenv run python src/main.py
```

- `venv`
```bash
$ python -m venv .venv
$ . .venv/bin/activate
(.venv) $ pip install -r requirements.txt
(.venv) $ python src/main.py
```

## 2. Tests
- [coverage html](./cov_html/index.html)

- `pipenv`
```bash
$ pipenv install --dev
$ pipenv run pytest .
```

- `venv`
```bash
(.venv) $ pytest .
```

- @TODO
    - bdd
    - terminal screen shot


## 3. Structure

```bash
.
├── Pipfile                 # Pipenv(package manager)
├── .pre-commit-config.yaml # Pre-commit hooks(black, flake8, mypy, reorder-imports)
├── README.md
├── cov_html                # Report test coverage
├── pytest.ini              # Pytest configuration
├── requirements.txt        # If you do not want to use pipenv, use venv
├── src
│   ├── atm.py              # Define simple atm controller
│   ├── banking.py          # Abstract Bank system (pin, account, bank)
│   ├── commands.py         # Define "Command" and "Protocols" (command-pattern)
│   ├── consts.py           # Define constants
│   ├── exceptions.py       # Define exceptions
│   └── modules.py          # Define 3rd party hardware modules (cash_bin, card_reader)
└── tests
    ├── conftest.py         # Define common "given" data to use before testing
    ├── integration         # Integration test (bdd)
    │   └──
    ├── unit
    │   └── test_atm.py     # Simple atm controller unit test
    └── utils.py            # Test utils
```


## 4. Key points
- Using `command pattern` with python protocol.
- Implement `transaction` command, it can handle `undo` when exception happened.
- Error handling each stage. (insert_card > enter_pin > deposit/balance/withdraw)
## 5. Features
### 5-1. `Card`
- [x] insert card
- [x] eject card
- [x] check already card slot is occupied (insert)
- [x] check empty card slot (eject)
### 5-2. `Pin` (`Account`)
- [x] enter pin number
- [x] validate pin number
- [x] get account by card and validate pin number
- [x] retry until `MAX_PIN_RETRY_COUNT` when wrong pin number is entered
- [x] record retried `account_uuid` with atm cache (`pin_try_cache`)
### 5-3. `Balance`
- [x] get current account balance
- [x] handling invalid try case to get account balance
    - before insert card
    - before enter pin
### 5-4. `Deposit`
- [x] add amount to cash_bin
- [x] add cash to current account
- [x] rollback when error occurred

### 5-5. `Withdraw`
- [x] subtract amount from cash_bin
- [x] withdraw cash from current account
- [x] rollback when error occurred
