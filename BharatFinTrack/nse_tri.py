import typing
import datetime
import dateutil.relativedelta
import pandas
import matplotlib
import matplotlib.pyplot
import tempfile
import os
import pyxirr
from .nse_product import NSEProduct
from .core import Core


class NSETRI:

    '''
    Provides functionality for downloading and analyzing
    NSE Equity Total Return Index (TRI) data,
    including both price and dividend reinvestment.
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
        excel_file: str,
        start_date: typing.Optional[str] = None,
        end_date: typing.Optional[str] = None,
        http_headers: typing.Optional[dict[str, str]] = None
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

        # check the Excel file extension first
        excel_ext = Core()._excel_file_extension(excel_file)
        if excel_ext == '.xlsx':
            pass
        else:
            raise Exception(f'Input file extension "{excel_ext}" does not match the required ".xlsx".')

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

        # downloaded DataFrame
        df = Core()._download_nse_tri(
            index_api=index_api,
            start_date=start_date,
            end_date=end_date,
            index=index,
            http_headers=http_headers
        )

        # saving the DataFrame
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
        with tempfile.TemporaryDirectory() as tmp_dir:
            add_df = self.download_historical_daily_data(
                index=index,
                excel_file=os.path.join(tmp_dir, 'temporary.xlsx'),
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
        base_df = base_df.groupby(level='Category').head(2) if test_mode is True else base_df
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
        with tempfile.TemporaryDirectory() as tmp_dir:
            for base_index in base_df.index:
                try:
                    index_df = self.download_historical_daily_data(
                        index=base_df.loc[base_index, 'Index Name'],
                        excel_file=os.path.join(tmp_dir, 'temporary.xlsx'),
                        start_date=start_date,
                        end_date=end_date
                    )
                    base_df.loc[base_index, 'Close Date'] = index_df.iloc[-1, 0]
                    base_df.loc[base_index, 'Close Value'] = index_df.iloc[-1, -1]
                except Exception:
                    print(base_df.loc[base_index, 'Index Name'])
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

    def sort_equity_value_from_launch(
        self,
        input_excel: str,
        output_excel: str,
    ) -> pandas.DataFrame:

        '''
        Returns equity indices sorted in descending order by TRI values since launch.

        Parameters
        ----------
        input_excel : str
            Path to the input Excel file.

        output_excel : str
            Path to an Excel file to save the output DataFrame.

        Returns
        -------
        DataFrame
            A DataFrame sorted in descending order by TRI values since launch.
        '''

        # check the Excel file extension first
        excel_ext = Core()._excel_file_extension(output_excel)
        if excel_ext == '.xlsx':
            pass
        else:
            raise Exception(f'Input file extension "{excel_ext}" does not match the required ".xlsx".')

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
        input_excel : str
            Path to the input Excel file.

        output_excel : str
            Path to an Excel file to save the output DataFrame.

        Returns
        -------
        DataFrame
            A DataFrame sorted in descending order by CAGR (%) values since launch.
        '''

        # check the Excel file extension first
        excel_ext = Core()._excel_file_extension(output_excel)
        if excel_ext == '.xlsx':
            pass
        else:
            raise Exception(f'Input file extension "{excel_ext}" does not match the required ".xlsx".')

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
        input_excel : str
            Path to the input Excel file.

        output_excel : str
            Path to an Excel file to save the output DataFrame.

        Returns
        -------
        DataFrame
            A multi-index DataFrame sorted in descending order by CAGR (%) values since launch
            within each index category.
        '''

        # check the Excel file extension first
        excel_ext = Core()._excel_file_extension(output_excel)
        if excel_ext == '.xlsx':
            pass
        else:
            raise Exception(f'Input file extension "{excel_ext}" does not match the required ".xlsx".')

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

    def compare_cagr_over_price_from_launch(
        self,
        tri_excel: str,
        price_excel: str,
        output_excel: str
    ) -> pandas.DataFrame:

        '''
        Compares the CAGR (%) between TRI and Price for NSE indices since launch.

        Parameters
        ----------
        tri_excel : str
            Path to the Excel file obtained from :meth:`BharatFinTrack.NSETRI.sort_equity_cagr_from_launch` method.

        price_excel : str
            Path to the Excel file obtained from :meth:`BharatFinTrack.NSEIndex.sort_equity_cagr_from_launch` method.

        output_excel : str
            Path to an Excel file to save the output DataFrame.

        Returns
        -------
        DataFrame
            A DataFrame containing the difference in CAGR (%) between TRI to Price since launch.
        '''

        # check the Excel file extension first
        excel_ext = Core()._excel_file_extension(output_excel)
        if excel_ext == '.xlsx':
            pass
        else:
            raise Exception(f'Input file extension "{excel_ext}" does not match the required ".xlsx".')

        # TRI Dataframe
        tri_df = pandas.read_excel(tri_excel)
        tri_df = tri_df.rename(
            columns={'CAGR(%)': 'TRI-CAGR(%)'}
        )
        for date_col in ['Base Date', 'Close Date']:
            tri_df[date_col] = tri_df[date_col].apply(lambda x: x.date())

        # Price DataFrame
        price_df = pandas.read_excel(price_excel)
        price_df = price_df.rename(
            columns={'CAGR(%)': 'PRICE-CAGR(%)'}
        )

        # merge TRI and PRICE DataFrames
        df = tri_df.merge(
            right=price_df[['Index Name', 'PRICE-CAGR(%)']],
            on='Index Name',
            how='left'
        )
        df['Difference(%)'] = tri_df['TRI-CAGR(%)'] - price_df['PRICE-CAGR(%)']
        df = df.drop(
            columns=['Close Value', 'Close/Base']
        )

        # saving the DataFrame
        with pandas.ExcelWriter(output_excel, engine='xlsxwriter') as excel_writer:
            df.to_excel(excel_writer, index=False)
            workbook = excel_writer.book
            worksheet = excel_writer.sheets['Sheet1']
            # format columns
            for col_num, col_df in enumerate(df.columns):
                if col_df == 'Index Name':
                    worksheet.set_column(col_num, col_num, 60)
                elif col_df.endswith('(%)'):
                    worksheet.set_column(
                        col_num, col_num, 15,
                        workbook.add_format({'num_format': '#,##0.00'})
                    )
                else:
                    worksheet.set_column(col_num, col_num, 15)

        return df

    def yearwise_sip_analysis(
        self,
        input_excel: str,
        monthly_invest: int,
        output_excel: str
    ) -> pandas.DataFrame:

        '''
        Calculates the year-wise closing value, growth multiples, and annualized XIRR (%)
        of a fixed monthly SIP, based on contributions made on the first date of each month.

        Parameters
        ----------
        input_excel : str
            Path to the Excel file obtained from :meth:`BharatFinTrack.NSETRI.download_historical_daily_data`
            and :meth:`BharatFinTrack.NSETRI.update_historical_daily_data` methods.

        monthly_invest : int
            Fixed investment amount contributed on the first date of each month.

        output_excel : str
            Path to an Excel file to save the output DataFrame.

        Returns
        -------
        DataFrame
            A DataFrame containing the year-wise closing value, growth multiples,
            and annualized XIRR (%) for the fixed SIP investment.
        '''

        # check the Excel file extension first
        excel_ext = Core()._excel_file_extension(output_excel)
        if excel_ext == '.xlsx':
            pass
        else:
            raise Exception(f'Input file extension "{excel_ext}" does not match the required ".xlsx".')

        # input DataFrame
        df = pandas.read_excel(input_excel)
        df['Date'] = df['Date'].apply(lambda x: x.date())

        # start and end dates
        start_date = df['Date'].min()
        end_date = df['Date'].max()

        # monthly first date
        month_1d = pandas.date_range(
            start=start_date,
            end=end_date,
            freq='MS'
        )
        month_1d = list(map(lambda x: x.date(), month_1d))
        month_1d = pandas.Series([start_date] + month_1d + [end_date]).unique()

        # DataFrame of monthly open and close value
        month_df = pandas.DataFrame(
            columns=['Date', 'Open', 'Close']
        )
        for idx, dates in enumerate(zip(month_1d[:-1], month_1d[1:])):
            idx_df = df[(df['Date'] >= dates[0]) & (df['Date'] < dates[1])]
            month_df.loc[idx, 'Date'] = idx_df.iloc[0, 0]
            month_df.loc[idx, 'Open'] = idx_df.iloc[0, 1]
            month_df.loc[idx, 'Close'] = idx_df.iloc[-1, -1]

        # date difference
        date_diff = dateutil.relativedelta.relativedelta(end_date, start_date)
        year_diff = date_diff.years

        # SIP DataFrame
        index_divisor = 1000
        sip_df = pandas.DataFrame()
        for idx in range(year_diff + 1):
            # year-wise SIP investment
            if idx < year_diff:
                sip_year = idx + 1
                sip_start = end_date.replace(year=end_date.year - sip_year)
                yi_df = month_df[(month_df['Date'] >= sip_start) & (month_df['Date'] < end_date)].reset_index(drop=True)
            else:
                sip_year = round(year_diff + (end_date.replace(year=end_date.year - year_diff) - start_date).days / 365, 1)
                yi_df = month_df.copy()
            yi_df['Invest'] = monthly_invest
            yi_df['Cumm-Invest'] = yi_df['Invest'].cumsum()
            open_nav = yi_df['Open'] / index_divisor
            yi_df['Unit'] = (yi_df['Invest'] / open_nav)
            yi_df['Cum-Unit'] = yi_df['Unit'].cumsum()
            close_nav = yi_df['Close'] / index_divisor
            yi_df['Value'] = (yi_df['Cum-Unit'] * close_nav)
            # year-wise SIP summary
            sip_df.loc[idx, 'Year'] = sip_year
            sip_df.loc[idx, 'Start Date'] = yi_df.iloc[0, 0]
            sip_df.loc[idx, 'Invest'] = yi_df.iloc[-1, -4]
            sip_df.loc[idx, 'Close Date'] = end_date
            sip_df.loc[idx, 'Value'] = yi_df.iloc[-1, -1]
            sip_df.loc[idx, 'Multiple (X)'] = sip_df.loc[idx, 'Value'] / sip_df.loc[idx, 'Invest']
            sip_dates = list(yi_df['Date']) + [end_date]
            sip_transactions = list(-1 * yi_df['Invest']) + [yi_df['Value'].iloc[-1]]
            xirr = pyxirr.xirr(zip(sip_dates, sip_transactions))
            sip_df.loc[idx, 'XIRR (%)'] = 100 * (xirr if xirr is not None else 0.0)

        # drop duplicates row if any
        sip_df = sip_df.drop_duplicates(ignore_index=True)

        # saving DataFrame
        with pandas.ExcelWriter(output_excel, engine='xlsxwriter') as excel_writer:
            sip_df.to_excel(excel_writer, index=False)
            workbook = excel_writer.book
            worksheet = excel_writer.sheets['Sheet1']
            # format columns
            for col_num, col_df in enumerate(sip_df.columns):
                if any(col_df.endswith(i) for i in ['(%)', 'Year', '(X)']):
                    worksheet.set_column(
                        col_num, col_num, 15,
                        workbook.add_format({'num_format': '#,##0.0'})
                    )
                else:
                    worksheet.set_column(
                        col_num, col_num, 15,
                        workbook.add_format({'num_format': '#,##0'})
                    )

        return sip_df

    def sip_summary_from_given_date(
        self,
        excel_file: str,
        start_year: int,
        start_month: int,
        monthly_invest: int
    ) -> dict[str, str]:

        '''
        Calculates the closing value, growth multiples, and annualized XIRR (%) of a fixed monthly
        SIP starting from a specified date, based on contributions made on the first date of each month.

        Parameters
        ----------
        excel_file : str
            Path to the Excel file obtained from :meth:`BharatFinTrack.NSETRI.download_historical_daily_data`
            and :meth:`BharatFinTrack.NSETRI.update_historical_daily_data` methods.

        start_year : int
            Year when the SIP begins.

        start_month : int
            Month (1 to 12) when the SIP begins.

        monthly_invest : int
            Fixed investment amount contributed on the first date of each month

        Returns
        -------
        dict
            A dictionary containing the closing value, growth multiples, and annualized XIRR (%)
            for the fixed SIP investment starting from a specified date.
        '''

        # SIP summary
        summary = {}

        # input DataFrame
        df = pandas.read_excel(excel_file)
        df['Date'] = df['Date'].apply(lambda x: x.date())

        # start and end dates
        start_date = datetime.date(
            year=start_year,
            month=start_month,
            day=1
        )
        end_date = df.iloc[-1, 0]

        # filtered DataFrame
        if start_date > df.iloc[-1, 0]:
            raise Exception(
                'Given year and month return an empty DataFrame.'
            )
        elif df.iloc[0, 0] <= start_date <= df.iloc[-1, 0]:
            summary['Start date'] = start_date.strftime('%d-%b-%Y')
        else:
            summary['Given date'] = start_date.strftime('%d-%b-%Y')
            df = df[(df['Date'] >= start_date)].reset_index(drop=True)
            start_date = df.iloc[0, 0]
            summary['Actual start date'] = start_date.strftime('%d-%b-%Y')

        # month first date
        month_1d = pandas.date_range(
            start=start_date,
            end=end_date,
            freq='MS'
        )
        month_1d = list(map(lambda x: x.date(), month_1d))
        month_1d = pandas.Series([start_date] + month_1d + [end_date]).unique()

        # DataFrame of monthly open and close value
        month_df = pandas.DataFrame(
            columns=['Date', 'Open', 'Close']
        )
        for idx, dates in enumerate(zip(month_1d[:-1], month_1d[1:])):
            idx_df = df[(df['Date'] >= dates[0]) & (df['Date'] < dates[1])]
            month_df.loc[idx, 'Date'] = idx_df.iloc[0, 0]
            month_df.loc[idx, 'Open'] = idx_df.iloc[0, 1]
            month_df.loc[idx, 'Close'] = idx_df.iloc[-1, -1]

        # SIP parameters
        index_divisor = 1000
        date_diff = dateutil.relativedelta.relativedelta(end_date, start_date)
        month_df['Invest'] = monthly_invest
        month_df['Cumm-Invest'] = month_df['Invest'].cumsum()
        open_nav = month_df['Open'] / index_divisor
        month_df['Unit'] = (month_df['Invest'] / open_nav)
        month_df['Cum-Unit'] = month_df['Unit'].cumsum()
        close_nav = month_df['Close'] / index_divisor
        month_df['Value'] = (month_df['Cum-Unit'] * close_nav)
        # year-wise SIP summary
        summary['Duration'] = f'{date_diff.years} years, {date_diff.months} months, {date_diff.days} days'
        summary['Invest'] = f'{month_df.iloc[-1, -4]:.0f}'
        summary['Value'] = f'{month_df.iloc[-1, -1]:.0f}'
        summary['Multiple (X)'] = f'{month_df.iloc[-1, -1] / month_df.iloc[-1, -4]:.1f}'
        sip_dates = list(month_df['Date']) + [end_date]
        sip_transactions = list(-1 * month_df['Invest']) + [month_df['Value'].iloc[-1]]
        xirr = pyxirr.xirr(zip(sip_dates, sip_transactions))
        xirr_p = 100 * (xirr if xirr is not None else 0.0)
        summary['XIRR (%)'] = f'{xirr_p:.1f}'

        return summary
