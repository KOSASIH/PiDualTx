#![no_std]
extern crate alloc;

use soroban_sdk::{contract, contractimpl, contracttype, symbol_short, Address, Env, Bytes};

#[contracttype]
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct HeirRecord {
    pub pioneer: Address,
    pub designated_heir: Address,
    pub zk_family_dna_hash: Bytes,
}

#[contract]
pub struct ImmortalityContract;

#[contractimpl]
impl ImmortalityContract {
    pub fn register_inheritance(env: Env, pioneer: Address, designated_heir: Address, zk_family_dna_hash: Bytes) {
        pioneer.require_auth();
        let record = HeirRecord {
            pioneer: pioneer.clone(),
            designated_heir,
            zk_family_dna_hash,
        };
        env.storage().persistent().set(&pioneer, &record);
        env.events().publish((symbol_short!("immortal"), pioneer), true);
    }

    pub fn execute_afterlife_transfer(env: Env, pioneer: Address, heir_proof: Bytes) {
        let record: HeirRecord = env.storage().persistent().get(&pioneer).unwrap();
        if heir_proof != record.zk_family_dna_hash {
            panic!("Afterlife Transfer Denied: ZK Family DNA Hash / Social Recovery proof invalid.");
        }
        let balance: i128 = env.storage().persistent().get(&pioneer).unwrap_or(0);
        env.storage().persistent().set(&record.designated_heir, &balance);
        env.storage().persistent().remove(&pioneer);
        env.events().publish((symbol_short!("afterlife"), pioneer), record.designated_heir);
    }
}
