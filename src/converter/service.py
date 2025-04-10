### Converter currency

from typing import Literal


class Converter:
    def __init__(self):
        pass

    def convert(self, sum: int, currency: Literal["usd", "rmb"] = "rmb") -> dict:
        """Convert logic"""
        
        if currency == "usd":
            data = {
                "sum": sum * 0.013,
                "currency": "usd"
            }
        elif currency == "rmb":
            data = {
                "sum": sum * 0.094,
                "currency": "rmb"
            }
        else:
            raise ValueError("Invalid currency type")
        
        return data