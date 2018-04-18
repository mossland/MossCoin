pragma solidity ^0.4.21;

import "./crowdsale/Crowdsale.sol";
import "./crowdsale/CappedCrowdsale.sol";

//pre ico crowdsale contract
contract MossCrowdsale is CappedCrowdsale {
    uint256[4] public bonus;
    uint256[4] public ends; // bonus by ico timing criteria
    Crowdsale pre; // pre ico contract

    function MossCrowdsale(uint256 _startTime, uint256 _end1, uint256 _end2, uint256 _end3, uint256 _endTime, uint256 _rate, uint256 _cap, uint256 _minInvestFinney, uint256 _maxInvestFinney, address _wallet, address _token, address _pre) public
        CappedCrowdsale(_cap)
        Crowdsale(_startTime, _endTime, _rate, _minInvestFinney, _maxInvestFinney, _wallet, _token) 
    {
        pre = Crowdsale(_pre);
        ends = [_end1, _end2, _end3, _endTime + 1];
        bonus = [1150, 1100, 1050, 1025];
    }

    function getTokens(uint256 _wei, uint256 _time) public view returns (uint256) {
        require(_time >= startTime && _time <= endTime);

        for (uint i = 0; i < ends.length; ++i) {
            if (_time >= ends[i]) {
                continue;
            }

            return _wei * rate * bonus[i] / 1000;
        }

        assert(false);
    }

    function validPurchase(address beneficiary, uint256 amount) internal view returns (bool) {
        bool withinPeriod = now >= startTime && now <= endTime;
        bool validCondition = beneficiary != 0x0 && msg.value >= minInvest && pre.balanceOf(beneficiary) + balanceOf[beneficiary].add(msg.value) <= maxInvest;
        return super.validPurchase(beneficiary, amount) && withinPeriod && validCondition;
    }
}