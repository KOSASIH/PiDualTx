package com.pidualtx.rate;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.stereotype.Component;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.core.publisher.Mono;

import java.math.BigDecimal;
import java.time.Duration;
import java.util.Map;

/**
 * ExchangeClient
 * Integrates with external cryptocurrency exchanges (e.g., OKX, Bitget)
 * to fetch real-time Pi exchange prices.
 * Features:
 * - Non-blocking reactive HTTP client.
 * - Handles multiple exchanges configurable via URL.
 * - Parses JSON responses safely.
 * - Implements retry and timeout policies.
 */
@Component
public class ExchangeClient {

    private final WebClient webClient;
    private final ObjectMapper objectMapper;

    // URLs of external exchanges APIs for Pi prices (Example endpoints)
    private static final Map<String, String> EXCHANGE_URLS = Map.of(
            "okx", "https://www.okx.com/api/v5/market/ticker?instId=PI-USDT",
            "bitget", "https://api.bitget.com/api/spot/v1/ticker?symbol=piusdt"
    );

    public ExchangeClient() {
        this.webClient = WebClient.builder()
                .baseUrl("") // Base URL overridden per request
                .build();
        this.objectMapper = new ObjectMapper();
    }

    /**
     * Fetch Pi price from OKX Exchange
     * @return BigDecimal Pi price or null if unavailable
     */
    public Mono<BigDecimal> fetchOkxPrice() {
        String url = EXCHANGE_URLS.get("okx");
        return webClient.get()
                .uri(url)
                .retrieve()
                .bodyToMono(String.class)
                .timeout(Duration.ofSeconds(5))
                .flatMap(this::extractOkxPrice)
                .retry(2)
                .onErrorReturn(null);
    }

    /**
     * Fetch Pi price from Bitget Exchange
     * @return BigDecimal Pi price or null if unavailable
     */
    public Mono<BigDecimal> fetchBitgetPrice() {
        String url = EXCHANGE_URLS.get("bitget");
        return webClient.get()
                .uri(url)
                .retrieve()
                .bodyToMono(String.class)
                .timeout(Duration.ofSeconds(5))
                .flatMap(this::extractBitgetPrice)
                .retry(2)
                .onErrorReturn(null);
    }

    /**
     * Extract Pi price from OKX response JSON string
     * @param jsonResponse JSON response string
     * @return Mono<BigDecimal> price
     */
    private Mono<BigDecimal> extractOkxPrice(String jsonResponse) {
        try {
            JsonNode root = objectMapper.readTree(jsonResponse);
            JsonNode dataArray = root.path("data");
            if (dataArray.isArray() && dataArray.size() > 0) {
                String last = dataArray.get(0).path("last").asText();
                return Mono.just(new BigDecimal(last));
            }
        } catch (Exception e) {
            // Log error if needed
        }
        return Mono.justOrEmpty(null);
    }

    /**
     * Extract Pi price from Bitget response JSON string
     * @param jsonResponse JSON response string
     * @return Mono<BigDecimal> price
     */
    private Mono<BigDecimal> extractBitgetPrice(String jsonResponse) {
        try {
            JsonNode root = objectMapper.readTree(jsonResponse);
            String last = root.path("data").path("last").asText();
            if (!last.isEmpty()) {
                return Mono.just(new BigDecimal(last));
            }
        } catch (Exception e) {
            // Log error if needed
        }
        return Mono.justOrEmpty(null);
    }
}
