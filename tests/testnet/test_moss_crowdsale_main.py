import pytest
import web3.contract
import web3.eth
import time
from ethereum.tester import TransactionFailed

@pytest.fixture
def bonus_ether():
    return [5, 10, 25, 75]

@pytest.fixture
def bonus_rate():
    return [ [1250, 1300, 1350, 1400, 1450]
           , [1150, 1200, 1250, 1350, 1400]
           , [1050, 1075, 1125, 1250, 1300]
           , [1025, 1025, 1050, 1100, 1200] ]

def test_bonus_property(bonus_ether, bonus_rate):
    for rate in bonus_rate:
        assert len(bonus_ether) + 1 == len(rate)

def sale_bonus(chain, wei, now, bonus_ether, bonus_rate, start, main_bonus_change_period):
    period_idx = -1
    
    for j in range(1, 4):
        if now < start + j * main_bonus_change_period:
            period_idx = j - 1
            break
    
    if period_idx == -1:
        period_idx = 3

    for i in range(0, 4):
        if wei < bonus_ether[i] * chain.web3.toWei(1,'ether'):
            return bonus_rate[period_idx][i]
    
    return bonus_rate[period_idx][-1]

def token_amount(chain, wei, now, bonus_ether, bonus_rate, rate, start, main_bonus_change_period):
    return wei * rate * sale_bonus(chain, wei, now, bonus_ether, bonus_rate, start, main_bonus_change_period) // 1000

