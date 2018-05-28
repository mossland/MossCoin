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
def coin_owner(accounts):
    return accounts[0]