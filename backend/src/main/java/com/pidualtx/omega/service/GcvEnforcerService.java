package com.pidualtx.omega.service;
    
    import java.math.BigDecimal;
    
    public class GcvEnforcerService {
        public static final BigDecimal GCV_CANONICAL = new BigDecimal("314159.0000000");
        public static final long GCV_CANONICAL_STROOPS = 3141590000000L;
    
        public boolean validateInternalSettlement(String settlementType, BigDecimal amount) {
            if (!"internal".equalsIgnoreCase(settlementType)) {
                throw new IllegalArgumentException("Settlement type must be internal.");
            }
            return true;
        }
    }
    