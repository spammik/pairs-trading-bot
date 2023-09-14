from func_connections import connect_binance
from constants import ABORT_ALL_POSITIONS
from func_private import abort_all_positions

if __name__ == "__main__":
    # Connect to client
    try:
        print("Connecting co client...")
        client = connect_binance()
    except Exception as e:
        print("Error connecting to client: ", e)
        exit(1)

    # Abort all open positions
    if ABORT_ALL_POSITIONS:
        try:
            print("Closing all positions...")
            close_orders = abort_all_positions(client)
        except Exception as e:
            print("Error closing all positions: ", e)
            exit(1)
