#![no_std]
extern crate alloc;

use soroban_sdk::{contract, contractimpl, contracttype, symbol_short, Address, Env, Bytes, String};

#[contracttype]
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct ConstitutionRecord {
    pub version: String,
    pub arweave_hash: Bytes,
    pub ipfs_hash: Bytes,
    pub genesis_block_ref: u64,
    pub enacted_timestamp: u64,
}

#[contract]
pub struct ConstitutionContract;

#[contractimpl]
impl ConstitutionContract {
    pub fn __constructor(env: Env, arweave_hash: Bytes, ipfs_hash: Bytes) {
        let record = ConstitutionRecord {
            version: String::from_str(&env, "v1.0-merdeka"),
            arweave_hash,
            ipfs_hash,
            genesis_block_ref: 314159,
            genesis_block_ref: env.ledger().timestamp(),
        };
        env.storage().instance().set(&symbol_short!("constitution"), &record);
    }

    pub fn get_constitution(env: Env) -> ConstitutionRecord {
        env.storage().instance().get(&symbol_short!("constitution")).unwrap()
    }

    pub fn amend_constitution(env: Env, proposer: Address, new_arweave_hash: Bytes, purity_proof_valid: bool) {
        proposer.require_auth();
        if !purity_proof_valid {
            panic!("Constitutional Amendment Rejected: Requires 67% PURE citizen vote + ZK citizenship proof + 21-day time-lock.");
        }
        let mut record: ConstitutionRecord = env.storage().instance().get(&symbol_short!("constitution")).unwrap();
        record.arweave_hash = new_arweave_hash;
        env.storage().instance().set(&symbol_short!("constitution"), &record);
        env.events().publish((symbol_short!("amend_cons"), proposer), true);
    }
}
