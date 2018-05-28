pragma solidity ^0.4.23;

import "./ownership/Ownable.sol";
import "./token/BurnableToken.sol";
import "./token/PausableToken.sol";

contract MossCoin is PausableToken, BurnableToken {
    string public constant name = "Moss Coin";
    string public constant symbol = "MOC";
    uint8 public constant decimals = 18;

    constructor(uint256 _amount) public
        Ownable()
    {
        totalSupply_ = _amount * 1 ether;
        balances[owner] = totalSupply_;
    }
}