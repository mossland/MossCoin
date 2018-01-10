import pytest
import web3.contract
from ethereum.tester import TransactionFailed

def test_burn(moss_coin, coin_owner, total_supply, token_decimals):
    moss_coin.transact({'from':coin_owner}).burn(1)

    assert moss_coin.call().totalSupply() == total_supply * (10 ** token_decimals) - 1

def test_burn_fail(moss_coin, accounts, total_supply, token_decimals):
    with pytest.raises(TransactionFailed):
        moss_coin.transact({'from':accounts[1]}).burn(1)
    
    assert moss_coin.call().totalSupply() == total_supply * (10 ** token_decimals)

def test_overburn(moss_coin, coin_owner, total_supply, token_decimals):
    with pytest.raises(TransactionFailed):
        moss_coin.transact({'from':coin_owner}).burn(total_supply * (10 ** token_decimals) + 1)
    
    assert moss_coin.call().totalSupply() == total_supply * (10 ** token_decimals)