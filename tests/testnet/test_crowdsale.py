import pytest
import web3.contract
from ethereum.tester import TransactionFailed

def test_sale_only_crowdsale(moss_coin, accounts):
    with pytest.raises(TransactionFailed):
        moss_coin.transact({'from':accounts[1]}).sale(accounts[1], 10000)
    
    assert moss_coin.call().waiting(accounts[1]) == 0