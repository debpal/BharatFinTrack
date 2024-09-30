import os
import json
import typing
import datetime
import pandas
import requests


class Core:

    '''
    Core functionality of :mod:`BharatFinTrack` module.
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
            data=payload
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
