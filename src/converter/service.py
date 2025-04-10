### Converter currency
import asyncio
import datetime
import os.path as op
import httpx
import os

from typing import Literal
from dotenv import load_dotenv
load_dotenv()


class Converter:
    def __init__(self):
        self.API_KEY = os.getenv("FOREX_API")
        self.currency = {
            "$": "USD",
            "€": "EUR",
            "¥": "JPY",
            "£": "GBP",
            "₽": "RUB"
        }

    async def convert(self, from_currency: str, to_currency: str = "RUB", amount: int = 0):
        """Convert logic"""
        
        async with httpx.AsyncClient() as client:
            response = await client.get(f"https://v6.exchangerate-api.com/v6/{self.API_KEY}/pair/{from_currency}/{to_currency}/{amount}")
            data = response.json()
            
            if data["result"] == "success":
                conversion_result = data["conversion_result"]
                return conversion_result
            
    async def convert_sum(self, sum: int, currency: Literal["$", "¥"] = "rmb") -> dict:
        """Конвертация и возврат конвертированой суммы"""
            
        result = await self.convert(from_currency=self.currency.get(currency), to_currency="RUB", amount=sum)
        
        return result