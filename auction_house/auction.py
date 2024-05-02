import random
import time
import logging
from database.database import execute_query


rate_mapping = {
    "Dead Slow": 2,
    "Very Slow": 2,
    "Slow": 3,
    "Average": 5,
    "Fast": 8,
    "Very Fast": 8,
}


def get_name():
    names = [
        "Aelar",
        "Brondar",
        "Caelum",
        "Draka",
        "Eilora",
        "Fenris",
        "Gorim",
        "Helia",
        "Ithra",
        "Jorund",
        "Kyra",
        "Lorin",
        "Mirelle",
        "Narlok",
        "Ophira",
        "Pyralis",
        "Quinlan",
        "Rael",
        "Sylvana",
        "Torin",
        "Ulyra",
        "Vaelis",
        "Wyran",
        "Xyrella",
        "Yorith",
        "Zephyra",
    ]
    return random.choice(names)


def buy_random_items():
    print("Buying random items...")
    current_time = int(time.time())
    all_items = execute_query(
        "SELECT id, price FROM auction_house WHERE sell_date = 0", fetch=True
    )
    if not all_items:
        print("No items available for purchase.")
        return

    num_items_to_buy = max(len(all_items) // 5, 1)
    items_to_buy = random.sample(all_items, k=num_items_to_buy)
    for item in items_to_buy:
        execute_query(
            "UPDATE auction_house SET buyer_name = %s, sale = %s, sell_date = %s WHERE id = %s AND sell_date = 0",
            (get_name(), item[1], current_time, item[0]),
            commit=True,
        )
    print(f"Randomly purchased items: {len(items_to_buy)}")
    print("\n")


def buy_all_items():
    print("Buying all items...")
    current_time = int(time.time())
    items_for_sale = execute_query(
        "SELECT id, price FROM auction_house WHERE sell_date = 0", fetch=True
    )
    for item in items_for_sale:
        execute_query(
            "UPDATE auction_house SET buyer_name = %s, sale = %s, sell_date = %s WHERE id = %s AND sell_date = 0",
            (get_name(), item[1], current_time, item[0]),
            commit=True,
        )
    print(f"Purchased all items: {len(items_for_sale)}")
    print("\n")


def update_auction_house():
    logging.basicConfig(level=logging.DEBUG)
    print("Updating auction house...")

    try:
        # Fetch items directly from the ah_data database, skipping the name
        items_query = "SELECT itemid, stack, single, rate FROM items"
        # logging.debug("Executing query on ah_data: %s", items_query)
        items = execute_query(items_query, fetch=True, database="ah_data")

        # Insert/update records in the xidb database
        # logging.debug("Inserting into xidb.auction_house")
        for item in items:
            item_id, stack_price, single_price, rate = item  # Corrected tuple unpacking
            required_quantity = rate_mapping.get(rate, 3)
            process_prices(
                item_id, single_price, stack_price, required_quantity, database="xidb"
            )

        print("Auction house updated successfully.")
        print("\n")
    except Exception as e:
        logging.error("Failed to update auction house: %s", e)


import time


def process_prices(item_id, single_price, stack_price, required_quantity, database):
    current_time = int(time.time())  # UNIX_TIMESTAMP() equivalent in Python

    # Process single price items
    if single_price is not None:
        current_single_qty = check_existing_quantity(item_id, 0, database)
        if current_single_qty < required_quantity:
            qty_to_add = required_quantity - current_single_qty
            for _ in range(qty_to_add):
                random_seller = get_name()
                try:
                    execute_query(
                        """
                        INSERT INTO auction_house
                        (itemid, stack, seller, seller_name, date, price, buyer_name, sale, sell_date)
                        VALUES (%s, 0, 0, %s, %s, %s, NULL, 0, 0)
                        """,
                        (item_id, random_seller, current_time, single_price),
                        commit=True,
                        database=database,
                    )
                except Exception as e:
                    logging.error(
                        "Failed to insert record for single price item: %s", e
                    )

    # Process stack price items
    if stack_price is not None:
        current_stack_qty = check_existing_quantity(item_id, 1, database)
        if current_stack_qty < required_quantity:
            qty_to_add = required_quantity - current_stack_qty
            for _ in range(qty_to_add):
                random_seller = get_name()
                try:
                    execute_query(
                        """
                        INSERT INTO auction_house
                        (itemid, stack, seller, seller_name, date, price, buyer_name, sale, sell_date)
                        VALUES (%s, 1, 0, %s, %s, %s, NULL, 0, 0)
                        """,
                        (item_id, random_seller, current_time, stack_price),
                        commit=True,
                        database=database,
                    )
                except Exception as e:
                    logging.error("Failed to insert record for stack price item: %s", e)


def check_existing_quantity(item_id, stack, database):
    result = execute_query(
        "SELECT COUNT(*) FROM auction_house WHERE itemid = %s AND stack = %s AND sell_date = 0",
        (item_id, stack),
        fetch=True,
        database=database,
    )
    return result[0][0] if result else 0

