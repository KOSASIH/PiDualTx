#![no_std]
extern crate alloc;

use soroban_sdk::{contract, contractimpl, contracttype, symbol_short, Address, Env, Bytes, String};

#[contracttype]
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct TemporalVaultRecord {
    pub owner: Address,
    pub locked_amount: i128,
    pub release_block: u64,
    pub mining_year: u16,
    pub temporal_gcv_valuation: u64, // scaled by 1000 (e.g. 471238 = $471.238k GCV for 2019 Pi)
}

#[contract]
pub struct TemporalVaultContract;

#[contractimpl]
impl TemporalVaultContract {
    pub fn deposit_temporal_vault(env: Env, owner: Address, amount: i128, mining_year: u16, lock_duration_blocks: u64) {
        owner.require_auth();
        let is_pure: bool = env.storage().persistent().get(&owner).unwrap_or(false);
        if !is_pure {
            panic!("Temporal Vault Rejection: Only PURE Pi can enter the Time-Travel Economy.");
        }

        let valuation = if mining_year <= 2019 { 471238 } else { 314159 };
        let record = TemporalVaultRecord {
            owner: owner.clone(),
            locked_amount: amount,
            release_block: env.ledger().sequence() + lock_duration_blocks,
            mining_year,
            temporal_gcv_valuation: valuation,
        };

        env.storage().persistent().set(&owner, &record);
        env.events().publish((symbol_short!("time_lock"), owner), (amount, valuation));
    }
}
