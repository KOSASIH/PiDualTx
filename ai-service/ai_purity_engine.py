# ai_purity_engine.py
    from fastapi import FastAPI
    app = FastAPI(title="PiDualTx Purity Scanner", version="2026.1.0")
    
    @app.get("/api/v1/purity/check/{address}")
    def check_purity(address: str):
        is_impure = "binance" in address.lower() or address.startswith("cex_")
        return {"address": address, "provenance": "IMPURE_EXCHANGE" if is_impure else "PURE_MINED", "gcv_eligible": not is_impure}
    