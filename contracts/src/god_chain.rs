#![no_std]
extern crate alloc;

use soroban_sdk::{contract, contractimpl, contracttype, symbol_short, Address, Env, Bytes, String};

#[contracttype]
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct GodChainRegistry {
    pub chain_id: u64,
    pub merkle_root: Bytes,
    pub active_civilizations_count: u32,
    pub arweave_memo_hash: Bytes,
}

#[contract]
pub struct GodChainContract;

#[contractimpl]
impl GodChainContract {
    pub fn __constructor(env: Env, merkle_root: Bytes, arweave_memo_hash: Bytes) {
        let registry = GodChainRegistry {
            chain_id: 314159,
            merkle_root,
            active_civilizations_count: 1,
            arweave_memo_hash,
        };
        env.storage().instance().set(&symbol_short!("god_chain"), &registry);
    }

    pub fn anchor_civilization_gcv(env: Env, civilization_id: Address, zk_purity_proof: Bytes) {
        civilization_id.require_auth();
        if zk_purity_proof.len() < 32 {
            panic!("God-Chain Anchor Failed: Invalid ZK Purity Proof from L1 Civilization.");
        }
        let mut registry: GodChainRegistry = env.storage().instance().get(&symbol_short!("god_chain")).unwrap();
        registry.active_civilizations_count += 1;
        env.storage().instance().set(&symbol_short!("god_chain"), &registry);
        env.events().publish((symbol_short!("anchor"), civilization_id), true);
    }

    pub fn mint_sovereign_citizenship_nft(env: Env, citizen: Address, mining_year: u16) -> u64 {
        let genesis_weight: u64 = if mining_year <= 2019 { 1500 } else { 1000 };
        env.storage().persistent().set(&citizen, &genesis_weight);
        env.events().publish((symbol_short!("nft_mint"), citizen), genesis_weight);
        genesis_weight
    }
}
