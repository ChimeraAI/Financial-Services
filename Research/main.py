from datetime import timedelta
from datetime import date
from controller.etl import etl
from model.postgresql import postgresql

def main():
    start = date.today() - timedelta(days=30)
    end = date.today()
    file = 'C:\\Users\\yimin\\Documents\\Github Repos\\Financial-Services\\Research\\files\\Tracker.csv'
    # etl().excel_import_watchlist(file)
    watchlist = postgresql().query_fxn('research_db','select symbol from research_sch.watchlist;')
    etl().iex_import_historical_data(watchlist,start,end)

if __name__ == "__main__":
    main()