import pytest

@pytest.fixture
def total_supply():
    return 250000000

@pytest.fixture
def token_name():
    return "Moss Coin"

@pytest.fixture
def token_symbol():
    return "MOC"

@pytest.fixture
def token_decimals():
    return 18

@pytest.fixture
def invest_decimals(token_decimals):
    return token_decimals - 3

@pytest.fixture
def coin_owner(accounts):
    return accounts[0]

@pytest.fixture
def pre_period():
    return 2*7*24*60*60 # 2 weeks

@pytest.fixture
def main_period():
    return 4*7*24*60*60 # 4 weeks

@pytest.fixture
def main_bonus_change_period():
    return 7*24*60*60 # 1 week

@pytest.fixture
def period():
    return 10000

@pytest.fixture
def min_invest():
    return 100

@pytest.fixture
def max_invest():
    return 1000000

@pytest.fixture
def cap():
    return 10000

@pytest.fixture
def rate():
    return 5000