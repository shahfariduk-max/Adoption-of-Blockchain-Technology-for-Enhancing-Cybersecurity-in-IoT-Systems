// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract IoTSecurity {
    struct Device {
        bool isRegistered;
        bool isBlocked;
        string deviceType;
    }

    mapping(address => Device) public devices;
    address public admin;

    event AccessDenied(address indexed device, string reason);
    event DataLogged(address indexed device, bytes32 dataHash);

    constructor() {
        admin = msg.sender;
    }

    // Fixed Modifier name to standard English characters
    modifier onlyAdmin() {
        require(msg.sender == admin, "Not authorized");
        _;
    }

    function registerDevice(address _dev, string memory _type) public onlyAdmin {
        devices[_dev] = Device(true, false, _type);
    }

    function blockDevice(address _dev) public onlyAdmin {
        devices[_dev].isBlocked = true;
    }

    function validateTraffic(address _dev, bytes32 _dataHash) public {
        require(devices[_dev].isRegistered, "Device not in registry");
        require(!devices[_dev].isBlocked, "Device is blocked due to anomaly");
        
        emit DataLogged(_dev, _dataHash);
    }
}