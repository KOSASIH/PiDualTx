#![no_std]
use soroban_sdk::{contract, contractimpl, contracttype, symbol_short, Address, Env, Map, String, Vec, Bytes};

#[contracttype]
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct Transaction {
    pub user: Address,
    pub merchant: Address,
    pub amount: i128,
    pub payment_type: String,
    pub auto_convert: bool,
    pub timestamp: u64,
    pub quantum_signature: Bytes,
}

#[contract]
pub struct PiDualTxContract;

#[contractimpl]
impl PiDualTxContract {
    pub fn __constructor(env: Env, admin: Address) {
        admin.require_auth();
        env.storage().instance().set(&symbol_short!("admin"), &admin);
    }

    pub fn set_pi_purity(env: Env, user: Address, is_pure: bool) {
        let admin: Address = env.storage().instance().get(&symbol_short!("admin")).unwrap();
        admin.require_auth();
        env.storage().persistent().set(&user, &is_pure);
        env.events().publish((symbol_short!("purity_val"), user), is_pure);
    }

    pub fn update_pi_balance(env: Env, user: Address, amount: i128) {
        let admin: Address = env.storage().instance().get(&symbol_short!("admin")).unwrap();
        admin.require_auth();
        let balance: i128 = env.storage().persistent().get(&user).unwrap_or(0);
        let new_balance = balance + amount;
        env.storage().persistent().set(&user, &new_balance);
        env.events().publish((symbol_short!("bal_upd"), user), new_balance);
    }

    pub fn validate_pi_purity(env: Env, user: Address) -> bool {
        env.storage().persistent().get(&user).unwrap_or(false)
    }

    pub fn submit_transaction(
        env: Env,
        user: Address,
        merchant: Address,
        amount: i128,
        payment_type: String,
        auto_convert: bool,
        quantum_signature: Bytes,
    ) {
        user.require_auth();
        if amount <= 0 {
            panic!("Amount must be greater than 0");
        }
        
        let balance: i128 = env.storage().persistent().get(&user).unwrap_or(0);
        if balance < amount {
            panic!("Insufficient Pi balance");
        }

        // Purity check enforcement: Only PURE_MINED Pi gets GCV $314,159
        let is_pure: bool = env.storage().persistent().get(&user).unwrap_or(false);
        if payment_type == String::from_str(&env, "internal") && !is_pure {
            panic!("Impure Pi cannot participate in GCV $314,159 internal consensus valuation");
        }

        env.storage().persistent().set(&user, &(balance - amount));

        if merchant != Address::from_string(&String::from_str(&env, "G0000000000000000000000000000000000000000000000000000000")) {
            let merchant_balance: i128 = env.storage().persistent().get(&merchant).unwrap_or(0);
            env.storage().persistent().set(&merchant, &(merchant_balance + amount));
        }

        let mut txs: Vec<Transaction> = env.storage().instance().get(&symbol_short!("txs")).unwrap_or(Vec::new(&env));
        let tx = Transaction {
            user: user.clone(),
            merchant,
            amount,
            payment_type: payment_type.clone(),
            auto_convert,
            timestamp: env.ledger().timestamp(),
            quantum_signature,
        };
        txs.push_back(tx);
        env.storage().instance().set(&symbol_short!("txs"), &txs);

        env.events().publish((symbol_short!("tx_rec"), user), (amount, payment_type));
    }

    pub fn get_pi_balance(env: Env, user: Address) -> i128 {
        env.storage().persistent().get(&user).unwrap_or(0)
    }

    pub fn get_total_balance(env: Env) -> i128 {
        let txs: Vec<Transaction> = env.storage().instance().get(&symbol_short!("txs")).unwrap_or(Vec::new(&env));
        let mut total: i128 = 0;
        for i in 0..txs.len() {
            let tx = txs.get(i).unwrap();
            total += tx.amount;
        }
        total
    }

    pub fn get_transaction_count(env: Env) -> u32 {
        let txs: Vec<Transaction> = env.storage().instance().get(&symbol_short!("txs")).unwrap_or(Vec::new(&env));
        txs.len()
    }
}
