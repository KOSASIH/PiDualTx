#!/bin/bash
# PiDualTx v15.1 Cijoho Genesis Node #0 Setup Script for Raspberry Pi 5 in Cijoho, Kuningan (-6.979, 108.484)
echo "=== INITIALIZING CIJOHO GENESIS NODE #0 (CAPITAL: CIJOHO) ==="

sudo apt update && sudo apt install -y docker.io docker-compose git curl
sudo systemctl enable docker --now

echo "Cloning PiDualTx Sovereign Repository..."
git clone https://github.com/KOSASIH/PiDualTx.git /opt/pidualtx
cd /opt/pidualtx

echo "Deploying Cijoho Genesis Local Node via Docker Compose..."
docker-compose -f docker-compose.cijoho.yml up -d

echo "=== CIJOHO GENESIS NODE #0 ACTIVE AT (-6.979, 108.484) ==="
