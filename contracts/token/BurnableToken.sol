pragma solidity ^0.4.21;

import "../ownership/Ownable.sol";
import "./BasicToken.sol";

contract BurnableToken is BasicToken, Ownable {
    event Burn(uint256 value);

    function burn(uint256 _value) onlyOwner public {
        require(_value <= balances[owner]);

        balances[owner] = balances[owner].sub(_value);
        totalSupply_ = totalSupply_.sub(_value);
        emit Burn(_value);
    }
}