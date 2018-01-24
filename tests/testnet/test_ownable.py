import pytest
import web3.contract
from ethereum.tester import TransactionFailed

def test_ownable_change(moss_coin, coin_owner, accounts):
    moss_coin.transact({'from':coin_owner}).transferOwnership(accounts[1])

def test_ownable_change_fail(moss_coin, coin_owner, accounts):
    with pytest.raises(TransactionFailed):
        moss_coin.transact({'from':accounts[1]}).transferOwnership(accounts[2])