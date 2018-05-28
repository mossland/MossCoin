pragma solidity ^0.4.21;

import "../math/SafeMath.sol";
import "./Crowdsale.sol";

contract CappedCrowdsale is Crowdsale {
    using SafeMath for uint256;

    uint256 public cap;
    uint256 startSaled;

    function CappedCrowdsale(uint256 _cap) public {
        require(_cap > 0);
        cap = _cap * 1 ether;
        startSaled = token.saled();
    }

    function validPurchase(address beneficiary, uint256 amount) internal view returns (bool) {
        bool withinCap = token.saled().add(amount) <= startSaled.add(cap);
        return super.validPurchase(beneficiary, amount) && withinCap;
    }

    function hasEnded() public view returns (bool) {
        bool capReached = token.saled() >= startSaled.add(cap);
        return super.hasEnded() || capReached;
    }
}