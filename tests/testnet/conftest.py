import time
import pytest

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
def moss_crowdsale_pre(chain, moss_coin, coin_owner, testernet_start, pre_period, min_invest, max_invest, cap, rate):
    start = testernet_start
    end = start + pre_period

    args = [start, end, rate, cap, min_invest, max_invest, coin_owner, moss_coin.address]

    transaction = {
        "from" : coin_owner
    }

    contract, _ = chain.provider.deploy_contract('MossCrowdsalePre', deploy_args=args, deploy_transaction=transaction)
    moss_coin.transact({'from':coin_owner}).setCrowdsale(contract.address, True)

    return contract

@pytest.fixture
def moss_crowdsale_main(chain, moss_coin, coin_owner, testernet_start, main_period, main_bonus_change_period, min_invest, max_invest, cap, rate):
    start = testernet_start
    bonus1 = start + main_bonus_change_period
    bonus2 = bonus1 + main_bonus_change_period
    bonus3 = bonus2 + main_bonus_change_period
    end = start + main_period

    args = [start, bonus1, bonus2, bonus3, end, rate, cap, min_invest, max_invest, coin_owner, moss_coin.address]

    transaction = {
        "from" : coin_owner
    }

    contract, _ = chain.provider.deploy_contract('MossCrowdsaleMain', deploy_args=args, deploy_transaction=transaction)
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