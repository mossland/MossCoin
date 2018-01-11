import pytest
import web3.contract
import web3.eth
import time
from ethereum.tester import TransactionFailed

def presale_bonus(chain, wei):
    bonus_line = [5, 10, 25, 75]
    bonus_rate = [130, 135, 140, 145, 150]

    for i in range(0, 4):
        if wei < bonus_line[i] * chain.web3.toWei(1,'ether'):
            return bonus_rate[i]
    
    return bonus_rate[-1]

def presale_token(chain, wei, rate):
    return wei * rate * presale_bonus(chain, wei) // 100

def test_crowdsale_initialized(moss_crowdsale_pre, moss_coin, coin_owner, period, min_invest, max_invest, cap, rate, token_decimals, invest_decimals):
    assert moss_crowdsale_pre.call().endTime() - moss_crowdsale_pre.call().startTime() == period
    assert moss_crowdsale_pre.call().minInvest() == (min_invest * (10 ** invest_decimals))
    assert moss_crowdsale_pre.call().maxInvest() == (max_invest * (10 ** invest_decimals))
    assert moss_crowdsale_pre.call().cap() == (cap * (10 ** token_decimals))
    assert moss_crowdsale_pre.call().weiRaised() == 0
    assert moss_crowdsale_pre.call().token().lower() == moss_coin.address
    assert moss_crowdsale_pre.call().wallet() == coin_owner

def test_crowdsale_buy(chain, moss_crowdsale_pre, moss_coin, coin_owner, accounts, rate):
    w3 = chain.web3
    moss_crowdsale_pre.transact({'from':accounts[1], 'value':w3.toWei(1,'ether')}).buyTokens(accounts[1])

    assert moss_coin.call().waiting(accounts[1]) == presale_token(chain, w3.toWei(1,'ether'), rate)

def test_crowdsale_buy_fallback(chain, moss_crowdsale_pre, moss_coin, accounts, rate):
    w3 = chain.web3
    w3.eth.sendTransaction({'from':accounts[1], 'to':moss_crowdsale_pre.address, 'value':w3.toWei(1,'ether')})
    assert moss_coin.call().waiting(accounts[1]) == presale_token(chain, w3.toWei(1,'ether'), rate)

def test_crowdsale_min_invest(chain, moss_crowdsale_pre, moss_coin, accounts, min_invest, invest_decimals, rate):
    with pytest.raises(TransactionFailed):
        moss_crowdsale_pre.transact({'from':accounts[1], 'value':min_invest * (10 ** invest_decimals) - 1}).buyTokens(accounts[1])

    assert moss_coin.call().waiting(accounts[1]) == 0

    moss_crowdsale_pre.transact({'from':accounts[1], 'value':min_invest * (10 ** invest_decimals) }).buyTokens(accounts[1])
    assert moss_coin.call().waiting(accounts[1]) == presale_token(chain, min_invest * (10 ** invest_decimals), rate)

def test_crowdsale_max_invest(chain, moss_crowdsale_pre, moss_coin, accounts, min_invest, max_invest, invest_decimals, rate):
    with pytest.raises(TransactionFailed):
        moss_crowdsale_pre.transact({'from':accounts[1], 'value':max_invest * (10 ** invest_decimals) + 1}).buyTokens(accounts[1])
    
    moss_crowdsale_pre.transact({'from':accounts[2], 'value':(max_invest-min_invest) * (10 ** invest_decimals) + 1}).buyTokens(accounts[2])

    with pytest.raises(TransactionFailed):
        moss_crowdsale_pre.transact({'from':accounts[2], 'value': min_invest * (10 ** invest_decimals)}).buyTokens(accounts[2])
    
    assert moss_coin.call().waiting(accounts[1]) == 0
    assert moss_coin.call().waiting(accounts[2]) == presale_token(chain, (max_invest-min_invest) * (10 ** invest_decimals) + 1, rate)

def test_crowdsale_state_change(chain, moss_crowdsale_pre, moss_coin, coin_owner, accounts, min_invest, invest_decimals):
    moss_coin.transact({'from':coin_owner}).setCrowdsale(moss_crowdsale_pre.address, False)

    with pytest.raises(TransactionFailed):
        moss_crowdsale_pre.transact({'from':accounts[1], 'value':min_invest * (10 ** invest_decimals) }).buyTokens(accounts[1])
    
    assert moss_coin.call().waiting(accounts[1]) == 0

def test_crowdsale_state_change_only_owner(chain, moss_crowdsale_pre, moss_coin, accounts):
    with pytest.raises(TransactionFailed):
        moss_coin.transact({'from':accounts[1]}).setCrowdsale(moss_crowdsale_pre.address, False)

    assert moss_coin.call().crowdsales(moss_crowdsale_pre.address)

def test_crowdsale_release(chain, moss_crowdsale_pre, moss_coin, coin_owner, accounts, rate):
    w3 = chain.web3
    moss_crowdsale_pre.transact({'from':accounts[1], 'value':w3.toWei(1,'ether')}).buyTokens(accounts[1])
    moss_coin.transact({'from':coin_owner}).release(accounts[1])

    assert moss_coin.call().balanceOf(accounts[1]) == presale_token(chain, w3.toWei(1,'ether'), rate)

def test_crowdsale_release_only_owner(chain, moss_crowdsale_pre, moss_coin, coin_owner, accounts, rate):
    w3 = chain.web3
    moss_crowdsale_pre.transact({'from':accounts[1], 'value':w3.toWei(1,'ether')}).buyTokens(accounts[1])

    with pytest.raises(TransactionFailed):
        moss_coin.transact({'from':accounts[1]}).release(accounts[1])

    assert moss_coin.call().balanceOf(accounts[1]) == 0