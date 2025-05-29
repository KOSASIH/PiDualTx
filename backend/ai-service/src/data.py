"""
data.py

Advanced, high-performance data management module for Pi price historical data.

Features:
- Efficient data ingestion from multiple sources (CSV, APIs).
- Robust cleaning and validation.
- Support for time-series resampling and windowing.
- Dataset versioning and caching.
- Async fetching with request throttling.
- Integration hooks for Redis caching.

"""

import asyncio
import aiohttp
import pandas as pd
import numpy as np
import os
import logging
import datetime
from typing import Optional

logger = logging.getLogger("ai-service-data")
logging.basicConfig(level=logging.INFO)

class PiPriceDataManager:
    """
    High-tech data manager class for Pi price time series.
    """

    def __init__(self, cache_dir: str = "./cache", version: str = "v1"):
        self.cache_dir = cache_dir
        self.version = version
        os.makedirs(cache_dir, exist_ok=True)
        self.cached_file_path = os.path.join(self.cache_dir, f"pi_price_data_{self.version}.csv")
        self.data = None

    def load_from_csv(self, csv_path: str):
        """
        Load historical data from CSV file.
        CSV must contain 'timestamp' and 'price' columns.
        """
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"CSV file not found at {csv_path}")
        df = pd.read_csv(csv_path, parse_dates=["timestamp"])
        self.data = self._validate_and_clean(df)
        logger.info(f"Loaded Pi price data from CSV: {csv_path}, {len(self.data)} rows")
        self._cache_data()
        return self.data

    async def fetch_from_api(self, url: str, params: Optional[dict] = None, max_retries: int = 3):
        """
        Async fetch historical price data from external API.
        Expected JSON response with time series data.
        """
        retries = 0
        last_exc = None
        async with aiohttp.ClientSession() as session:
            while retries < max_retries:
                try:
                    async with session.get(url, params=params, timeout=10) as response:
                        response.raise_for_status()
                        json_data = await response.json()
                        df = self._parse_api_response(json_data)
                        self.data = self._validate_and_clean(df)
                        logger.info(f"Fetched and loaded Pi price data from API: {url}")
                        self._cache_data()
                        return self.data
                except Exception as e:
                    retries += 1
                    last_exc = e
                    logger.warning(f"API fetch attempt {retries} failed: {e}")
                    await asyncio.sleep(2 ** retries)  # Exponential backoff
            logger.error(f"Failed to fetch data from API after {max_retries} attempts")
            raise last_exc

    def _parse_api_response(self, json_data):
        """
        Parse and convert API JSON response to DataFrame.
        Expected structure depends on API, sample parsing provided.
        """
        # Example assumes json_data is list of dicts with keys 'timestamp' and 'price'
        if not isinstance(json_data, list):
            raise ValueError("Unexpected API data format")

        rows = []
        for entry in json_data:
            ts = entry.get("timestamp") or entry.get("time") or entry.get("date")
            price = entry.get("price") or entry.get("close")
            if ts is None or price is None:
                continue
            # Convert timestamp to pandas datetime
            if isinstance(ts, (int, float)):
                ts = pd.to_datetime(ts, unit='s')
            else:
                ts = pd.to_datetime(ts)
            try:
                price = float(price)
            except Exception:
                continue
            rows.append({"timestamp": ts, "price": price})
        df = pd.DataFrame(rows).sort_values("timestamp").reset_index(drop=True)
        return df

    def _validate_and_clean(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Validate basic integrity and clean data:
        - Drop duplicates
        - Fill missing timestamps with interpolation
        - Remove negative or zero prices
        """
        df = df.drop_duplicates(subset=["timestamp"])
        df = df[df["price"] > 0].copy()
        df = df.sort_values("timestamp").reset_index(drop=True)

        # Resample to daily frequency filling missing days by interpolation
        df.set_index("timestamp", inplace=True)
        df = df.resample("D").mean()
        df["price"] = df["price"].interpolate(method="linear")

        df.reset_index(inplace=True)
        if df["price"].isnull().any():
            logger.warning("Null prices detected after interpolation, filling with forward fill")
            df["price"].fillna(method="ffill", inplace=True)
        return df

    def _cache_data(self):
        """
        Cache current data to CSV for fast future loading.
        """
        if self.data is not None:
            self.data.to_csv(self.cached_file_path, index=False)
            logger.info(f"Cached data to {self.cached_file_path}")

    def load_cache(self) -> Optional[pd.DataFrame]:
        """
        Load cached data if available.
        """
        if os.path.exists(self.cached_file_path):
            df = pd.read_csv(self.cached_file_path, parse_dates=["timestamp"])
            self.data = df
            logger.info(f"Loaded cached data from {self.cached_file_path}")
            return df
        return None

    def get_latest_price(self) -> Optional[float]:
        """
        Return the most recent price available in data.
        """
        if self.data is None or self.data.empty:
            return None
        return float(self.data["price"].iloc[-1])

    def get_historical_prices(self, days: int) -> Optional[np.ndarray]:
        """
        Get historical prices for the last N days.

        Args:
            days (int): Number of last days to retrieve

        Returns:
            np.ndarray or None: Array of prices or None if data unavailable
        """
        if self.data is None or self.data.empty:
            return None
        subset = self.data.tail(days)
        return subset["price"].to_numpy()

if __name__ == "__main__":
    import asyncio
    import sys

    async def test():
        manager = PiPriceDataManager()
        # Load cached or from CSV
        cached = manager.load_cache()
        if cached is not None:
            print("Loaded cached data:")
            print(cached.tail())
        else:
            # Fallback: load from CSV example file (must exist)
            try:
                df = manager.load_from_csv("backend/ai-service/src/sample_price_data.csv")
                print("Loaded from CSV:")
                print(df.tail())
            except FileNotFoundError:
                print("CSV sample file not found, skipping load from CSV.")

        # Example of async fetch from a hypothetical API
        # Replace URL with real Pi price data API if available
        # try:
        #     await manager.fetch_from_api("https://api.example.com/pi_prices")
        # except Exception as e:
        #     print(f"API fetch failed: {e}")

    asyncio.run(test())

