pragma solidity ^0.4.21;
import "./FreezableToken.sol";

contract StoppableToken is FreezableToken {
    event Stop();
    event Start();

    bool isStop;

    function stop() onlyOwner public {
        isStop = true;
        emit Stop();
    }

    function start() onlyOwner public {
        isStop = false;
        emit Start();
    }

    modifier notFrozen(address _who) {
        require(!isStop);
        require(freezeEnd[_who] < now);
        _;
    }
}