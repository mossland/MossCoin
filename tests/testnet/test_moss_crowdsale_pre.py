import pytest
import web3.contract
import web3.eth
import time
from ethereum.tester import TransactionFailed

@pytest.fixture
def presale_bonus_ether():
    return [5, 10, 25, 75]

@pytest.fixture
def presale_bonus_rate():
    return [1300, 1350, 1400, 1450, 1500]

def test_bonus_property(presale_bonus_ether, presale_bonus_rate):
    assert len(presale_bonus_ether) + 1 == len(presale_bonus_rate)

def test_bonus_rating(chain, presale_bonus_ether, presale_bonus_rate, rate):
    w3 = chain.web3
    assert presale_token(chain, 5 * w3.toWei(1, 'ether') - 1, presale_bonus_ether, presale_bonus_rate, rate) == 32500000000000000000000 - 6500
    assert presale_token(chain, 5 * w3.toWei(1, 'ether'), presale_bonus_ether, presale_bonus_rate, rate) == 33750000000000000000000
    assert presale_token(chain, 10 * w3.toWei(1, 'ether') - 1, presale_bonus_ether, presale_bonus_rate, rate) == 67500000000000000000000 - 6750
    assert presale_token(chain, 10 * w3.toWei(1, 'ether'), presale_bonus_ether, presale_bonus_rate, rate) == 70000000000000000000000
    assert presale_token(chain, 25 * w3.toWei(1, 'ether') - 1, presale_bonus_ether, presale_bonus_rate, rate) == 175000000000000000000000 - 7000
    assert presale_token(chain, 25 * w3.toWei(1, 'ether'), presale_bonus_ether, presale_bonus_rate, rate) == 181250000000000000000000
    assert presale_token(chain, 75 * w3.toWei(1, 'ether') - 1, presale_bonus_ether, presale_bonus_rate, rate) == 543750000000000000000000 - 7250
    assert presale_token(chain, 75 * w3.toWei(1, 'ether'), presale_bonus_ether, presale_bonus_rate, rate) == 562500000000000000000000

def presale_bonus(chain, wei, presale_bonus_ether, presale_bonus_rate):
    for i in range(0, 4):
        if wei < presale_bonus_ether[i] * chain.web3.toWei(1,'ether'):
            return presale_bonus_rate[i]
    
    return presale_bonus_rate[-1]

def presale_token(chain, wei, presale_bonus_ether, presale_bonus_rate, rate):
    return wei * rate * presale_bonus(chain, wei, presale_bonus_ether, presale_bonus_rate) // 1000

def test_crowdsale_initialized(chain, moss_crowdsale_pre, moss_coin, coin_owner, period, min_invest, max_invest, cap, rate, token_decimals, invest_decimals, presale_bonus_ether, presale_bonus_rate):
    w3 = chain.web3
    assert moss_crowdsale_pre.call().endTime() - moss_crowdsale_pre.call().startTime() == period
    assert moss_crowdsale_pre.call().minInvest() == (min_invest * (10 ** invest_decimals))
    assert moss_crowdsale_pre.call().maxInvest() == (max_invest * (10 ** invest_decimals))
    assert moss_crowdsale_pre.call().cap() == (cap * (10 ** token_decimals))
    assert moss_crowdsale_pre.call().weiRaised() == 0
    assert moss_crowdsale_pre.call().token().lower() == moss_coin.address
    assert moss_crowdsale_pre.call().wallet() == coin_owner

    for i in range(0, len(presale_bonus_ether)):
        assert moss_crowdsale_pre.call().values(i) == presale_bonus_ether[i] * w3.toWei(1, 'ether')
    
    assert moss_crowdsale_pre.call().values(len(presale_bonus_ether)) == moss_crowdsale_pre.call().maxInvest() 
    
    for i in range(0, len(presale_bonus_rate)):
        assert moss_crowdsale_pre.call().bonus(0, i) == presale_bonus_rate[i]

    assert moss_crowdsale_pre.call().ends(0) == moss_crowdsale_pre.call().endTime()

def test_crowdsale_buy(chain, moss_crowdsale_pre, moss_coin, coin_owner, accounts, rate, presale_bonus_ether, presale_bonus_rate):
    w3 = chain.web3
    moss_crowdsale_pre.transact({'from':accounts[1], 'value':w3.toWei(1,'ether')}).buyTokens(accounts[1])

    assert moss_coin.call().waiting(accounts[1]) == presale_token(chain, w3.toWei(1,'ether'), presale_bonus_ether, presale_bonus_rate, rate)

def test_crowdsale_buy_fallback(chain, moss_crowdsale_pre, moss_coin, accounts, rate, presale_bonus_ether, presale_bonus_rate):
    w3 = chain.web3
    w3.eth.sendTransaction({'from':accounts[1], 'to':moss_crowdsale_pre.address, 'value':w3.toWei(1,'ether')})
    assert moss_coin.call().waiting(accounts[1]) == presale_token(chain, w3.toWei(1,'ether'), presale_bonus_ether, presale_bonus_rate, rate)

