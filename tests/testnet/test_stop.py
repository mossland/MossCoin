import pytest
import web3.contract
from ethereum.tester import TransactionFailed

def test_stop_start_owner_only(chain, moss_coin, coin_owner, accounts):
    moss_coin.transact({'from':coin_owner}).stop()

    with pytest.raises(TransactionFailed):
        moss_coin.transact({'from':accounts[1]}).stop()

    with pytest.raises(TransactionFailed):
        moss_coin.transact({'from':accounts[1]}).start()
    
    moss_coin.transact({'from':coin_owner}).start()

def test_stop_transfer(chain, moss_coin, coin_owner, accounts):
    moss_coin.transact({'from' : coin_owner}).transfer(accounts[1], 100)

    moss_coin.transact({'from':coin_owner}).stop()

    with pytest.raises(TransactionFailed):
        moss_coin.transact({'from' : accounts[1]}).transfer(coin_owner, 100)
    
    with pytest.raises(TransactionFailed):
        moss_coin.transact({'from' : coin_owner}).transfer(accounts[1], 100)

    moss_coin.transact({'from':coin_owner}).start()

    moss_coin.transact({'from' : accounts[1]}).transfer(coin_owner, 100)
    moss_coin.transact({'from' : coin_owner}).transfer(accounts[1], 100)