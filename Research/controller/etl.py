from iexfinance.stocks import get_historical_data
from model.postgresql import postgresql
import pandas as pd

class etl:

    __token = "pk_6bae0caafd6942bcbfcb3374895fd4ae"
    __symbols = []
    __postgresql = ''

    def __init__(self):
        self.__postgresql = postgresql()

    def iex_import_historical_data(self,symbols,start,end):
        self.__setSymbols(symbols)
        post_data = []
        schema = 'research_sch'
        table = 'raw_historical_prices'
        iex_columns = ['symbol','open','close','high','low','volume','label']
        columns = ['symbol','open','close','high','low','volume','date']
        for symbol in self.__symbols:
            raw_data = get_historical_data(symbol, start, end, output_format = 'pandas', token = self.__token)
            filter_data = raw_data[iex_columns]
            post_data = list(filter_data.itertuples(index=False))
            self.__postgresql.write_fxn_list(schema,table,post_data,columns)
            post_data.clear()
    
    def excel_import_watchlist(self,file):
        post_data = []
        schema = 'research_sch'
        table = 'watchlist'
        excel_columns = ['Symbol','Name','52wk Hi','52wk Lo','Market Cap','Sector']
        df = pd.read_csv(file)
        df.drop(df.tail(1).index,inplace=True)
        df = df[excel_columns]
        columns = ['symbol','name','yrHi','yrLow','marketCap','sector']
        post_data = list(df.itertuples(index=False))
        self.__postgresql.write_fxn_list(schema,table,post_data,columns)
        post_data.clear()

    def __setSymbols(self,symbols):
        print("Begin to set symbol")
        for symbol in symbols:
            self.__symbols.append(symbol[0])