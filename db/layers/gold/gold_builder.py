from db.init.schema import execute_script

def build_portfolio_daily(conn):
    sql = """
        INSERT INTO gold.portfolio_daily(date,last_ts, amount)
        WITH daily_last AS(
            SELECT
            date_trunc('day', timestamp)::date as date,
            timestamp as last_ts,
            amount,
            ROW_NUMBER() OVER(
            PARTITION BY date_trunc('day', timestamp)::date
            ORDER BY timestamp DESC) as rn
            FROM silver.portfolio_totals 
        )
        SELECT date, last_ts, amount
        FROM daily_last 
        WHERE rn = 1
    """ 
    execute_script(conn, sql)

def build_asset_daily(conn):
    sql = """
        insert into gold.asset_daily (date, symbol, quantity_end, amount_end)
        with asset_last_ts as(
            select 
                date_trunc('day', timestamp)::date as date,
                symbol,
                quantity as quantity_end,
                amount as amount_end,   
                row_number() over(
                partition by date_trunc('day', timestamp)::date
                order by timestamp desc) as rn
            from silver.asset_snapshot	
        )
        select date, symbol, quantity_end, amount_end
        from asset_last_ts
        where rn = 1
        """
    execute_script(conn, sql)

def truncate_gold(conn):
    sql = """TRUNCATE TABLE
         gold.asset_daily,
         gold.portfolio_daily
        """
    execute_script(conn, sql)

def rebuild_gold(conn):
    truncate_gold(conn)
    build_asset_daily(conn)
    build_portfolio_daily(conn)




