import time
import pytest

@pytest.fixture
def total_supply():
    return 30000000

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
def moss_coin(chain, coin_owner, total_supply):
    args = [total_supply]

    transaction = {
        'from' : coin_owner
    }

    contract, _ = chain.provider.deploy_contract('MossCoin', deploy_args=args, deploy_transaction=transaction)
    return contract

@pytest.fixture
def testernet_start():
    return 1410973381

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
    return 1200

@pytest.fixture
def moss_crowdsale(chain, moss_coin, coin_owner, testernet_start, period, min_invest, max_invest, cap, rate):
    start = testernet_start
    end = start + period

    args = [start, end, rate, cap, min_invest, max_invest, coin_owner, moss_coin.address]

    transaction = {
        "from" : coin_owner
    }

    contract, _ = chain.provider.deploy_contract('MossCrowdsale', deploy_args=args, deploy_transaction=transaction)
    moss_coin.transact({'from':coin_owner}).setCrowdsale(contract.address, True)

    return contract


@pytest.fixture
def upgrade_target(chain, moss_coin, coin_owner):
    args = [moss_coin.address]

    transaction = {
        "from" : coin_owner
    }

    contract, _ = chain.provider.deploy_contract('UpgradeTestToken', deploy_args=args, deploy_transaction=transaction)
    
    return contract

@pytest.fixture
def upgrade_target2(chain, moss_coin, coin_owner):
    args = [moss_coin.address]

    transaction = {
        "from" : coin_owner
    }

    contract, _ = chain.provider.deploy_contract('UpgradeTestToken', deploy_args=args, deploy_transaction=transaction)
    
    return contract