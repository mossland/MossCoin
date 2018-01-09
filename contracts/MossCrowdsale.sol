pragma solidity ^0.4.18;

import './crowdsale/Crowdsale.sol';
import './crowdsale/CappedCrowdsale.sol';

contract MossCrowdsale is CappedCrowdsale {
    function MossCrowdsale(uint256 _startTime, uint256 _endTime, uint256 _rate, uint256 _capEther, uint256 _minInvestFinney, uint256 _maxInvestFinney, address _wallet, address _token) public
        CappedCrowdsale(_capEther)
        Crowdsale(_startTime, _endTime, _rate, _minInvestFinney, _maxInvestFinney, _wallet, _token) 
    {
    }

    function() external payable {
        buyTokens(msg.sender);
    }
}