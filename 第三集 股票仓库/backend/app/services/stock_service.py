from typing import NotImplemented


class StockService:
    """Service for fetching stock data from various markets."""

    @staticmethod
    def get_quote(symbol: str, market: str) -> dict:
        """Fetch a stock quote for the given symbol and market."""
        raise NotImplementedError("Stock data fetching not yet implemented")

    @staticmethod
    def get_batch_quotes(symbols: list[str], market: str) -> list[dict]:
        """Fetch multiple stock quotes."""
        raise NotImplementedError("Stock data fetching not yet implemented")