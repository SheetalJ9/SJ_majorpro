import pandas as pd
import sqlite3
import config
import os


def load_data(data_path=config.SQL_LITE_FILE_NAME):
    # Convert Path object to string for sqlite3.connect()
    data_path_str = str(data_path)

    print(f"Attempting to connect to database at: {data_path_str}")
    print(f"Database file exists: {os.path.exists(data_path_str)}")

    try:
        conn = sqlite3.connect(data_path_str)
        print("Successfully connected to database!")

        query = """
        SELECT 
            d_year + 20 AS d_year,
            d_moy,
            ca_state,
            i_class,
            i_category,
            SUM(ws_quantity) AS ws_quantity,
            SUM(wr_return_quantity) AS wr_return_quantity,
            SUM(wr_net_loss) AS wr_net_loss
        FROM web_sales ws 
        JOIN item i ON ws.ws_item_sk = i.i_item_sk 
        JOIN date_dim dd ON dd.d_date_sk = ws.ws_sold_date_sk 
        JOIN web_returns wr ON wr.wr_order_number = ws.ws_order_number 
        JOIN customer_address ca ON wr.wr_returning_addr_sk = ca.ca_address_sk 
        WHERE d_year IS NOT NULL AND d_moy IS NOT NULL 
          AND i_class != 'None' AND i_category != 'None'
          -- TODO remove below filters
          AND ca_state = 'CA'
        GROUP BY d_year, d_moy, ca_state, i_class, i_category
        HAVING SUM(wr_net_loss) > AVG(wr_net_loss)
        """

        print("Executing query...")
        data_raw = pd.read_sql(query, conn)
        conn.close()
        print(f"Query successful! Retrieved {len(data_raw)} rows.")
        return data_raw

    except sqlite3.OperationalError as e:
        print(f"SQLite error: {e}")
        raise
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise


if __name__ == "__main__":
    data = load_data()
    print(f"\nDataset shape: {data.shape}")
    print("\nFirst few rows:")
    print(data.head())
    print("\nColumn info:")
    print(data.info())