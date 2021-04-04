from datetime import datetime
from iexfinance.stocks import get_historical_data

token = "pk_6bae0caafd6942bcbfcb3374895fd4ae"

start = datetime(2021, 3, 1)
end = datetime(2021, 4, 1)
rawImport = get_historical_data("tsla", start, end, output_format = 'pandas', token = token)
filterImport = rawImport[['symbol','open','close','high','low','volume','label']]


