# PiDualTx Architecture Overview

## Introduction

PiDualTx is a cutting-edge decentralized application (DApp) built for the Pi Network that implements a robust Dual Value System. This system allows transactions using either an internal community-agreed value or an external market-driven price, providing flexibility and enhanced utility for Pi users.

---

## System Components

### 1. Backend Services

- **AI Service**  
  - Built with FastAPI and TensorFlow.  
  - Provides price predictions using LSTM models.  
  - Uses Redis for caching and state management.  
  - Containerized with Docker and orchestrated by Kubernetes.  

- **Rate Service**  
  - Spring Boot REST API offering real-time internal and external Pi rates.  
  - Integrates with external exchanges like OKX and Bitget to fetch market data.  
  - Performs rate computations and volatility analysis.  
  - Containerized and deployed on Kubernetes for scalability.  

- **Smartcontract Service**  
  - Facilitates interactions with the PiDualTx Solidity smart contract via Web3j.  
  - Exposes REST API endpoints for transaction execution and analytics retrieval.  
  - Ensures secure blockchain transaction handling.  
  - Deployed on Kubernetes with automated scaling capabilities.  

---

### 2. Frontend Application

- Vue 3-based Single Page Application (SPA).  
- Features a modern, responsive UI with auto and manual transaction modes.  
- Integrates Web3 to interact with the Ethereum-compatible PiDualTx smart contract.  
- Supports internationalization (i18n) for English and Indonesian languages.  
- Provides real-time charts and analytics via integrated chart.js component.  
- Packaged using Vue CLI, Dockerized, and managed via Kubernetes deployments.  

---

### 3. Smart Contract (PiDualTx.sol)

- Implemented in Solidity, optimized for Ethereum-compatible chains.  
- Implements the Dual Value System with rigorous security and upgrade considerations.  
- Supports community-driven internal rate updates and oracle-updated external rates.  
- Emits events for all transactions, enabling rich client-side and analytic monitoring.  

---

### 4. Kubernetes Orchestration

- All backend and frontend services are containerized and deployed on Kubernetes clusters.  
- Includes Redis caching deployment for fast data storage and retrieval.  
- Ingress resource manages API routing and frontend access with TLS support.  
- Prometheus and Grafana provide advanced monitoring and alerting capabilities.  

---

## Data Flow Summary

1. Users interact with the **Frontend SPA** to execute transactions or view analytics.  
2. The frontend retrieves predicted prices from the **AI Service** and current rates from the **Rate Service** API.  
3. On transaction execution, the frontend calls the **Smartcontract Service** API, which interacts with the blockchain smart contract to submit the transaction.  
4. The **Smartcontract** emits events recorded for analytics, while backend services update rates and monitor health metrics.  
5. Kubernetes ensures high availability and scalability of all components, supported by centralized monitoring solutions.  

---

## Technology Stack

| Component           | Technology                              |
|---------------------|---------------------------------------|
| Backend AI Service   | Python, FastAPI, TensorFlow, Redis    |
| Backend Rate Service | Java, Spring Boot, WebFlux, Reactor   |
| Backend Smartcontract| Java, Spring Boot, Web3j               |
| Frontend            | Vue 3, Vuex, Vue Router, Web3.js      |
| Smart Contract      | Solidity                              |
| Containerization    | Docker                               |
| Orchestration       | Kubernetes                           |
| Monitoring          | Prometheus, Grafana                  |
| Caching             | Redis                               |

---

## Security Considerations

- All smart contract functions have access control checks.  
- Backend APIs validate user inputs to prevent malformed transactions.  
- Services communicate over secured channels with token-based or mutual TLS where applicable.  
- Kubernetes deployments enable resource limits and readiness/liveness probes to ensure reliability.  

---

## Future Enhancements

- Full integration with decentralized oracles to automate external rate feeding.  
- Implementation of on-chain governance features for internal rate adjustments.  
- Enhanced analytics dashboards powered by time-series blockchain data indexing.  
- Support for additional languages and accessibility improvements.  
- Automated CI/CD pipelines for seamless deployments and updates.  

---

*This document serves as a living guide to the PiDualTx system architecture and intended for developers, maintainers, and community stakeholders.*
```
