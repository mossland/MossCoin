pragma solidity ^0.4.21;

import "../ownership/Ownable.sol";
import "./StandardToken.sol";

contract FreezableToken is StandardToken, Ownable {
    event Freeze(address indexed who, uint256 end);

    mapping(address=>uint256) freezeEnd;

    function freeze(address _who, uint256 _end) onlyOwner public {
        require(_who != address(0));
        require(_end >= freezeEnd[_who]);

        freezeEnd[_who] = _end;

        emit Freeze(_who, _end);
    }

    modifier notFrozen(address _who) {
        require(freezeEnd[_who] < now);
        _;
    }

    function transferFrom(address _from, address _to, uint256 _value) public notFrozen(_from) returns (bool) {
        super.transferFrom(_from, _to, _value);
    }

    function transfer(address _to, uint256 _value) public notFrozen(msg.sender) returns (bool) {
        super.transfer(_to, _value);
    }
}