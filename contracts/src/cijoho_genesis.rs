#![no_std]
extern crate alloc;

use soroban_sdk::{contract, contractimpl, contracttype, symbol_short, Address, Env, Bytes, String};

#[contracttype]
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct CijohoGenesisRecord {
    pub latitude: String,   // "-6.979"
    pub longitude: String,  // "108.484"
    pub capital: String,    // "Cijoho, Kuningan, West Java"
    pub memo: String,       // "Ti Cijoho, Kuningan pikeun Dunia - PURE Pi $314,159 - KOSASIH"
    pub genesis_block: u64, // 314159
}

#[contract]
pub struct CijohoGenesisContract;

#[contractimpl]
impl CijohoGenesisContract {
    pub fn __constructor(env: Env) {
        let genesis = CijohoGenesisRecord {
            latitude: String::from_str(&env, "-6.979"),
            longitude: String::from_str(&env, "108.484"),
            capital: String::from_str(&env, "Cijoho, Kuningan, West Java"),
            memo: String::from_str(&env, "Ti Cijoho, Kuningan pikeun Dunia - From Cijoho for the World - PURE Pi $314,159 - KOSASIH"),
            genesis_block: 314159,
        };
        env.storage().instance().set(&symbol_short!("cijoho"), &genesis);
    }

    pub fn verify_cijoho_geo_and_culture(env: Env, pioneer: Address, cultural_oath: String) -> bool {
        pioneer.require_auth();
        // Sunda Wiwitan Philosophy: Tri Tangtu verification oath
        if cultural_oath.len() == 0 {
            panic!("Cijoho Genesis Rejection: Must take cultural oath of Silih Asah, Asih, Asuh rooted in Cijoho.");
        }
        let is_pure: bool = env.storage().persistent().get(&pioneer).unwrap_or(false);
        env.events().publish((symbol_short!("cijoho_ok"), pioneer), true);
        is_pure
    }
}
