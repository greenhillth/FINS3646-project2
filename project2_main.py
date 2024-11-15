""" scaffold for project2


"""
# IMPORTANT: You should not import any other modules. This means that the
# only import statements in this module should be the ones below. In
# particular, this means that you cannot import modules inside functions.

import os

import numpy as np
import pandas as pd

import tkutils


# ----------------------------------------------------------------------------
#   Aux functions
# ----------------------------------------------------------------------------
def read_dat(pth: str) -> pd.DataFrame:
    """ Create a data frame with the raw content of a .dat file.

    This function loads data from a `.dat` file into a data frame. It does not
    parse or clean the data, nor does it assign specific data types. All
    entries in the resulting data frame are stored as `str` instances, and all
    columns have an object `dtype`. This function can be used to load any
    `.dat` file.

    Parameters
    ----------
    pth: str
        The location of a .dat file. 

    Returns
    -------
    frame:
        A data frame. The dtype of each column is 'object' and the type of
        each element is `str`
    """
    # IMPORTANT: Please do not modify this function
    return pd.read_csv(pth, dtype=str).astype(str)


def str_to_float(value: str) -> float:
    """ This function attempts to convert a string into a float. It returns a
    float if the conversion is successful and None otherwise. 

    Parameters
    ----------
    value: str
        A string representing a float. Quotes and spaces will be ignored. 

    Returns
    -------
    float or None
        A float representing the string or None

    """
    # IMPORTANT: Please do not modify this function
    out = value.replace('"', '').replace("'", '').strip()
    try:
        out = pd.to_numeric(out)
    except:
        return None
    return float(out)


def fmt_col_name(label: str) -> str:
    """ Formats a column name according to the rules specified in the "Project
    Description" slide

    Parameters
    ----------
    label: str
        The original column label. See the "Project description" slide for
        more information

    Returns
    -------
    str:
        The formatted column label. 

    Examples
    --------

    - `fmt_col_name(' Close') -> 'close'

    - `fmt_col_name('Adj    Close') -> 'adj_close'

    """
    # <COMPLETE_THIS_PART>

    return "_".join(label.strip().lower().split())


def fmt_ticker(value: str) -> str:
    """ Formats a ticker value according to the rules specified in the "Project
    Description" slide

    Parameters
    ----------
    value: str
        The original ticker value

    Returns
    -------
    str:
        The formatted ticker value.

    """
    # <COMPLETE_THIS_PART>

    return value.replace("'", "").replace('"', "").replace(" ", "").upper()


def read_prc_dat(pth: str):
    """ This function produces a data frame with volume and return from a single
    `<PRICE_DAT>` file. 

    This function should clean the original data in `<PRICE_DAT>` as described
    in the "Project description" slide.

    Returns should be computed using adjusted closing prices.


    Parameters
    ----------
    pth: str
        The location of a <PRICE_DAT> file. This file includes price and
        volume information for different tickers and dates. See the project
        description for more information on these files.


    Returns
    -------
    frame: 
        A dataframe with formatted column names (in any order):

         Column     dtype
         ------     -----
         date       datetime64[ns]
         ticker     object
         return     float64
         volume     float64

    Notes
    -----

    Assume that there are no gaps in the time series of adjusted closing
    prices for each ticker.


    """
    # <COMPLETE_THIS_PART>

    # construct path (assuming pth is the relative path to prc.dat?)
    # TODO - check this jawn
    abspath = os.path.join(os.getcwd(), pth)
    raw = pd.read_csv(abspath)

    # format headers
    raw.columns = [fmt_col_name(name) for name in raw.columns]

    # sanitise data using regular expressions
    raw = raw.replace({
        r'[Oo]': 0,
        r".*-.*": np.nan,
        r'^["\']|["\']$': ''},
        regex=True)

    dtypes = {
        "close": "float64",
        "date": "datetime64[ns]",
        "ticker": "object",
        "adj_close": "float64",
        "high": "float64",
        "low": "float64",
        "open": "float64",
        "volume": "float64"
    }

    # apply dtype map
    final = raw.astype(dtypes)

    # format tickers
    final['ticker'] = [fmt_ticker(tic) for tic in final['ticker']]

    # return only requested slice of df
    return final.loc[:, ['date', 'ticker', 'low', 'volume']]


def read_ret_dat(pth: str) -> pd.DataFrame:
    """ This function produces a data frame with volume and returns from a single
    `<RET_DAT>` file. 


    This function should clean the original data in `<RET_DAT>` as described
    in the "Project description" slide.

    Parameters
    ----------
    pth: str
        The location of a <RET_DAT> file. This file includes returns and
        volume information for different tickers and dates. See the project
        description for more information on these files.


    Returns
    -------
    frame: 
        A dataframe with columns (in any order):

          Column        dtype
          ------        -----
          date          datetime64[ns]
          ticker        object
          return        float64
          volume        float64

    Notes
    -----
    This .dat file also includes market returns. Market returns are 
    represented by a special ticker called 'MKT'

    """
    # <COMPLETE_THIS_PART>
    abspath = os.path.join(os.getcwd(), pth)
    raw = pd.read_csv(abspath)

    # format headers
    raw.columns = [fmt_col_name(name) for name in raw.columns]

    # sanitise data
    raw = raw.replace({
        r'[Oo]': 0,
        r'^["\']|["\']$': ''},
        regex=True)  # replace O's and remove quotes

    dtypes = {
        "date": "datetime64[ns]",
        "ticker": "object",
        "return": "float64",
        "volume": "float64"
    }

    # apply dtype map
    final = raw.astype(dtypes)

    # format tickers
    final['ticker'] = [fmt_ticker(tic) for tic in final['ticker']]

    return final


def mk_ret_df(
        pth_prc_dat: str,
        pth_ret_dat: str,
        tickers: list[str],
):
    """ Combine information from two sources to produce a data frame 
    with stock and market returns according to the following rules:

    - Returns should be computed using information from <PRICE_DAT>, if
      possible. If a ticker is not found in the <PRICE_DAT> file, then returns
      should be obtained from the <RET_DAT> file.

    - Market returns should always be obtained from the <RET_DAT> file.

    - Only dates with available market returns should be part of the index.


    Parameters
    ----------
    pth_prc_dat: str
        Location of the <PRICE_DAT> file with price and volume information.
        This is the same parameter as the one described in `read_prc_dat`

    pth_ret_dat: str
        Location of the <RET_DAT> file with returns and volume information.
        This is the same parameter as the one described in `read_ret_dat`

    tickers: list
        A list of (possibly unformatted) tickers to be included in the output
        data frame. 

    Returns
    -------
    frame:
        A data frame with a DatetimeIndex and the following columns (in any
        order):

        Column      dtype 
        ------      -----
        <tic0>      float64
        <tic1>      float64
        ...
        <ticN>      float64
        <mkt>       float64


        Where `<tic0>`, ..., `<ticN>` are formatted column labels with tickers
        in the list `tickers`, and `<mkt>` is the formatted column label
        representing market returns.

        Should only include dates with available market returns.


    """
    # <COMPLETE_THIS_PART>
