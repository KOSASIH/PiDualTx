package com.pidualtx.smartcontract;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.web3j.protocol.Web3j;
import org.web3j.protocol.core.RemoteCall;
import org.web3j.protocol.core.methods.response.TransactionReceipt;
import org.web3j.protocol.http.HttpService;
import org.web3j.tx.gas.DefaultGasProvider;

import java.math.BigInteger;
import java.util.HashMap;
import java.util.Map;

/**
 * TransactionController
 * REST API Controller for interacting with PiDualTx smart contract:
 * - Execute transactions on-chain
 * - Query transaction analytics
 * - Provide safe and secure endpoints supporting blockchain tx
 */
@RestController
@RequestMapping("/api/transactions")
public class TransactionController {

    private final PiDualTxContract piDualTxContract;

    @Autowired
    public TransactionController(PiDualTxContract piDualTxContract) {
        this.piDualTxContract = piDualTxContract;
    }

    /**
     * POST /api/transactions/execute
     * Execute a PiDualTx transaction on-chain.
     * Request body expects user address, merchant address, amount (wei), payment type, and autoConvert flag.
     *
     * @param request TransactionRequest payload
     * @return ResponseEntity with tx hash or error
     */
    @PostMapping("/execute")
    public ResponseEntity<?> executeTransaction(@RequestBody TransactionRequest request) {
        try {
            // Validate inputs
            if (request.getUser() == null || request.getUser().isEmpty()) {
                return ResponseEntity.badRequest().body("User address is required");
            }
            if (request.getAmount() == null || request.getAmount().compareTo(BigInteger.ZERO) <= 0) {
                return ResponseEntity.badRequest().body("Amount must be positive");
            }

            // Call smart contract executeTransaction method
            RemoteCall<TransactionReceipt> remoteCall = piDualTxContract.executeTransaction(
                    request.getUser(),
                    request.getMerchant(),
                    request.getAmount(),
                    request.getPaymentType(),
                    request.isAutoConvert());

            TransactionReceipt receipt = remoteCall.send();

            Map<String, Object> response = new HashMap<>();
            response.put("transactionHash", receipt.getTransactionHash());
            response.put("status", receipt.isStatusOK());

            return ResponseEntity.ok(response);

        } catch (Exception e) {
            return ResponseEntity.status(500).body("Transaction failed: " + e.getMessage());
        }
    }

    /**
     * GET /api/transactions/{user}
     * Retrieve transaction history for a user.
     *
     * @param user Ethereum address of the user
     * @return List of transactions or error
     */
    @GetMapping("/{user}")
    public ResponseEntity<?> getTransactionsByUser(@PathVariable String user) {
        try {
            if (user == null || user.isEmpty()) {
                return ResponseEntity.badRequest().body("User address is required");
            }

            // Call contract method to get transactions
            // Note: This requires the contract to expose such a method, otherwise
            //       transaction history should be maintained off-chain or indexed.
            // For demo, returning empty or placeholder response.
            // Replace with real implementation as appropriate.

            return ResponseEntity.ok(new String[]{"Transaction history fetching not implemented on-chain. Use off-chain analytics."});

        } catch (Exception e) {
            return ResponseEntity.status(500).body("Failed to retrieve transactions: " + e.getMessage());
        }
    }

    // DTO for transaction request
    public static class TransactionRequest {
        private String user;
        private String merchant;
        private BigInteger amount;
        private String paymentType;
        private boolean autoConvert;

        public String getUser() { return user; }
        public void setUser(String user) { this.user = user; }

        public String getMerchant() { return merchant; }
        public void setMerchant(String merchant) { this.merchant = merchant; }

        public BigInteger getAmount() { return amount; }
        public void setAmount(BigInteger amount) { this.amount = amount; }

        public String getPaymentType() { return paymentType; }
        public void setPaymentType(String paymentType) { this.paymentType = paymentType; }

        public boolean isAutoConvert() { return autoConvert; }
        public void setAutoConvert(boolean autoConvert) { this.autoConvert = autoConvert; }
    }
}

