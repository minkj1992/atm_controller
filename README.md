# atm_controller
> simple atm controller

## build

## run
- `pipenv`
```bash
$ brew install pipenv
$ pipenv install
$ pipenv run python src/main.py
```

- `venv`
```bash
$ python -m venv .venv
$ . .venv/bin/activate
(.venv) $ pip install -r requirements.txt
(.venv) $ python src/main.py
```

## tests
- `pipenv`
```bash
$ pipenv install --dev
$ pipenv run pytest .
```

- `venv`
```bash
(.venv) $ pytest .
```
