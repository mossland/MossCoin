import pytest

def test_transfer(local_chain, moss_coin, owner, local_accounts):
    original = moss_coin.call().balanceOf(owner)
    tx_hash = moss_coin.transact({'from' : owner}).transfer(local_accounts[1], 100)
    local_chain.wait.for_receipt(tx_hash)

    assert moss_coin.call().balanceOf(local_accounts[1]) == 100
    assert moss_coin.call().balanceOf(owner) == original - 100

    tx_hash = moss_coin.transact({'from' : local_accounts[1]}).transfer(owner, 100)
    local_chain.wait.for_receipt(tx_hash)