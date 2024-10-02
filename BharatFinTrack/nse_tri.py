import typing
import datetime
import pandas
from .nse_product import NSEProduct
from .core import Core


class NSETRI:

    '''
    Download and analyze NSE TRI (Total Return Index) data,
    including both price index and dividend reinvestment.
    '''

    @property
    def _index_api(
        self
    ) -> dict[str, str]:

        '''
        Returns a dictionary containing equity indices as keys
        and corresponding API names as values.
        '''

        df = NSEProduct()._dataframe_equity_index
        output = dict(
            zip(df['Index Name'], df['API TRI'])
        )

        return output

    @property
    def non_open_source_indices(
        self
    ) -> list[str]:

        '''
        Returns a list of equity indices that are not open-source.
        '''

        df = NSEProduct()._dataframe_equity_index
        df = df[df['API TRI'] == 'NON OPEN SOURCE']
        output = list(df['Index Name'].sort_values())

        return output

    def is_index_open_source(
        self,
        index: str,
    ) -> bool:

        '''
        Check whether the index data is open-source.

        Parameters
        ----------
        index : str
            Name of the index.

        Returns
        -------
        bool
            True if the index data is open-source, False otherwise.
        '''

        if NSEProduct().is_index_exist(index) is True:
            pass
        else:
            raise Exception(f'"{index}" index does not exist.')

        output = index not in self.non_open_source_indices

        return output

    def download_historical_daily_data(
        self,
        index: str,
        start_date: typing.Optional[str] = None,
        end_date: typing.Optional[str] = None,
        http_headers: typing.Optional[dict[str, str]] = None,
        excel_file: typing.Optional[str] = None
    ) -> pandas.DataFrame:

        '''
        Downloads historical daily closing values for the specified index
        between the given start and end dates, both inclusive, and returns them in a DataFrame.

        Parameters
        ----------
        index : str
            Name of the index.

        start_date : str, optional
            Start date in the format 'DD-MMM-YYYY'.
            Defaults to the index's base date if None is provided.

        end_date : str, optional
            End date in the format 'DD-MMM-YYYY'.
            Defaults to the current date if None is provided.

        http_headers : dict, optional
            HTTP headers for the web request. If not provided, defaults to
            :attr:`BharatFinTrack.core.Core.default_http_headers`.

        excel_file : str, optional
            Path to an Excel file to save the DataFrame.

        Returns
        -------
        DataFrame
            A DataFrame with two columns: 'Date' and 'Close', representing the daily
            closing values for the index between the specified dates.
        '''

        # check index name
        if self.is_index_open_source(index) is True:
            index_api = self._index_api.get(index, index)
        else:
            raise Exception(f'"{index}" index data is not available as open-source.')

        # check start date
        if start_date is not None:
            pass
        else:
            start_date = NSEProduct().get_equity_index_base_date(index)
        date_s = Core().string_to_date(start_date)

        # check end date
        if end_date is not None:
            pass
        else:
            end_date = datetime.date.today().strftime('%d-%b-%Y')
        date_e = Core().string_to_date(end_date)

        # check end date is greater than start date
        difference_days = (date_e - date_s).days
        if difference_days >= 0:
            pass
        else:
            raise Exception(f'Start date {start_date} cannot be later than end date {end_date}.')

        # check the Excel file extension first
        excel_ext = Core()._excel_file_extension(excel_file) if excel_file is not None else None
        if excel_ext is None or excel_ext == '.xlsx':
            pass
        else:
            raise Exception(f'Input file extension "{excel_ext}" does not match the required ".xlsx".')

        # downloaded DataFrame
        df = Core()._download_nse_tri(
            index_api=index_api,
            start_date=start_date,
            end_date=end_date,
            index=index,
            http_headers=http_headers
        )

        # saving the DataFrame
        if excel_ext is None:
            pass
        else:
            with pandas.ExcelWriter(excel_file, engine='xlsxwriter') as excel_writer:
                df.to_excel(excel_writer, index=False)
                worksheet = excel_writer.sheets['Sheet1']
                worksheet.set_column(0, 1, 12)

        return df
