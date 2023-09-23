import json
import os
from datetime import datetime
from typing import List, Dict, Union

import requests


class DataParser:
    api_url: str = "https://api.bscscan.com/api"
    params: Dict[str, Union[int, str]] = {
        "module": "account",
        "action": "txlist",
        "startblock": 0,
        "endblock": 99999999,
        "sort": "desc",
        "apikey": os.environ.get("APIKEY")
    }

    def __init__(self, address: str):
        self.address: str = address
        self.transactions: List[Dict] = []
        self.parsed_data: List[Dict] = []
        self.error_message: str = ''

    def get_transactions(self) -> None:
        params: Dict[str, Union[int, str]] = {**self.params, "address": self.address}
        response = requests.get(self.api_url, params=params)
        if response.status_code != 200:
            self.error_message = "Error: Could not fetch data, please press /start again"
            return
        transactions: List[Dict] = json.loads(response.text).get("result", [])
        if not transactions:
            self.error_message = "Error: Could not fetch data, please press /start again"
            return
        for transaction in transactions:
            if transaction.get("to").lower() == self.address.lower():
                self.transactions.append(transaction)

    def data_parser(self) -> None:
        for block in self.transactions:
            status: str = "Success" if block.get("txreceipt_status") == "1" else "Fail"

            value_in_wei: int = int(block.get("value"))
            value_in_bnb: float = value_in_wei / 1e18
            formatted_value: str = "{:.9f}".format(value_in_bnb)

            time_stamp_int: int = int(block.get("timeStamp"))
            date_and_time: str = datetime.fromtimestamp(time_stamp_int).strftime('%Y-%m-%d %H:%M:%S')

            parsed_block: Dict[str, Union[str, int]] = {
                "transaction type": "transfer",
                "date and time": date_and_time,
                "value": formatted_value,
                "status": status,
                "error": block.get("isError")
            }
            self.parsed_data.append(parsed_block)

    def get_info(self):
        self.get_transactions()
        if self.error_message:
            return self.error_message
        elif not self.transactions:
            return "No incoming transactions"
        self.data_parser()
        return self.parsed_data

