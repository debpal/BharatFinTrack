import typing
import datetime
import dateutil.relativedelta
import pandas
import matplotlib
import warnings
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
        between the given start and end dates, both inclusive.

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
            A DataFrame containing the daily closing values for the index between the specified dates.
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

    def update_historical_daily_data(
        self,
        index: str,
        excel_file: str,
        http_headers: typing.Optional[dict[str, str]] = None
    ) -> pandas.DataFrame:

        '''
        Updates historical daily closing values from the last date in the input Excel file
        to the present and saves the aggregated data to the same file.

        Parameters
        ----------
        index : str
            Name of the index.

        excel_file : str
            Path to the Excel file containing existing historical data.

        http_headers : dict, optional
            HTTP headers for the web request. If not provided, defaults to
            :attr:`BharatFinTrack.core.Core.default_http_headers`.

        Returns
        -------
        DataFrame
            A DataFrame with updated closing values from the last recorded date to the present.
        '''

        # read the input Excel file
        df = pandas.read_excel(excel_file)
        df['Date'] = df['Date'].apply(
            lambda x: x.date()
        )

        # addition of downloaded DataFrame
        add_df = self.download_historical_daily_data(
            index=index,
            start_date=df.iloc[-1, 0].strftime('%d-%b-%Y'),
            end_date=datetime.date.today().strftime('%d-%b-%Y'),
            http_headers=http_headers
        )

        # updating the DataFrame
        update_df = pandas.concat([df, add_df]) if isinstance(add_df, pandas.DataFrame) else df
        update_df = update_df.drop_duplicates().reset_index(drop=True)

        # saving the DataFrame
        with pandas.ExcelWriter(excel_file, engine='xlsxwriter') as excel_writer:
            update_df.to_excel(excel_writer, index=False)
            worksheet = excel_writer.sheets['Sheet1']
            worksheet.set_column(0, 1, 12)

        return add_df

    def download_daily_summary_equity_closing(
        self,
        excel_file: str,
        http_headers: typing.Optional[dict[str, str]] = None,
        test_mode: bool = False
    ) -> pandas.DataFrame:

        '''
        Returns updated TRI closing values for all NSE indices.

        Parameters
        ----------
        excel_file : str, optional
            Path to an Excel file to save the DataFrame.

        http_headers : dict, optional
            HTTP headers for the web request. Defaults to
            :attr:`BharatFinTrack.core.Core.default_http_headers` if not provided.

        test_mode : bool, optional
            If True, the function will use a mocked DataFrame for testing purposes
            instead of the actual data. This parameter is intended for developers
            for testing purposes only and is not recommended for use by end-users.

        Returns
        -------
        DataFrame
            A DataFrame containing updated TRI closing values for all NSE indices.
        '''

        # processing base DataFrame
        base_df = NSEProduct()._dataframe_equity_index
        base_df = base_df.groupby(level='Category').head(1) if test_mode is True else base_df
        base_df = base_df.reset_index()
        base_df = base_df.drop(columns=['ID', 'API TRI'])
        base_df['Base Date'] = base_df['Base Date'].apply(lambda x: x.date())

        # check the Excel file extension first
        excel_ext = Core()._excel_file_extension(excel_file)
        if excel_ext == '.xlsx':
            pass
        else:
            raise Exception(f'Input file extension "{excel_ext}" does not match the required ".xlsx".')

        # downloading data
        today = datetime.date.today()
        week_ago = today - datetime.timedelta(days=7)
        end_date = today.strftime('%d-%b-%Y')
        start_date = week_ago.strftime('%d-%b-%Y')
        for base_index in base_df.index:
            try:
                index_df = self.download_historical_daily_data(
                    index=base_df.loc[base_index, 'Index Name'],
                    start_date=start_date,
                    end_date=end_date
                )
                base_df.loc[base_index, 'Close Date'] = index_df.iloc[-1, 0]
                base_df.loc[base_index, 'Close Value'] = index_df.iloc[-1, -1]
            except Exception:
                base_df.loc[base_index, 'Close Date'] = end_date
                base_df.loc[base_index, 'Close Value'] = -1000

        # removing error rows from the DataFrame
        base_df = base_df[base_df['Close Value'] != -1000].reset_index(drop=True)

        # saving the DataFrame
        with pandas.ExcelWriter(excel_file, engine='xlsxwriter') as excel_writer:
            base_df.to_excel(excel_writer, index=False)
            worksheet = excel_writer.sheets['Sheet1']
            # format columns
            for col_num, df_col in enumerate(base_df.columns):
                if df_col == 'Index Name':
                    worksheet.set_column(col_num, col_num, 60)
                else:
                    worksheet.set_column(col_num, col_num, 15)

        return base_df

    def download_equity_indices_updated_value(
        self,
        excel_file: str,
        http_headers: typing.Optional[dict[str, str]] = None,
        test_mode: bool = False
    ) -> pandas.DataFrame:

        '''
        Returns updated TRI values for all NSE indices.

        Parameters
        ----------
        excel_file : str, optional
            Path to an Excel file to save the DataFrame.

        http_headers : dict, optional
            HTTP headers for the web request. Defaults to
            :attr:`BharatFinTrack.core.Core.default_http_headers` if not provided.

        test_mode : bool, optional
            If True, the function will use a mocked DataFrame for testing purposes
            instead of the actual data. This parameter is intended for developers
            for testing purposes only and is not recommended for use by end-users.

        Returns
        -------
        DataFrame
            A DataFrame containing updated TRI values for all NSE indices.

        Warnings
        --------
        The method :meth:`BharatFinTrack.NSETRI.download_equity_indices_updated_value` is deprecated.
        Use the :meth:`BharatFinTrack.NSETRI.download_daily_summary_equity_closing` instead.
        '''

        warnings.warn(
            'download_equity_indices_updated_value(excel_file) is deprecated. Use download_daily_summary_equity_closing(excel_file) instead.',
            DeprecationWarning,
            stacklevel=2
        )

        output = self.download_daily_summary_equity_closing(
            excel_file=excel_file,
            http_headers=http_headers,
            test_mode=test_mode
        )

        return output

    def sort_equity_value_from_launch(
        self,
        input_excel: str,
        output_excel: str,
    ) -> pandas.DataFrame:

        '''
        Returns equity indices sorted in descending order by TRI values since launch.

        Parameters
        ----------
        inout_excel : str
            Path to the input Excel file.

        output_excel : str
            Path to an output Excel file to save the output DataFrame.

        Returns
        -------
        DataFrame
            A DataFrame sorted in descending order by TRI values since launch.
        '''

        # sorting DataFrame by TRI values
        df = pandas.read_excel(input_excel)
        df = df.drop(columns=['Category'])
        df = df.sort_values(
            by=['Close Value'],
            ascending=[False]
        )
        df = df.reset_index(drop=True)
        for col_df in df.columns:
            if 'Date' in col_df:
                df[col_df] = df[col_df].apply(lambda x: x.date())
            else:
                pass

        # saving the DataFrame
        excel_ext = Core()._excel_file_extension(output_excel)
        if excel_ext != '.xlsx':
            raise Exception(
                f'Input file extension "{excel_ext}" does not match the required ".xlsx".'
            )
        else:
            with pandas.ExcelWriter(output_excel, engine='xlsxwriter') as excel_writer:
                df.to_excel(excel_writer, index=False)
                worksheet = excel_writer.sheets['Sheet1']
                # format columns
                for col_num, col_df in enumerate(df.columns):
                    if col_df == 'Index Name':
                        worksheet.set_column(col_num, col_num, 60)
                    else:
                        worksheet.set_column(col_num, col_num, 15)

        return df

    def sort_equity_cagr_from_launch(
        self,
        input_excel: str,
        output_excel: str,
    ) -> pandas.DataFrame:

        '''
        Returns equity indices sorted in descending order by CAGR (%) since launch.

        Parameters
        ----------
        inout_excel : str
            Path to the input Excel file.

        output_excel : str
            Path to an output Excel file to save the output DataFrame.

        Returns
        -------
        DataFrame
            A DataFrame sorted in descending order by CAGR (%) values since launch.
        '''

        # DataFrame processing
        df = pandas.read_excel(input_excel)
        df = df.drop(columns=['Category'])
        for col_df in df.columns:
            if 'Date' in col_df:
                df[col_df] = df[col_df].apply(lambda x: x.date())
            else:
                pass
        df['Close/Base'] = df['Close Value'] / df['Base Value']
        df['Years'] = list(
            map(
                lambda x, y: dateutil.relativedelta.relativedelta(x, y).years, df['Close Date'], df['Base Date']
            )
        )
        df['Days'] = list(
            map(
                lambda x, y, z: (x - y.replace(year=y.year + z)).days, df['Close Date'], df['Base Date'], df['Years']
            )
        )
        total_years = df['Years'] + (df['Days'] / 365)
        df['CAGR(%)'] = 100 * (pow(df['Close Value'] / df['Base Value'], 1 / total_years) - 1)

        # sorting DataFrame by CAGR (%) values
        df = df.sort_values(
            by=['CAGR(%)', 'Years', 'Days'],
            ascending=[False, False, False]
        )
        df = df.reset_index(drop=True)

        # saving the DataFrame
        excel_ext = Core()._excel_file_extension(output_excel)
        if excel_ext != '.xlsx':
            raise Exception(
                f'Input file extension "{excel_ext}" does not match the required ".xlsx".'
            )
        else:
            with pandas.ExcelWriter(output_excel, engine='xlsxwriter') as excel_writer:
                df.to_excel(excel_writer, index=False)
                workbook = excel_writer.book
                worksheet = excel_writer.sheets['Sheet1']
                # format columns
                for col_num, col_df in enumerate(df.columns):
                    if col_df == 'Index Name':
                        worksheet.set_column(col_num, col_num, 60)
                    elif col_df == 'Close Value':
                        worksheet.set_column(
                            col_num, col_num, 15,
                            workbook.add_format({'num_format': '#,##0'})
                        )
                    elif col_df == 'Close/Base':
                        worksheet.set_column(
                            col_num, col_num, 15,
                            workbook.add_format({'num_format': '#,##0.0'})
                        )
                    elif col_df == 'CAGR(%)':
                        worksheet.set_column(
                            col_num, col_num, 15,
                            workbook.add_format({'num_format': '#,##0.00'})
                        )
                    else:
                        worksheet.set_column(col_num, col_num, 15)

        return df

    def category_sort_equity_cagr_from_launch(
        self,
        input_excel: str,
        output_excel: str,
    ) -> pandas.DataFrame:

        '''
        Returns equity indices sorted in descending order by CAGR (%) since launch
        within each index category.

        Parameters
        ----------
        inout_excel : str
            Path to the input Excel file.

        output_excel : str
            Path to an output Excel file to save the output DataFrame.

        Returns
        -------
        DataFrame
            A multi-index DataFrame sorted in descending order by CAGR (%) values since launch
            within each index category.
        '''

        # DataFrame processing
        df = pandas.read_excel(input_excel)
        for col_df in df.columns:
            if 'Date' in col_df:
                df[col_df] = df[col_df].apply(lambda x: x.date())
            else:
                pass
        df['Close/Base'] = df['Close Value'] / df['Base Value']
        df['Years'] = list(
            map(
                lambda x, y: dateutil.relativedelta.relativedelta(x, y).years, df['Close Date'], df['Base Date']
            )
        )
        df['Days'] = list(
            map(
                lambda x, y, z: (x - y.replace(year=y.year + z)).days, df['Close Date'], df['Base Date'], df['Years']
            )
        )
        total_years = df['Years'] + (df['Days'] / 365)
        df['CAGR(%)'] = 100 * (pow(df['Close Value'] / df['Base Value'], 1 / total_years) - 1)

        # Convert 'Category' column to categorical data types with a defined order
        categories = list(df['Category'].unique())
        df['Category'] = pandas.Categorical(
            df['Category'],
            categories=categories,
            ordered=True
        )

        # Sorting Dataframe
        df = df.sort_values(
            by=['Category', 'CAGR(%)', 'Years', 'Days'],
            ascending=[True, False, False, False]
        )
        dataframes = []
        for category in categories:
            category_df = df[df['Category'] == category]
            category_df = category_df.drop(columns=['Category']).reset_index(drop=True)
            dataframes.append(category_df)
        output = pandas.concat(
            dataframes,
            keys=[word.upper() for word in categories],
            names=['Category', 'ID']
        )

        # saving the DataFrame
        excel_ext = Core()._excel_file_extension(output_excel)
        if excel_ext != '.xlsx':
            raise Exception(
                f'Input file extension "{excel_ext}" does not match the required ".xlsx".'
            )
        else:
            with pandas.ExcelWriter(output_excel, engine='xlsxwriter') as excel_writer:
                output.to_excel(excel_writer, index=True)
                workbook = excel_writer.book
                worksheet = excel_writer.sheets['Sheet1']
                # number of columns for DataFrame indices
                index_cols = len(output.index.names)
                # format columns
                worksheet.set_column(0, index_cols - 1, 15)
                for col_num, col_df in enumerate(output.columns):
                    if col_df == 'Index Name':
                        worksheet.set_column(index_cols + col_num, index_cols + col_num, 60)
                    elif col_df == 'Close Value':
                        worksheet.set_column(
                            index_cols + col_num, index_cols + col_num, 15,
                            workbook.add_format({'num_format': '#,##0'})
                        )
                    elif col_df == 'Close/Base':
                        worksheet.set_column(
                            index_cols + col_num, index_cols + col_num, 15,
                            workbook.add_format({'num_format': '#,##0.0'})
                        )
                    elif col_df == 'CAGR(%)':
                        worksheet.set_column(
                            index_cols + col_num, index_cols + col_num, 15,
                            workbook.add_format({'num_format': '#,##0.00'})
                        )
                    else:
                        worksheet.set_column(index_cols + col_num, index_cols + col_num, 15)
                # Dataframe colors
                get_colormap = matplotlib.colormaps.get_cmap('Pastel2')
                colors = [
                    get_colormap(count / len(dataframes)) for count in range(len(dataframes))
                ]
                hex_colors = [
                    '{:02X}{:02X}{:02X}'.format(*[int(num * 255) for num in color]) for color in colors
                ]
                # coloring of DataFrames
                start_col = index_cols - 1
                end_col = index_cols + len(output.columns) - 1
                start_row = 1
                for df, color in zip(dataframes, hex_colors):
                    color_format = workbook.add_format({'bg_color': color})
                    end_row = start_row + len(df) - 1
                    worksheet.conditional_format(
                        start_row, start_col, end_row, end_col,
                        {'type': 'no_blanks', 'format': color_format}
                    )
                    start_row = end_row + 1

        return output
