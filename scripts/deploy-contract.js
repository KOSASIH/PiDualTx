// Import the Hardhat runtime environment
const hre = require("hardhat");

async function main() {
    // Get the contract factory
    const PiDualTx = await hre.ethers.getContractFactory("PiDualTx");

    // Deploy the contract
    const piDualTx = await PiDualTx.deploy();

    // Wait for the deployment to be mined
    await piDualTx.deployed();

    console.log("PiDualTx deployed to:", piDualTx.address);
}

// Execute the main function and handle errors
main()
    .then(() => process.exit(0))
    .catch((error) => {
        console.error(error);
        process.exit(1);
    });
