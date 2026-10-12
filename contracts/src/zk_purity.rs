#![no_std]
extern crate alloc;

use soroban_sdk::{contract, contractimpl, contracttype, symbol_short, Address, Env, Bytes};

#[contracttype]
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct ZkPurityProofData {
    pub pioneer_kyc_hash: Bytes,
    pub mining_lineage_proof: Bytes,
    pub gcv_consensus_score: u32, // scaled by 1000 (e.g. 930 = 0.93)
}

#[contract]
pub struct ZkPurityContract;

#[contractimpl]
impl ZkPurityContract {
    pub fn verify_zk_purity_and_poch(env: Env, user: Address, proof: ZkPurityProofData) -> bool {
        user.require_auth();
        if proof.gcv_consensus_score < 930 {
            panic!("Proof-of-Humanity Consensus (PoCH) Failed: GCV Consensus Score < 0.93");
        }
        
        let is_pure: bool = env.storage().persistent().get(&user).unwrap_or(false);
        if !is_pure {
            panic!("ZK Purity Lineage Check Failed: Wallet touched CEX hot wallet or lacks mining lineage");
        }

        env.storage().persistent().set(&symbol_short!("poch_wt"), &proof.gcv_consensus_score);
        env.events().publish((symbol_short!("poch_ok"), user), true);
        true
    }
}