def test_crowdsale_min_invest(chain, moss_crowdsale_pre, moss_coin, accounts, min_invest, invest_decimals, rate, presale_bonus_ether, presale_bonus_rate):
    with pytest.raises(TransactionFailed):
        moss_crowdsale_pre.transact({'from':accounts[1], 'value':min_invest * (10 ** invest_decimals) - 1}).buyTokens(accounts[1])

    assert moss_coin.call().waiting(accounts[1]) == 0

    moss_crowdsale_pre.transact({'from':accounts[1], 'value':min_invest * (10 ** invest_decimals) }).buyTokens(accounts[1])
    assert moss_coin.call().waiting(accounts[1]) == presale_token(chain, min_invest * (10 ** invest_decimals), presale_bonus_ether, presale_bonus_rate, rate)

def test_crowdsale_max_invest(chain, moss_crowdsale_pre, moss_coin, accounts, min_invest, max_invest, invest_decimals, rate, presale_bonus_ether, presale_bonus_rate):
    with pytest.raises(TransactionFailed):
        moss_crowdsale_pre.transact({'from':accounts[1], 'value':max_invest * (10 ** invest_decimals) + 1}).buyTokens(accounts[1])
    
    # buy max_invest - min_invest + 1
    moss_crowdsale_pre.transact({'from':accounts[2], 'value':(max_invest-min_invest) * (10 ** invest_decimals) + 1}).buyTokens(accounts[2])

    # if you already bought 'max_invest - min_invest + 1', you cannot buy tokens anymore.
    with pytest.raises(TransactionFailed):
        moss_crowdsale_pre.transact({'from':accounts[2], 'value': min_invest * (10 ** invest_decimals)}).buyTokens(accounts[2])
    
    assert moss_coin.call().waiting(accounts[1]) == 0
    assert moss_coin.call().waiting(accounts[2]) == presale_token(chain, (max_invest-min_invest) * (10 ** invest_decimals) + 1, presale_bonus_ether, presale_bonus_rate, rate)

def test_crowdsale_state_change(chain, moss_crowdsale_pre, moss_coin, coin_owner, accounts, min_invest, invest_decimals):
    moss_coin.transact({'from':coin_owner}).setCrowdsale(moss_crowdsale_pre.address, False)

    with pytest.raises(TransactionFailed):
        moss_crowdsale_pre.transact({'from':accounts[1], 'value':min_invest * (10 ** invest_decimals) }).buyTokens(accounts[1])
    
    assert moss_coin.call().waiting(accounts[1]) == 0

def test_crowdsale_state_change_only_owner(chain, moss_crowdsale_pre, moss_coin, accounts):
    with pytest.raises(TransactionFailed):
        moss_coin.transact({'from':accounts[1]}).setCrowdsale(moss_crowdsale_pre.address, False)

    assert moss_coin.call().crowdsales(moss_crowdsale_pre.address)

def test_crowdsale_release(chain, moss_crowdsale_pre, moss_coin, coin_owner, accounts, rate, presale_bonus_ether, presale_bonus_rate):
    w3 = chain.web3
    moss_crowdsale_pre.transact({'from':accounts[1], 'value':w3.toWei(1,'ether')}).buyTokens(accounts[1])
    moss_coin.transact({'from':coin_owner}).release(accounts[1])

    assert moss_coin.call().balanceOf(accounts[1]) == presale_token(chain, w3.toWei(1,'ether'), presale_bonus_ether, presale_bonus_rate, rate)

def test_crowdsale_release_only_owner(chain, moss_crowdsale_pre, moss_coin, coin_owner, accounts, rate):
    w3 = chain.web3
    moss_crowdsale_pre.transact({'from':accounts[1], 'value':w3.toWei(1,'ether')}).buyTokens(accounts[1])

    with pytest.raises(TransactionFailed):
        moss_coin.transact({'from':accounts[1]}).release(accounts[1])

    assert moss_coin.call().balanceOf(accounts[1]) == 0

# bonus rating test
def test_crowdsale_bonus_rating(chain, moss_crowdsale_pre, moss_coin, coin_owner, accounts, rate, presale_bonus_ether, presale_bonus_rate):
    w3 = chain.web3
    for criteria in presale_bonus_ether:
        moss_crowdsale_pre.transact({'from':accounts[1], 'value':w3.toWei(1, 'ether') * criteria - 1}).buyTokens(accounts[1])

        assert moss_coin.call().waiting(accounts[1]) == presale_token(chain, w3.toWei(1,'ether') * criteria - 1, presale_bonus_ether, presale_bonus_rate, rate)
        moss_coin.transact({'from':coin_owner}).release(accounts[1])

        moss_crowdsale_pre.transact({'from':accounts[1], 'value':w3.toWei(1, 'ether') * criteria}).buyTokens(accounts[1])

        assert moss_coin.call().waiting(accounts[1]) == presale_token(chain, w3.toWei(1,'ether') * criteria, presale_bonus_ether, presale_bonus_rate, rate)
        moss_coin.transact({'from':coin_owner}).release(accounts[1])