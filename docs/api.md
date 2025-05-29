# PiDualTx API Documentation

## Overview

This document describes the REST API endpoints provided by PiDualTx backend services:

- **AI Service**: Price prediction using LSTM model.
- **Rate Service**: Internal and external Pi price data.
- **Smartcontract Service**: Blockchain transaction operations.

---

## AI Service API

### POST `/predict`

Predict the future Pi price based on historical data.

#### Request

- Content-Type: `application/json`
- Body:
  ```json
  {
    "historical_prices": [0.80, 0.81, 0.82, 0.83, 0.84],
    "sequence_length": 5
  }
  ```

#### Response

- Status: `200 OK`
- Body:
  ```json
  {
    "predicted_price": 0.8423,
    "confidence": 0.95
  }
  ```

#### Errors

- `400 Bad Request`: Input validation failure.
- `500 Internal Server Error`: Prediction failed.

---

## Rate Service API

### GET `/api/rates`

Retrieve current Pi price rates.

#### Response

- Status: `200 OK`
- Body:
  ```json
  {
    "internalRate": "314159",
    "externalRate": "0.8152",
    "timestamp": 1680000000
  }
  ```

---

## Smartcontract Service API

### POST `/api/transactions/execute`

Execute a transaction via the PiDualTx smart contract.

#### Request

- Content-Type: `application/json`
- Body:
  ```json
  {
    "user": "GUser Address...",  // User address starting with 'G'
    "merchant": "GMerchantAddress...",  // Merchant address starting with 'G'
    "amount": "1000000000000000000", // Amount in wei
    "paymentType": "internal", // or "external"
    "autoConvert": true
  }
  ```

#### Response

- Status: `200 OK`
- Body:
  ```json
  {
    "transactionHash": "0xabc123...",
    "status": true
  }
  ```

#### Errors

- `400 Bad Request`: Invalid input.
- `500 Internal Server Error`: Transaction failed.

### GET `/api/transactions/{user}`

Retrieve transaction history for a specified user address.

#### Response

- Status: `200 OK`
- Body:
  ```json
  [
    {
      "user": "GUser Address...",  // User address starting with 'G'
      "merchant": "GMerchantAddress...",  // Merchant address starting with 'G'
      "amount": 1000000000000000000,
      "paymentType": "internal",
      "autoConvert": true,
      "timestamp": 1680000123
    },
    {
      "user": "GUser Address...",  // User address starting with 'G'
      "merchant": "GAnotherMerchant...",  // Merchant address starting with 'G'
      "amount": 500000000000000000,
      "paymentType": "external",
      "autoConvert": false,
      "timestamp": 1680000456
    }
  ]
  ```

---

## Notes

- All timestamps are Unix epoch seconds (UTC).
- Amounts are in wei (1 pi = 10^18 wei).
- Payment type is either `"internal"` or `"external"`.
- Make sure to connect to the services via the API gateway or use their Kubernetes cluster IPs as configured.

---

*This document is subject to update as the PiDualTx platform evolves.*
