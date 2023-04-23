import yfinance as yf
from event_study import config as cfg

# Step 1

def yf_rec_to_csv(tic, pth, start=None, end=None):
    """Downloads analysts recommendation from YahooFinance and saves the
    information in a CSV file"""

    c = yf.Ticker(tic)
    c.history(start=start, end=end).tz_localize(None)
    # Makesure we only relevant dates
    if start is not None and end is not None:
        df = c.recommendations.loc[start:end]
    elif start is not None:
        df = c.recommendations.loc[start:]
    elif end is not None:
        df = c.recommendations.loc[:end]
    else:
        df = c.recommendations
        df.to_csv(pth)


def get_data(tic):
    """Downloads price and recommendation data for a given ticker `tic`
    given the sample period defined by the `config` variables `START` and
    `END`.
    Parameters
    ----------
    tic:str
        Ticker
    """
    # Get out put paths
    locs = cfg.csv_locs(tic)

    # Download and save prices
    print(f'Downloading prices for {tic} ...')
    df = yf.download(tic,
        start=cfg.START,
        end=cfg.END, ignore_tz=True)
    pth = locs['prc_csv']
    df.to_csv(pth)
    print('Done')

    # NOTE:Comment out the code below to ignore downloading analyst recommendations
    # Uncomment the code when the issue with yfinance is resolved

    # Download and save recs
    # print(f'Downloading recs for {tic}...')
    # yf_rec_to_csv(tic,pth=locs['rec_csv'],start=cfg.START,end=cfg.END)
    # print('Done')