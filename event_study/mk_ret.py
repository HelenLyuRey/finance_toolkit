# Step 2

from event_study import config as cfg
import pandas as pd

def mk_ret_df(tic):
    """Calculates return variables for the ticker `tic`
    Parameters
    ----------
    tic: str
        Ticker

    Returns
    -------
    dataframe
        This dataframe has the following structure:
        index: DatetimeIndex
        columns:
            ret: float
                Daily stock returns for this ticker `tic`
            mkt:float
                Daily market returns
    Notes
    -----
    This function perform the following operations:
    1.Get the location of the CSV file with the price information for `tic`
    2.Read the CSV file in to a dataframe
    3.Calculate stock returns
    4.Join market returns
    """

    # 1. Get the location of the CSV file with the price information for `tic`
    locs = cfg.csv_locs(tic)
    pth = locs['prc_csv']

    # 2. Read the CSV file in to a dataframe
    df = pd.read_csv(pth, index_col='Date', parse_dates=['Date'])

    # We will use the standardise_colnames from the config.py module to rename the
    # columns of the original data frame.
    df = cfg.standardise_colnames(df)

    # 3. Calculate stock returns
    df.sort_index(inplace=True)
    df.loc[:, 'ret'] = df.loc[:, 'close'].pct_change()

    # 4. Join market returns: We can use an inner join to
    # only include dates for which we have available data for both ret and mkt

    # 4.1: Get market returns
    ff_df = pd.read_csv(cfg.FF_FACTORS_CSV, index_col='Date', parse_dates=['Date'])

    # 4.2: Inner join between `df` and `ff_df`.
    # Note that:
    # a.We are only interested in two columns, 'mkt' and 'ret'
    # b.We do not want any missing observations
    cols = ['mkt', 'ret']
    df = df.join(ff_df, how='inner')[cols]
    df.dropna(inplace=True)

    return df

print(mk_ret_df('TSLA'))