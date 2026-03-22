import typing
import pandas
import requests
import bs4
import io
from .helper import Helper


class NSEPRI:
    '''
    Provide functionalities to download and analyze NSE Price Return Index (PRI),
    excluding dividend reinvestment.
    '''

    @property
    def _url(
        self
    ) -> str:
        '''
        URL used to download PRI daily data.
        '''

        output = 'https://www.niftyindices.com/Backpage.aspx/getHistoricaldatatabletoString'

        return output

    def _download_daily_summary(
        self,
        http_headers: dict[str, str]
    ) -> pandas.DataFrame:
        '''
        Download the daily summary report for all NSE indices and generate a DataFrame.
        '''

        # Response from main URL
        main_url = 'https://www.niftyindices.com'
        csv_url = main_url + '/reports/daily-reports'
        response = requests.get(
            url=csv_url,
            headers=http_headers,
            timeout=10
        )

        # Content soup of the URL
        soup = bs4.BeautifulSoup(
            markup=response.content,
            features='html.parser'
        )

        # Resposne from the CSV file link
        for anchor in soup.find_all('a'):
            if isinstance(anchor, bs4.Tag):
                href = anchor.get('href')
                anchor_id = anchor.get('id')
                if isinstance(href, str) and href.endswith('.csv') and anchor_id == 'dailysnapOneDaybefore':
                    csv_link = main_url + href
                    response = requests.get(
                        url=csv_link,
                        headers=http_headers
                    )
                    # DataFrame
                    df = pandas.read_csv(
                        filepath_or_buffer=io.StringIO(response.text)
                    )
                    req_cols = {
                        'Index Name': 'Index Name',
                        'Index Date': 'Close Date',
                        'Closing Index Value': 'Close Value'
                    }
                    df = df[list(req_cols.keys())]
                    df = df.rename(
                        columns=req_cols
                    )
                    df['Index Name'] = df['Index Name'].apply(
                        lambda x: x.upper()
                    )

        return df

    @property
    def _index_name_change(
        self
    ) -> dict[str, str]:

        output = {
            'NIFTY 50 FUTURES INDEX': 'NIFTY 50 FUTURES PR',
            'NIFTY 50 FUTURES TR INDEX': 'NIFTY 50 FUTURES TR',
            'NIFTY HEALTHCARE INDEX': 'NIFTY HEALTHCARE'
        }

        return output

    def download_equity_close(
        self,
        csv_file: str,
        http_headers: typing.Optional[dict[str, str]] = None,
        untracked_base_equity: bool = False,
    ) -> pandas.DataFrame:
        '''
        Download closing values for all equity indices.

        Parameters
        ----------
        csv_file : str
            Path to a CSV file to save the DataFrame.

        http_headers : dict, optional
            HTTP header dictionary used for the web request. If the default header is not suitable
            for the user's environment,a custom header must be provided. The header must include
            the key ``content-type`` with value ``application/json; charset=UTF-8``. The default header
            can be obtained via :attr:`BharatFinTrack.helper.Helper._default_http_headers`.

        untracked_base_equity : bool, optional
            If True, print equity indices present in the downloaded data but missing from the in-built base file.

        Returns
        -------
        DataFrame
            DataFrame containing closing values for all equity indices.
        '''

        # Check static type of input variable origin
        Helper()._validate_variable_origin_static_type(
            vars_types=typing.get_type_hints(
                obj=self.download_equity_close
            ),
            vars_values=locals()
        )

        # Validate output file path
        Helper()._validate_file_path(
            input_file=csv_file,
            input_ext='.csv'
        )

        # Web request headers
        http_headers = Helper()._http_headers_default if http_headers is None else http_headers

        # DataFrame
        df = self._download_daily_summary(
            http_headers=http_headers
        )
        df['Index Name'] = df['Index Name'].apply(
            lambda x: self._index_name_change.get(x, x)
        )

        # Base DataFrame
        base_df = Helper()._equity_base_midf.reset_index()
        equity_df = base_df.merge(
            right=df,
            on=['Index Name']
        )
        equity_df = equity_df.drop(
            columns=['API TRI']
        )

        Helper()._df_date_to_csv(
            df=equity_df,
            csv_file=csv_file,
            date_cols=['Base Date', 'Close Date']
        )

        # Find missing indices in base file
        if untracked_base_equity:
            col = 'Index Name'
            untracked_indices = df[~df[col].isin(base_df[col].tolist())][col].tolist()
            remove_word = (
                'VIX',
                'G-SEC',
                'BHARAT BOND',
                '1D RATE'
            )
            untracked_equity = [
                ui for ui in untracked_indices if not any(rm in ui for rm in remove_word)
            ]
            print('Untracked equity indices from the base file:')
            print(untracked_equity)
            print("-" * 100)

        return equity_df
