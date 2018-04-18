pragma solidity ^0.4.21;
import "../math/SafeMath.sol";
import "../ownership/Ownable.sol";
import "./StandardToken.sol";

contract CrowdsaleToken is StandardToken, Ownable {
    using SafeMath for uint256;
    address public crowdsale;
    mapping (address => uint256) public waiting;
    uint256 public saled;

    event Sale(address indexed to, uint256 value);
    event Release(address indexed to);
    event Reject(address indexed to);
    event SetCrowdsale(address indexed addr);

    function setCrowdsale(address _addr) onlyOwner public {
        crowdsale = _addr;
        emit SetCrowdsale(_addr);
    }

    modifier onlyCrowdsale() {
        require(crowdsale != address(0));
        require(crowdsale == msg.sender);
        _;
    }

    function sale(address _to, uint256 _value) public onlyCrowdsale returns (bool) {
        require(_to != address(0));
        assert(saled.add(_value) <= balances[owner]);

        saled = saled.add(_value);
        waiting[_to] = waiting[_to].add(_value);
        emit Sale(_to, _value);
        return true;
    }

    // send waiting tokens to customer's balance
    function release(address _to) external onlyOwner {
        require(_to != address(0));

        uint256 val = waiting[_to];
        waiting[_to] = 0;
        balances[owner] = balances[owner].sub(val);
        balances[_to] = balances[_to].add(val);
        emit Release(_to);
    }

    // reject waiting token
    function reject(address _to) external onlyOwner {
        require(_to != address(0));

        saled = saled.sub(waiting[_to]);
        waiting[_to] = 0;

        emit Reject(_to);
    }
}