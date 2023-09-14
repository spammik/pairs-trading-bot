from decouple import config
from binance.client import Client
from constants import BINANCE_API, BINANCE_APIS, QUOTE_ASSET


def connect_binance():
    client = Client(BINANCE_API, BINANCE_APIS)

    # Getting your futures account info
    account_info = client.futures_account()

    # Extract balance for the desired quote asset
    quote_balance = next(
        (asset for asset in account_info["assets"] if asset["asset"] == QUOTE_ASSET),
        None,
    )
    print("Connection successful.")
    print("Quote Balance:", quote_balance["availableBalance"])

    # Return client
    return client
