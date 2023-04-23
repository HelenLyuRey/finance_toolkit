from event_study import config as cfg
import pandas as pd

# Step 3

def mk_event_df(tic):
    """Subsets and processes recommendations given a ticker and return a data
    frame with all events in the sample.
    Parameters
    ----------
    tic:str
        Ticker
    Returns
    -------
    pandas dataframe

        The columns are:
        * event_date: string
            Date string with format 'YYYY-MM-DD'
        * firm: string
            Name of the firm (uppercase)
        * event_type: string
            Either "downgrade" or "upgrade"
        index: integer
            Index named 'event_id' starting at 1

    Notes
    -----
    This function will perform th efollowing actions:
    1. Read the appropriate CSV file with recommendations into a dataframe
    2. Create variables identifying the firm and the event date
    3. Deal with multiple recommendations
    4. Create a table with all relevant events
    """

    # ----------------------------------------------------------------------
    # Step1. Read the appropriate CSV file with recommendations into a dataframe
    # ----------------------------------------------------------------------
    # Read the source file, set the column 'Date' as a DatetimeIndex

    pth = cfg.csv_locs(tic)['rec_csv']
    df = pd.read_csv(pth, index_col='Date', parse_dates=['Date'])
    # Standardise column names and keep only the columns of interest
    cols = ['firm', 'action']
    df = cfg.standardise_colnames(df)[cols]


    # ----------------------------------------------------------------------
    # Step2. Create variables identifying the firm and the event date
    # ----------------------------------------------------------------------
    # Replace the values of the column "firm" with their upper case version
    # Alternative: df.loc[:,'firm']=[x.upper() for x in df.loc[:,'firm']]
    df.loc[:, 'firm'] = df.loc[:, 'firm'].str.upper()

    # The column 'firm' is already part of the source data,so we only need to
    # create the 'event_date' column
    df.loc[:, 'event_date'] = df.index.strftime('%Y-%m-%d')


    # ----------------------------------------------------------------------
    # Step3. Deal with multiple recommendations
    # ----------------------------------------------------------------------
    df.sort_index(inplace=True)
    groups = df.groupby(['event_date', 'firm'])
    # Select the last obs for each group using the GroupBy method `last`
    # Note: result is a dataframe with a multi-index.There set_index will convert
    # the se indexes to columns
    df = groups.last().reset_index()


    # ----------------------------------------------------------------------
    # Step 4. Create a table with all relevant events
    # ----------------------------------------------------------------------
    # Step3.4.1: Create a subset of the original data frame that
    # contains only observations for which the action column is either "up" or "down"
    cond = df.loc[:, 'action'].str.contains('up|down')
    df = df.loc[cond]

    # Step3.4.2: Create a new column called event_type with values
    # "upgrade" or "downgrade", corresponding to "up" and "down"
    # values of the column action
    df.loc[:, 'event_type'] = df['action'].apply(_mk_et)

    # Step3.4.3: Make sure our index (which we will call event_id ) starts at 1.
    df.reset_index(inplace=True)
    df.index = df.index + 1
    df.index.name = 'event_id'

    return df


def _mk_et(value):
    """Converts the string `value` as follows:
        -"down"-->"downgrade"
        -"up"-->"upgrade"
    and raise an exception if value is not "up" or "down"
    """
    if value == 'down':
        return 'downgrade'
    elif value == 'up':
        return 'upgrade'
    else:
        raise Exception(f'Unknown value for column `action`: {value}')

print(mk_event_df('TSLA'))