// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract PiDualTx {
    // Structure for transactions
    struct Transaction {
        address user;          // Address of the user making the transaction
        address merchant;      // Address of the merchant (0x0 if none)
        uint256 amount;        // Amount of Pi in wei
        string paymentType;    // "internal" or "external"
        bool autoConvert;      // Whether to convert to fiat
        uint256 timestamp;     // Transaction time
    }

    // Mapping to track Pi ownership (for Pi Purity Badge)
    mapping(address => bool) public isPurePiHolder;
    mapping(address => uint256) public piBalance;

    // List of transactions
    Transaction[] private transactions;

    // Address of the admin (for initial configuration)
    address public admin;

    // Event for analytics and tracking
    event TransactionRecorded(
        address indexed user,
        address indexed merchant,
        uint256 amount,
        string paymentType,
        bool autoConvert,
        uint256 timestamp
    );

    event PiPurityValidated(address indexed user, bool isPure);
    event PiBalanceUpdated(address indexed user, uint256 balance);
    event AdminTransferred(address indexed previousAdmin, address indexed newAdmin);

    // Modifier to restrict access
    modifier onlyAdmin() {
        require(msg.sender == admin, "Only admin is allowed");
        _;
    }

    modifier onlyValidUser(address user) {
        require(user != address(0), "Invalid user address");
        require(piBalance[user] > 0, "Insufficient Pi balance");
        _;
    }

    constructor() {
        admin = msg.sender;
    }

    // Function to set Pi Purity status (called by admin or oracle)
    function setPiPurity(address user, bool isPure) external onlyAdmin {
        isPurePiHolder[user] = isPure;
        emit PiPurityValidated(user, isPure);
    }

    // Function to update Pi balance (simulating mining/transfers)
    function updatePiBalance(address user, uint256 amount) external onlyAdmin {
        require(user != address(0), "Invalid user address");
        piBalance[user] += amount; // Allow incrementing balance
        emit PiBalanceUpdated(user, piBalance[user]);
    }

    // Function to perform a transaction
    function submitTransaction(
        address user,
        address merchant,
        uint256 amount,
        string memory paymentType,
        bool autoConvert
    ) external onlyValidUser(user) {
        require(
            keccak256(abi.encodePacked(paymentType)) == keccak256(abi.encodePacked("internal")) ||
            keccak256(abi.encodePacked(paymentType)) == keccak256(abi.encodePacked("external")),
            "Invalid payment type"
        );
        require(amount > 0, "Amount must be greater than 0");
        require(piBalance[user] >= amount, "Insufficient balance");

        // Deduct user's balance
        piBalance[user] -= amount;
        if (merchant != address(0)) {
            piBalance[merchant] += amount; // Credit merchant if applicable
        }

        // Record transaction
        transactions.push(Transaction({
            user: user,
            merchant: merchant,
            amount: amount,
            paymentType: paymentType,
            autoConvert: autoConvert,
            timestamp: block.timestamp
        }));

        // Emit event for analytics
        emit TransactionRecorded(user, merchant, amount, paymentType, autoConvert, block.timestamp);
    }

    // Function to validate Pi Purity
    function validatePiPurity(address user) external view returns (bool) {
        return isPurePiHolder[user];
    }

    // Function to retrieve user or merchant transaction history
    function getUserTransactions(address user) external view returns (Transaction[] memory) {
        uint256 count = 0;
        for (uint256 i = 0; i < transactions.length; i++) {
            if (transactions[i].user == user || transactions[i].merchant == user) {
                count++;
            }
        }

        Transaction[] memory result = new Transaction[](count);
        uint256 index = 0;
        for (uint256 i = 0; i < transactions.length; i++) {
            if (transactions[i].user == user || transactions[i].merchant == user) {
                result[index] = transactions[i];
                index++;
            }
        }
        return result;
    }

    // Function to get the total number of transactions
    function getTransactionCount() external view returns (uint256) {
        return transactions.length;
    }

    // Function for admin to transfer admin rights
    function transferAdmin(address newAdmin) external onlyAdmin {
        require(newAdmin != address(0), "Invalid new admin");
        emit AdminTransferred(admin, newAdmin);
        admin = newAdmin;
    }

    // Function to get the balance of a user
    function getPiBalance(address user) external view returns (uint256) {
        return piBalance[user];
    }

    // Function to get the total balance of all users (for analytics)
    function getTotalBalance() external view returns (uint256 total) {
        for (uint256 i = 0; i < transactions.length; i++) {
            total += transactions[i].amount;
        }
    }

    // Function to get the last transaction of a user
    function getLastTransaction(address user) external view returns (Transaction memory) {
        for (uint256 i = transactions.length; i > 0; i--) {
            if (transactions[i - 1].user == user || transactions[i - 1].merchant == user) {
                return transactions[i - 1];
            }
        }
        revert("No transactions found for this user");
    }
}
