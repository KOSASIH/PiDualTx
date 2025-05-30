// Import the Hardhat runtime environment
const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("PiDualTx Contract", function () {
    let PiDualTx;
    let piDualTx;
    let owner;
    let user1;
    let user2;

    beforeEach(async function () {
        // Get the ContractFactory and Signers
        PiDualTx = await ethers.getContractFactory("PiDualTx");
        [owner, user1, user2] = await ethers.getSigners();

        // Deploy a new instance of the contract for each test
        piDualTx = await PiDualTx.deploy();
        await piDualTx.deployed();
    });

    it("Should set the owner correctly", async function () {
        expect(await piDualTx.owner()).to.equal(owner.address);
    });

    it("Should allow the owner to set the Pi purity badge", async function () {
        await piDualTx.setPiPurityBadge(user1.address, true);
        expect(await piDualTx.validatePiPurityBadge(user1.address)).to.equal(true);
    });

    it("Should not allow non-owners to set the Pi purity badge", async function () {
        await expect(piDualTx.connect(user1).setPiPurityBadge(user1.address, true)).to.be.revertedWith("Ownable: caller is not the owner");
    });

    it("Should allow users to submit transactions", async function () {
        await piDualTx.setPiPurityBadge(user1.address, true);
        await piDualTx.connect(user1).submitTransaction(user1.address, user2.address, 100, "internal", false, "0x123");
        
        const transactions = await piDualTx.getUserTransactions(user1.address);
        expect(transactions.length).to.equal(1);
        expect(transactions[0].amount).to.equal(100);
    });

    it("Should revert if the user has insufficient balance", async function () {
        await piDualTx.setPiPurityBadge(user1.address, true);
        await expect(piDualTx.connect(user1).submitTransaction(user1.address, user2.address, 100, "internal", false, "0x123")).to.be.revertedWith("Invalid user or insufficient balance");
    });
});
