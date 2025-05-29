package com.pidualtx.smartcontract;

import org.web3j.protocol.Web3j;
import org.web3j.tx.gas.ContractGasProvider;
import org.web3j.tx.Contract;
import org.web3j.tx.TransactionManager;
import org.web3j.protocol.core.RemoteCall;
import org.web3j.protocol.core.methods.response.TransactionReceipt;

import java.math.BigInteger;
import java.util.Arrays;
import java.util.Collections;
import java.util.concurrent.CompletableFuture;

import org.web3j.abi.datatypes.Type;
import org.web3j.abi.datatypes.Address;
import org.web3j.abi.datatypes.Bool;
import org.web3j.abi.datatypes.generated.Uint256;
import org.web3j.abi.datatypes.Utf8String;
import org.web3j.abi.datatypes.Function;
import org.web3j.crypto.Credentials;
import org.web3j.protocol.core.RemoteFunctionCall;

/**
 * PiDualTxContract Java wrapper for the PiDualTx Solidity smart contract.
 * Generated partially manually for demonstration with advanced transaction methods.
 *
 * Features:
 *  - Methods to call executeTransaction with detailed parameters.
 *  - Support for async calls and transaction receipts.
 *  - Gas provider configurable for efficient gas usage.
 */
public class PiDualTxContract extends Contract {

    public static final String BINARY = "";

    protected PiDualTxContract(String contractAddress, Web3j web3j, Credentials credentials, ContractGasProvider contractGasProvider) {
        super(BINARY, contractAddress, web3j, credentials, contractGasProvider);
    }

    protected PiDualTxContract(String contractAddress, Web3j web3j, TransactionManager transactionManager, ContractGasProvider contractGasProvider) {
        super(BINARY, contractAddress, web3j, transactionManager, contractGasProvider);
    }

    /**
     * Executes a transaction on the PiDualTx contract.
     *
     * @param user User address (string)
     * @param merchant Merchant address (string)
     * @param amount Amount in wei (BigInteger)
     * @param paymentType Payment type: "internal" or "external"
     * @param autoConvert Boolean flag whether to auto-convert
     * @return RemoteCall<TransactionReceipt> transaction receipt future
     */
    public RemoteCall<TransactionReceipt> executeTransaction(
            String user,
            String merchant,
            BigInteger amount,
            String paymentType,
            boolean autoConvert) {

        final Function function = new Function(
                "executeTransaction",
                Arrays.<Type>asList(
                        new Address(user),
                        new Address(merchant),
                        new Uint256(amount),
                        new Utf8String(paymentType),
                        new Bool(autoConvert)
                ),
                Collections.emptyList());

        return executeRemoteCallTransaction(function);
    }

    /**
     * Loads an existing contract instance.
     *
     * @param contractAddress Deployed contract address
     * @param web3j Web3j instance
     * @param credentials Wallet credentials
     * @param contractGasProvider Gas provider
     * @return PiDualTxContract instance
     */
    public static PiDualTxContract load(String contractAddress, Web3j web3j, Credentials credentials, ContractGasProvider contractGasProvider) {
        return new PiDualTxContract(contractAddress, web3j, credentials, contractGasProvider);
    }

    /**
     * Loads an existing contract instance with TransactionManager (e.g., for managed wallet)
     */
    public static PiDualTxContract load(String contractAddress, Web3j web3j, TransactionManager transactionManager, ContractGasProvider contractGasProvider) {
        return new PiDualTxContract(contractAddress, web3j, transactionManager, contractGasProvider);
    }
}
