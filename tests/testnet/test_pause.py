import pytest
import web3.contract
from ethereum.tester import TransactionFailed

def test_pause_owner_only(chain, moss_coin, coin_owner, accounts):
    moss_coin.transact({'from':coin_owner}).pause()

    with pytest.raises(TransactionFailed):
        moss_coin.transact({'from':accounts[1]}).pause()

    with pytest.raises(TransactionFailed):
        moss_coin.transact({'from':accounts[1]}).unpause()
    
    moss_coin.transact({'from':coin_owner}).unpause()

def test_pause_transfer(chain, moss_coin, coin_owner, accounts):
    moss_coin.transact({'from' : coin_owner}).transfer(accounts[1], 100)

    moss_coin.transact({'from':coin_owner}).pause()

    with pytest.raises(TransactionFailed):
        moss_coin.transact({'from' : accounts[1]}).transfer(coin_owner, 100)
    
    with pytest.raises(TransactionFailed):
        moss_coin.transact({'from' : coin_owner}).transfer(accounts[1], 100)

    moss_coin.transact({'from':coin_owner}).unpause()

    moss_coin.transact({'from' : accounts[1]}).transfer(coin_owner, 100)
    moss_coin.transact({'from' : coin_owner}).transfer(accounts[1], 100)