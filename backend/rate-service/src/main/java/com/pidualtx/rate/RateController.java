package com.pidualtx.rate;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.http.ResponseEntity;

import java.math.BigDecimal;
import java.time.Instant;
import java.util.HashMap;
import java.util.Map;
import java.util.Random;

/**
 * RateController
 * REST API Controller providing Pi price rates.
 * Features:
 * - Returns internal community rate and external exchange rate.
 * - Simulates real-time updates with randomized fluctuations.
 * - Provides timestamped rate data for client consumption.
 */
@RestController
public class RateController {

    // Internal community rate fixed at $314,159/Pi
    private static final BigDecimal INTERNAL_RATE = new BigDecimal("314159");

    // External rate base value ~ $0.8111/Pi (could be updated from external APIs)
    private BigDecimal externalRate = new BigDecimal("0.8111");

    private final Random random = new Random();

    /**
     * GET /api/rates
     * Returns current rates including internal and external with timestamp.
     * Example JSON response:
     * {
     *   "internalRate": "314159",
     *   "externalRate": "0.8053",
     *   "timestamp": 1699999999
     * }
     */
    @GetMapping("/api/rates")
    public ResponseEntity<Map<String, Object>> getRates() {
        // Simulate external rate fluctuation +/- up to 0.01 around current value
        BigDecimal fluctuation = BigDecimal.valueOf(random.nextDouble() * 0.02 - 0.01);
        externalRate = externalRate.add(fluctuation);
        // Bound externalRate to reasonable positive range
        if (externalRate.compareTo(BigDecimal.ZERO) <= 0) {
            externalRate = new BigDecimal("0.8");
        }

        Map<String, Object> rates = new HashMap<>();
        rates.put("internalRate", INTERNAL_RATE.setScale(2, BigDecimal.ROUND_HALF_UP).toPlainString());
        rates.put("externalRate", externalRate.setScale(4, BigDecimal.ROUND_HALF_UP).toPlainString());
        rates.put("timestamp", Instant.now().getEpochSecond());

        return ResponseEntity.ok(rates);
    }
}

