pragma solidity ^0.4.18;

import '../math/SafeMath.sol';
import './Crowdsale.sol';

contract CappedCrowdsale is Crowdsale {
    using SafeMath for uint256;

    uint256 public cap;

    function CappedCrowdsale(uint256 _cap) public {
        require(_cap > 0);
        cap = _cap * 1 ether;
    }

    function validPurchase(address beneficiary) internal view returns (bool) {
        bool withinCap = weiRaised.add(msg.value) <= cap;
        return super.validPurchase(beneficiary) && withinCap;
    }

    function hasEnded() public view returns (bool) {
        bool capReached = weiRaised >= cap;
        return super.hasEnded() || capReached;
    }
}