import os
import json
import typing
import datetime
import pandas
import requests
import matplotlib.pyplot


class Core:

    '''
    Provides common functionality used throughout
    the :mod:`BharatFinTrack` package.
    '''

    def _excel_file_extension(
        self,
        file_path: str
    ) -> str:

        '''
        Returns the extension of an Excel file.

        Parameters
        ----------
        file_path : str
            Path of the Excel file.

        Returns
        -------
        str
            Extension of the Excel file.
        '''

        output = os.path.splitext(file_path)[-1]

        return output

    def is_valid_figure_extension(
        self,
        file_path: str
    ) -> bool:

        '''
        Returns whether the given path is a valid figure file.

        Parameters
        ----------
        file_path : str
            Path of the figure file.

        Returns
        -------
        bool
            True if the file path is valid, False otherwise.
        '''

        figure = matplotlib.pyplot.figure(
            figsize=(1, 1)
        )
        file_ext = os.path.splitext(file_path)[-1][1:]
        supported_ext = list(figure.canvas.get_supported_filetypes().keys())
        output = file_ext in supported_ext

        matplotlib.pyplot.close(figure)

        return output

    def string_to_date(
        self,
        date_string: str
    ) -> datetime.date:

        '''
        Converts a date string is in format 'DD-MMM-YYYY' to a `datetime.date` object.

        Parameters
        ----------
        date_string : str
            Date string in the format 'DD-MMM-YYYY'.

        Returns
        -------
        datetime.date
            A `datetime.date` object corresponding to the input date string.
        '''

        output = datetime.datetime.strptime(date_string, '%d-%b-%Y').date()

        return output

    @property
    def default_http_headers(
        self,
    ) -> dict[str, str]:

        '''
        Returns the default http headers to be used for the web requests.
        '''

        output = {
            'Content-Type': 'application/json; charset=UTF-8',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
            'Origin': 'https://www.niftyindices.com',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Connection': 'keep-alive',
            'X-Requested-With': 'XMLHttpRequest'
        }

        return output

    @property
    def url_nse_index_tri_data(
        self,
    ) -> str:

        '''
        Returns the url to access TRI (Total Return Index) data of NSE equity indices.
        '''

        output = 'https://www.niftyindices.com/Backpage.aspx/getTotalReturnIndexString'

        return output

    def _download_nse_tri(
        self,
        index_api: str,
        start_date: str,
        end_date: str,
        index: str,
        http_headers: typing.Optional[dict[str, str]] = None
    ) -> pandas.DataFrame:

        '''
        Helper method for the :meth:`NSETRI.download_historical_daily_data`.
        '''

        # payloads
        parameters = {
            'name': index_api,
            'startDate': start_date,
            'endDate': end_date,
            'indexName': index
        }
        payload = json.dumps(
            {
                'cinfo': json.dumps(parameters)
            }
        )

        # web request headers
        headers = self.default_http_headers if http_headers is None else http_headers

        # sent web requets
        response = requests.post(
            url=self.url_nse_index_tri_data,
            headers=headers,
            data=payload,
            timeout=10
        )
        response_data = response.json()
        records = json.loads(response_data['d'])
        df = pandas.DataFrame.from_records(records)
        df = df.iloc[:, -2:][::-1].reset_index(drop=True)
        df['Date'] = df['Date'].apply(
            lambda x: datetime.datetime.strptime(x, '%d %b %Y').date()
        )
        df = df.rename(columns={'TotalReturnsIndex': 'Close'})
        df['Close'] = df['Close'].astype(float)

        return df

    def sip_growth(
        self,
        invest: int,
        frequency: str,
        annual_return: float,
        years: int
    ) -> pandas.DataFrame:

        '''
        Calculates the SIP growth over a specified number of years for a fixed investment amount.

        Parameters
        ----------
        invest : int
            Fixed amount invested at each SIP interval.

        frequency : str
            Frequency of SIP contributions; must be one of ['yearly', 'quarterly', 'monthly', 'weekly'].

        annual_return : float
            Expected annual return rate in percentage.

        years : int
            Total number of years for the SIP investment duration.

        Returns
        -------
        DataFrame
            A DataFrame containing columns for the annual investment,
            closing balance, and cumulative growth over the investment period.
        '''

        # frequency dictionary
        freq_value = {
            'yearly': 1,
            'quarterly': 4,
            'monthly': 12,
            'weekly': 52
        }

        if frequency in freq_value.keys():
            pass
        else:
            raise Exception(f'Select a valid frequency from {list(freq_value.keys())}')

        # cagr rate for the given frequency
        cagr = pow(1 + (annual_return / 100), 1 / freq_value[frequency]) - 1

        # SIP DataFrame
        df = pandas.DataFrame()
        for yr in range(years):
            df.loc[yr, 'Year'] = yr + 1
            if yr == 0:
                df.loc[yr, 'Invest'] = freq_value[frequency] * invest
            else:
                df.loc[yr, 'Invest'] = df.loc[yr - 1, 'Invest'] + freq_value[frequency] * invest
            total_freq = (yr + 1) * freq_value[frequency]
            df.loc[yr, 'Value'] = invest * (1 + cagr) * (((1 + cagr) ** total_freq - 1) / cagr)
        df['Multiple (X)'] = df['Value'] / df['Invest']

        return df

    def _github_action(
        self,
        integer: int
    ) -> str:

        '''
        A simple function that converts an integer to a string,
        which can trigger a GitHub action due to the modification of a '.py' file.
        '''

        output = str(integer)

        return output
