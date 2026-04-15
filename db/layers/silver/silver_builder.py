from db.init.schema import execute_script


def load_silver_asset_snapshot(conn):
    sql = """
        INSERT INTO silver.asset_snapshot(timestamp, symbol, price, quantity, amount)
        SELECT timestamp, symbol, price, quantity, amount 
        FROM clean.assets;
    """
    execute_script(conn, sql)

def build_portfolio_totals(conn):
    sql = """
        TRUNCATE TABLE silver.portfolio_totals;

        INSERT INTO silver.portfolio_totals(timestamp, amount)
        SELECT timestamp, SUM(amount) as amount
        FROM silver.asset_snapshot
        GROUP BY timestamp;
    """
    execute_script(conn, sql)

def truncate_silver(conn):
    execute_script(conn, 'TRUNCATE TABLE silver.asset_snapshot')

def rebuild_silver(conn):
    truncate_silver(conn)          
    load_silver_asset_snapshot(conn)  
    build_portfolio_totals(conn)  


        