def test_main_bonus_rating(chain, bonus_ether, bonus_rate, rate, testernet_start, main_period, main_bonus_change_period):
    w3 = chain.web3
    start = testernet_start
    end = testernet_start + main_period

    # 1st week
    week1end = start + main_bonus_change_period - 1

    assert token_amount(chain, 5 * w3.toWei(1, 'ether') - 1,  week1end, bonus_ether, bonus_rate, rate, testernet_start, main_bonus_change_period) == 31250000000000000000000 - 6250
    assert token_amount(chain, 5 * w3.toWei(1, 'ether'),      week1end, bonus_ether, bonus_rate, rate, testernet_start, main_bonus_change_period) == 32500000000000000000000
    assert token_amount(chain, 10 * w3.toWei(1, 'ether') - 1, week1end, bonus_ether, bonus_rate, rate, testernet_start, main_bonus_change_period) == 65000000000000000000000 - 6500
    assert token_amount(chain, 10 * w3.toWei(1, 'ether'),     week1end, bonus_ether, bonus_rate, rate, testernet_start, main_bonus_change_period) == 67500000000000000000000
    assert token_amount(chain, 25 * w3.toWei(1, 'ether') - 1, week1end, bonus_ether, bonus_rate, rate, testernet_start, main_bonus_change_period) == 168750000000000000000000 - 6750
    assert token_amount(chain, 25 * w3.toWei(1, 'ether'),     week1end, bonus_ether, bonus_rate, rate, testernet_start, main_bonus_change_period) == 175000000000000000000000
    assert token_amount(chain, 75 * w3.toWei(1, 'ether') - 1, week1end, bonus_ether, bonus_rate, rate, testernet_start, main_bonus_change_period) == 525000000000000000000000 - 7000
    assert token_amount(chain, 75 * w3.toWei(1, 'ether'),     week1end, bonus_ether, bonus_rate, rate, testernet_start, main_bonus_change_period) == 543750000000000000000000
    
    # 2nd week
    week2start = start + main_bonus_change_period
    week2end = start + 2 * main_bonus_change_period - 1

    assert token_amount(chain, 5 * w3.toWei(1, 'ether') - 1,  week2start, bonus_ether, bonus_rate, rate, testernet_start, main_bonus_change_period) == 28750000000000000000000 - 5750
    assert token_amount(chain, 5 * w3.toWei(1, 'ether'),      week2start, bonus_ether, bonus_rate, rate, testernet_start, main_bonus_change_period) == 30000000000000000000000
    assert token_amount(chain, 10 * w3.toWei(1, 'ether') - 1, week2start, bonus_ether, bonus_rate, rate, testernet_start, main_bonus_change_period) == 60000000000000000000000 - 6000
    assert token_amount(chain, 10 * w3.toWei(1, 'ether'),     week2start, bonus_ether, bonus_rate, rate, testernet_start, main_bonus_change_period) == 62500000000000000000000
    assert token_amount(chain, 25 * w3.toWei(1, 'ether') - 1, week2start, bonus_ether, bonus_rate, rate, testernet_start, main_bonus_change_period) == 156250000000000000000000 - 6250
    assert token_amount(chain, 25 * w3.toWei(1, 'ether'),     week2start, bonus_ether, bonus_rate, rate, testernet_start, main_bonus_change_period) == 168750000000000000000000
    assert token_amount(chain, 75 * w3.toWei(1, 'ether') - 1, week2start, bonus_ether, bonus_rate, rate, testernet_start, main_bonus_change_period) == 506250000000000000000000 - 6750
    assert token_amount(chain, 75 * w3.toWei(1, 'ether'),     week2start, bonus_ether, bonus_rate, rate, testernet_start, main_bonus_change_period) == 525000000000000000000000

    assert token_amount(chain, 5 * w3.toWei(1, 'ether') - 1,  week2end, bonus_ether, bonus_rate, rate, testernet_start, main_bonus_change_period) == 28750000000000000000000 - 5750
    assert token_amount(chain, 5 * w3.toWei(1, 'ether'),      week2end, bonus_ether, bonus_rate, rate, testernet_start, main_bonus_change_period) == 30000000000000000000000
    assert token_amount(chain, 10 * w3.toWei(1, 'ether') - 1, week2end, bonus_ether, bonus_rate, rate, testernet_start, main_bonus_change_period) == 60000000000000000000000 - 6000
    assert token_amount(chain, 10 * w3.toWei(1, 'ether'),     week2end, bonus_ether, bonus_rate, rate, testernet_start, main_bonus_change_period) == 62500000000000000000000
    assert token_amount(chain, 25 * w3.toWei(1, 'ether') - 1, week2end, bonus_ether, bonus_rate, rate, testernet_start, main_bonus_change_period) == 156250000000000000000000 - 6250
    assert token_amount(chain, 25 * w3.toWei(1, 'ether'),     week2end, bonus_ether, bonus_rate, rate, testernet_start, main_bonus_change_period) == 168750000000000000000000
    assert token_amount(chain, 75 * w3.toWei(1, 'ether') - 1, week2end, bonus_ether, bonus_rate, rate, testernet_start, main_bonus_change_period) == 506250000000000000000000 - 6750
    assert token_amount(chain, 75 * w3.toWei(1, 'ether'),     week2end, bonus_ether, bonus_rate, rate, testernet_start, main_bonus_change_period) == 525000000000000000000000
    
    # 3rd week
    week3start = start + 2 * main_bonus_change_period
    week3end = start + 3 * main_bonus_change_period - 1

    assert token_amount(chain, 5 * w3.toWei(1, 'ether') - 1,  week3start, bonus_ether, bonus_rate, rate, testernet_start, main_bonus_change_period) == 26250000000000000000000 - 5250
    assert token_amount(chain, 5 * w3.toWei(1, 'ether'),      week3start, bonus_ether, bonus_rate, rate, testernet_start, main_bonus_change_period) == 26875000000000000000000
    assert token_amount(chain, 10 * w3.toWei(1, 'ether') - 1, week3start, bonus_ether, bonus_rate, rate, testernet_start, main_bonus_change_period) == 53750000000000000000000 - 5375
    assert token_amount(chain, 10 * w3.toWei(1, 'ether'),     week3start, bonus_ether, bonus_rate, rate, testernet_start, main_bonus_change_period) == 56250000000000000000000
    assert token_amount(chain, 25 * w3.toWei(1, 'ether') - 1, week3start, bonus_ether, bonus_rate, rate, testernet_start, main_bonus_change_period) == 140625000000000000000000 - 5625
    assert token_amount(chain, 25 * w3.toWei(1, 'ether'),     week3start, bonus_ether, bonus_rate, rate, testernet_start, main_bonus_change_period) == 156250000000000000000000
    assert token_amount(chain, 75 * w3.toWei(1, 'ether') - 1, week3start, bonus_ether, bonus_rate, rate, testernet_start, main_bonus_change_period) == 468750000000000000000000 - 6250
    assert token_amount(chain, 75 * w3.toWei(1, 'ether'),     week3start, bonus_ether, bonus_rate, rate, testernet_start, main_bonus_change_period) == 487500000000000000000000

    assert token_amount(chain, 5 * w3.toWei(1, 'ether') - 1,  week3end, bonus_ether, bonus_rate, rate, testernet_start, main_bonus_change_period) == 26250000000000000000000 - 5250
    assert token_amount(chain, 5 * w3.toWei(1, 'ether'),      week3end, bonus_ether, bonus_rate, rate, testernet_start, main_bonus_change_period) == 26875000000000000000000
    assert token_amount(chain, 10 * w3.toWei(1, 'ether') - 1, week3end, bonus_ether, bonus_rate, rate, testernet_start, main_bonus_change_period) == 53750000000000000000000 - 5375
    assert token_amount(chain, 10 * w3.toWei(1, 'ether'),     week3end, bonus_ether, bonus_rate, rate, testernet_start, main_bonus_change_period) == 56250000000000000000000
    assert token_amount(chain, 25 * w3.toWei(1, 'ether') - 1, week3end, bonus_ether, bonus_rate, rate, testernet_start, main_bonus_change_period) == 140625000000000000000000 - 5625
    assert token_amount(chain, 25 * w3.toWei(1, 'ether'),     week3end, bonus_ether, bonus_rate, rate, testernet_start, main_bonus_change_period) == 156250000000000000000000
    assert token_amount(chain, 75 * w3.toWei(1, 'ether') - 1, week3end, bonus_ether, bonus_rate, rate, testernet_start, main_bonus_change_period) == 468750000000000000000000 - 6250
    assert token_amount(chain, 75 * w3.toWei(1, 'ether'),     week3end, bonus_ether, bonus_rate, rate, testernet_start, main_bonus_change_period) == 487500000000000000000000

    # 4th week
    week4start = start + 3 * main_bonus_change_period
    week4end = end

    assert token_amount(chain, 5 * w3.toWei(1, 'ether') - 1,  week4start, bonus_ether, bonus_rate, rate, testernet_start, main_bonus_change_period) == 25625000000000000000000 - 5125
    assert token_amount(chain, 5 * w3.toWei(1, 'ether'),      week4start, bonus_ether, bonus_rate, rate, testernet_start, main_bonus_change_period) == 25625000000000000000000
    assert token_amount(chain, 10 * w3.toWei(1, 'ether') - 1, week4start, bonus_ether, bonus_rate, rate, testernet_start, main_bonus_change_period) == 51250000000000000000000 - 5125
    assert token_amount(chain, 10 * w3.toWei(1, 'ether'),     week4start, bonus_ether, bonus_rate, rate, testernet_start, main_bonus_change_period) == 52500000000000000000000
    assert token_amount(chain, 25 * w3.toWei(1, 'ether') - 1, week4start, bonus_ether, bonus_rate, rate, testernet_start, main_bonus_change_period) == 131250000000000000000000 - 5250
    assert token_amount(chain, 25 * w3.toWei(1, 'ether'),     week4start, bonus_ether, bonus_rate, rate, testernet_start, main_bonus_change_period) == 137500000000000000000000
    assert token_amount(chain, 75 * w3.toWei(1, 'ether') - 1, week4start, bonus_ether, bonus_rate, rate, testernet_start, main_bonus_change_period) == 412500000000000000000000 - 5500
    assert token_amount(chain, 75 * w3.toWei(1, 'ether'),     week4start, bonus_ether, bonus_rate, rate, testernet_start, main_bonus_change_period) == 450000000000000000000000

    assert token_amount(chain, 5 * w3.toWei(1, 'ether') - 1,  week4end, bonus_ether, bonus_rate, rate, testernet_start, main_bonus_change_period) == 25625000000000000000000 - 5125
    assert token_amount(chain, 5 * w3.toWei(1, 'ether'),      week4end, bonus_ether, bonus_rate, rate, testernet_start, main_bonus_change_period) == 25625000000000000000000
    assert token_amount(chain, 10 * w3.toWei(1, 'ether') - 1, week4end, bonus_ether, bonus_rate, rate, testernet_start, main_bonus_change_period) == 51250000000000000000000 - 5125
    assert token_amount(chain, 10 * w3.toWei(1, 'ether'),     week4end, bonus_ether, bonus_rate, rate, testernet_start, main_bonus_change_period) == 52500000000000000000000
    assert token_amount(chain, 25 * w3.toWei(1, 'ether') - 1, week4end, bonus_ether, bonus_rate, rate, testernet_start, main_bonus_change_period) == 131250000000000000000000 - 5250
    assert token_amount(chain, 25 * w3.toWei(1, 'ether'),     week4end, bonus_ether, bonus_rate, rate, testernet_start, main_bonus_change_period) == 137500000000000000000000
    assert token_amount(chain, 75 * w3.toWei(1, 'ether') - 1, week4end, bonus_ether, bonus_rate, rate, testernet_start, main_bonus_change_period) == 412500000000000000000000 - 5500
    assert token_amount(chain, 75 * w3.toWei(1, 'ether'),     week4end, bonus_ether, bonus_rate, rate, testernet_start, main_bonus_change_period) == 450000000000000000000000