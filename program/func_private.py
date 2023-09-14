from binance.enums import SIDE_BUY, SIDE_SELL, ORDER_TYPE_MARKET


# Place market order for Binance Futures
def place_market_order(client, market, side, size, price=None, reduce_only=False):
    """
    Place a market order on Binance Futures.

    Parameters:
    - client: Binance client
    - market: e.g. 'BTCUSDT'
    - side: 'BUY' or 'SELL'
    - size: Quantity of the asset
    - price: Optional for market orders
    - reduce_only: Flag to ensure the order only reduces a position

    Returns:
    - Order response from Binance
    """
    if side not in ["BUY", "SELL"]:
        raise ValueError("Side should be 'BUY' or 'SELL'")

    side_enum = SIDE_BUY if side == "BUY" else SIDE_SELL

    order = client.futures_create_order(
        symbol=market,
        side=side_enum,
        type=ORDER_TYPE_MARKET,
        quantity=size,
        reduceOnly=reduce_only,
    )
    return order


# Abort all open positions for Binance Futures
def abort_all_positions(client):
    """
    Close all open futures positions on Binance.

    Parameters:
    - client: Binance client

    Returns:
    - List of responses from Binance for each position closed
    """
    # Get the open positions
    positions = client.futures_position_information()

    # List to store the responses
    responses = []

    for position in positions:
        symbol = position["symbol"]
        positionAmt = float(position["positionAmt"])

        # If the position amount is positive, it's a LONG position and needs to be sold
        if positionAmt > 0:
            order_response = client.futures_create_order(
                symbol=symbol,
                side=SIDE_SELL,
                type=ORDER_TYPE_MARKET,
                quantity=positionAmt,
            )
            responses.append(order_response)

        # If the position amount is negative, it's a SHORT position and needs to be bought to be closed
        elif positionAmt < 0:
            order_response = client.futures_create_order(
                symbol=symbol,
                side=SIDE_BUY,
                type=ORDER_TYPE_MARKET,
                quantity=-positionAmt,  # Convert the negative amount to positive for order
            )
            responses.append(order_response)

    return responses
