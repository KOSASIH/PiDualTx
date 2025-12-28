// =====================================================
// PI NETWORK – NSC GCV GUARD
// Anti Price Claim & Anti Scam Narrative Smart Contract
// =====================================================
//
// ⚠️ This contract DOES NOT define price.
// ⚠️ This contract DOES NOT enable trading.
// ⚠️ This contract PROTECTS narrative integrity.
//
// Compatible with: Pi-style WASM / NSC architecture
// =====================================================

/// ------------------------------
/// NETWORK EPOCH
/// ------------------------------
#[derive(Clone, PartialEq)]
enum NetworkEpoch {
    ENCLOSED,     // Enclosed Mainnet
    TRANSITION,   // Transition Phase
    OPEN          // Open Mainnet
}

/// ------------------------------
/// CLAIM TYPE
/// ------------------------------
#[derive(Clone, PartialEq)]
enum ClaimType {
    PRICE_CLAIM,        // Klaim harga / nilai pasti
    VALUE_REFERENCE,    // Referensi nilai non-market
    EDUCATIONAL,        // Edukasi / diskusi
    UNKNOWN
}

/// ------------------------------
/// NETWORK STATE
/// ------------------------------
struct NetworkState {
    epoch: NetworkEpoch,
    allow_market_price: bool,
}

/// ------------------------------
/// AUDIT LOG
/// ------------------------------
struct GuardLog {
    timestamp: u64,
    actor: String,
    claim_type: ClaimType,
    decision: String,
}

/// ------------------------------
/// CORE CONTRACT
/// ------------------------------
struct GCVGuard {
    state: NetworkState,
    logs: Vec<GuardLog>,
}

impl GCVGuard {

    /// INIT CONTRACT
    fn init() -> Self {
        GCVGuard {
            state: NetworkState {
                epoch: NetworkEpoch::ENCLOSED,
                allow_market_price: false,
            },
            logs: Vec::new(),
        }
    }

    /// --------------------------
    /// CLAIM DETECTION ENGINE
    /// --------------------------
    fn detect_claim(&self, text: &String) -> ClaimType {

        let lower = text.to_lowercase();

        if lower.contains("harga resmi")
            || lower.contains("official price")
            || lower.contains("gcv =")
            || lower.contains("jamin harga")
            || lower.contains("guaranteed value")
        {
            return ClaimType::PRICE_CLAIM;
        }

        if lower.contains("konsensus")
            || lower.contains("referensi nilai")
            || lower.contains("nilai internal")
        {
            return ClaimType::VALUE_REFERENCE;
        }

        if lower.contains("edukasi")
            || lower.contains("diskusi")
            || lower.contains("pembahasan")
        {
            return ClaimType::EDUCATIONAL;
        }

        ClaimType::UNKNOWN
    }

    /// --------------------------
    /// GCV USAGE POLICY
    /// --------------------------
    fn gcv_usage_guard(&self, use_case: &String) -> Result<(), String> {

        let lower = use_case.to_lowercase();

        if lower.contains("jual")
            || lower.contains("beli")
            || lower.contains("exchange")
            || lower.contains("withdraw")
            || lower.contains("transfer nilai")
        {
            return Err(
                "GCV_VIOLATION: GCV cannot be used for financial transactions."
                    .to_string()
            );
        }

        Ok(())
    }

    /// --------------------------
    /// ENFORCEMENT ENGINE
    /// --------------------------
    fn enforce(
        &mut self,
        actor: String,
        content: String,
        use_case: String,
        timestamp: u64,
    ) -> Result<String, String> {

        let claim = self.detect_claim(&content);

        // GCV misuse guard
        if let Err(e) = self.gcv_usage_guard(&use_case) {
            self.log(actor, claim.clone(), "BLOCKED".to_string(), timestamp);
            return Err(e);
        }

        match self.state.epoch {

            NetworkEpoch::ENCLOSED => {
                if claim == ClaimType::PRICE_CLAIM {
                    self.log(actor, claim, "BLOCKED".to_string(), timestamp);
                    return Err(
                        "BLOCKED: No price claims allowed in Enclosed Mainnet."
                            .to_string()
                    );
                }
            }

            NetworkEpoch::TRANSITION => {
                if claim == ClaimType::PRICE_CLAIM {
                    self.log(actor, claim, "REJECTED".to_string(), timestamp);
                    return Err(
                        "REJECTED: No official Pi price during transition phase."
                            .to_string()
                    );
                }
            }

            NetworkEpoch::OPEN => {
                if !self.state.allow_market_price
                    && claim == ClaimType::PRICE_CLAIM
                {
                    self.log(actor, claim, "DENIED".to_string(), timestamp);
                    return Err(
                        "DENIED: Market price not enabled by governance."
                            .to_string()
                    );
                }
            }
        }

        self.log(actor, claim, "ALLOWED".to_string(), timestamp);
        Ok(self.notice())
    }

    /// --------------------------
    /// LOGGING
    /// --------------------------
    fn log(
        &mut self,
        actor: String,
        claim: ClaimType,
        decision: String,
        timestamp: u64,
    ) {
        self.logs.push(
            GuardLog {
                timestamp,
                actor,
                claim_type: claim,
                decision,
            }
        );
    }

    /// --------------------------
    /// USER NOTICE
    /// --------------------------
    fn notice(&self) -> String {
        "NOTICE:
Pi Network has no official price.
GCV is a community discussion concept only.
Never share private keys.
Beware of scams and misinformation."
            .to_string()
    }

    /// --------------------------
    /// GOVERNANCE HOOK
    /// --------------------------
    fn set_epoch(&mut self, epoch: NetworkEpoch) {
        self.state.epoch = epoch;
    }

    fn enable_market_price(&mut self, status: bool) {
        self.state.allow_market_price = status;
    }
}
