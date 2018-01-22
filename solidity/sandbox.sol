pragma solidity ^0.4.18;

contract SandBox {
    string username;
    uint age;
    
    function setNameAge(string _username, uint _age) public {
        username = _username;
        age = _age;
    }
    
    function getNameAge() public constant returns (string, uint) {
        return (username, age);
    }
}
