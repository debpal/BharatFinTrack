import typing
import types
import os
import json
import datetime
import pandas
import requests
import dateutil.relativedelta


class Helper:
    '''
    Provide backend functionalities used throughout the :mod:`BharatFinTrack` package.
    '''

    def _validate_variable_origin_static_type(
        self,
        vars_types: dict[str, typing.Any],
        vars_values: dict[str, typing.Any]
    ) -> None:
        '''
        Validate input variables against their expected types.
        '''

        # Iterate name and type of method variables
        for v_name, v_type in vars_types.items():
            # Continute if varibale name is return
            if v_name == 'return':
                continue
            # Get origin type and value of the variable
            type_origin = typing.get_origin(v_type)
            type_value = vars_values[v_name]
            # If origin type in None
            if type_origin is None:
                if not isinstance(type_value, v_type):
                    raise TypeError(
                        f'Expected "{v_name}" to be "{v_type.__name__}", but got type "{type(type_value).__name__}"'
                    )
            # If origin type in not None
            else:
                # if origin type is a Union
                if type_origin in (typing.Union, types.UnionType):
                    # get argument types
                    type_args = tuple(
                        typing.get_origin(arg) or arg for arg in typing.get_args(v_type)
                    )
                    if not isinstance(type_value, type_args):
                        type_expect = [t.__name__ for t in type_args]
                        raise TypeError(
                            f'Expected "{v_name}" to be one of {type_expect}, but got type "{type(type_value).__name__}"'
                        )
                # If origin type in not a Union
                else:
                    if not isinstance(type_value, type_origin):
                        raise TypeError(
                            f'Expected "{v_name}" to be "{type_origin.__name__}", but got type "{type(type_value).__name__}"'
                        )

        return None

    def _validate_file_path(
        self,
        input_file: str,
        input_ext: str
    ) -> None:
        '''
        Validate the directory of the specified input file path and
        ensure that the file extension matches the expected type.
        '''

        # Directory path and file name
        dir_path, file_name = os.path.split(input_file)

        # Validate directory path
        if not os.path.isdir(dir_path):
            raise NotADirectoryError(
                f'Invalid directory path "{str(dir_path)}" for the input file'
            )

        # Check file extension
        file_ext = os.path.splitext(file_name)[-1]
        if file_ext.lower() != input_ext:
            raise ValueError(
                f'Input file extension "{file_ext}" does not match the required "{input_ext}"'
            )

        return None

    @property
    def _equity_base_midf(
        self
    ) -> pandas.DataFrame:
        '''
        Return a MultiIndex DataFrame containing the base parameters of the equity indices.
        '''

        file_path = os.path.join(
            os.path.dirname(__file__), 'index_base', 'base_equity.xlsx'
        )

        dataframes = pandas.read_excel(
            io=file_path,
            sheet_name=None
        )

        df = pandas.concat(
            dataframes,
            names=['Category', 'ID']
        )

        return df

    def _equity_index_base_param(
        self,
        index: str,
        check_open_source: bool
    ) -> pandas.DataFrame:
        '''
        Validate the specified equity index identifier, optionally verify
        whether its daily data is available as open-source, and return
        a DataFrame containing the base parameters of the index.
        '''

        # DataFrame of base parameters
        df = self._equity_base_midf

        # Validate index
        if index not in df['Index Name'].values:
            raise ValueError(
                f'Non-existent index name: "{index}"'
            )

        # Check index data is open-source
        if check_open_source:
            index_nos = df[df['API TRI'] == 'NON OPEN SOURCE']['Index Name'].values
            if index in index_nos:
                raise ValueError(
                    f'Historical daily data is not open-source for the index: "{index}"'
                )

        # Specific index DataFrame
        df = df.reset_index().drop(columns=['ID'])
        index_df = df[df['Index Name'] == index]
        index_df = index_df.reset_index(drop=True)

        return index_df

    @property
    def _date_str_fmt(
        self,
    ) -> str:
        '''
        Date string format used to parse a ``datetime.date`` object.
        '''

        output = '%d-%b-%Y'

        return output

    def _date_from_str(
        self,
        date_str: str
    ) -> datetime.date:
        '''
        Convert a date string is in the format ``DD-MMM-YYYY`` to a ``datetime.date`` object.
        '''

        output = datetime.datetime.strptime(date_str, self._date_str_fmt).date()

        return output

    def _date_end_later_start(
        self,
        start_date: str,
        end_date: str
    ) -> tuple[datetime.date, datetime.date]:
        '''
        Validate that the end date is later than the start date and
        return the corresponding start and end dates as ``datetime.date`` objects.
        '''

        # String to datetime.date objects
        date_s = self._date_from_str(
            date_str=start_date
        )
        date_e = self._date_from_str(
            date_str=end_date
        )

        # Check end date is greater than start date
        difference_days = (date_e - date_s).days
        if not difference_days >= 0:
            raise ValueError(
                f'Start date "{start_date}" cannot be later than end date "{end_date}"'
            )

        # List of ``datetime.date`` objects
        output = (date_s, date_e)

        return output

    def _date_difference(
        self,
        start_date: datetime.date,
        end_date: datetime.date
    ) -> dict[str, int]:
        '''
        Return the difference between two dates as years, months, and days.
        '''

        # Date difference
        date_diff = dateutil.relativedelta.relativedelta(end_date, start_date)

        # Convert difference in days, months, and years
        output = {
            'days': date_diff.days,
            'months': date_diff.months,
            'years': date_diff.years
        }

        return output

    @property
    def _http_headers_default(
        self,
    ) -> dict[str, str]:
        '''
        Return the default HTTP header dictionary to be used for the web requests.
        '''

        output = {
            'Content-Type': 'application/json; charset=UTF-8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36',
            'Referer': 'https://www.niftyindices.com/reports/historical-data',
            'Origin': 'https://www.niftyindices.com',
            'X-Requested-With': 'XMLHttpRequest'
        }

        return output

    def _df_not_empty(
        self,
        df: pandas.DataFrame,
        error_str: str
    ) -> None:
        '''
        Validate that the input DataFrame is not empty.
        '''

        if len(df) == 0:
            raise ValueError(
                error_str
            )

        return None

    def _download_index_data(
        self,
        url: str,
        index: str,
        index_api: str,
        start_date: str,
        end_date: str,
        http_headers: dict[str, str],
        price_type: str
    ) -> pandas.DataFrame:
        '''
        Download historical daily data of index.
        '''

        # Payloads
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

        # Web requets
        response = requests.post(
            url=url,
            data=payload,
            headers=http_headers,
            timeout=10
        )

        # DataFrame
        response_data = response.json()
        records = json.loads(response_data['d'])
        df = pandas.DataFrame.from_records(records)
        self._df_not_empty(
            df=df,
            error_str='No records found between the specified start and end dates'
        )
        df = df[::-1].reset_index(drop=True)
        date_col = 'Date' if price_type == 'TRI' else 'HistoricalDate'
        df[date_col] = pandas.to_datetime(
            arg=df[date_col],
            format='%d %b %Y'
        ).dt.date

        return df

    def _df_date_to_csv(
        self,
        df: pandas.DataFrame,
        csv_file: str,
        date_cols: typing.Optional[list[str]] = None
    ) -> None:
        '''
        Modify the specified date columns in the DataFrame and write the resulting DataFrame to a CSV file.
        '''

        copy_df = df.copy()
        if date_cols is not None:
            for col in date_cols:
                copy_df[col] = pandas.to_datetime(
                    arg=copy_df[col],
                    dayfirst=True
                )
        copy_df.to_csv(
            path_or_buf=csv_file,
            index=False,
            date_format=self._date_str_fmt
        )

        return None

    def _csv_date_format(
        self,
        csv_file: str,
        date_cols: typing.Optional[list[str]] = None
    ) -> pandas.DataFrame:
        '''
        Read the input CSV file and convert the specified date columns to ``datetime.date``.
        '''

        # Read DataFrame
        df = pandas.read_csv(
            filepath_or_buffer=csv_file
        )

        # Date column processing
        if date_cols is not None:
            for col in date_cols:
                df[col] = pandas.to_datetime(
                    arg=df[col],
                    format=self._date_str_fmt
                ).dt.date

        return df

    def _df_tri_monthly_open_close(
        self,
        df: pandas.DataFrame,
        start_date: datetime.date,
        end_date: datetime.date
    ) -> pandas.DataFrame:
        '''
        Compute the first date of each month between the start and end dates,
        along with the corresponding monthly open and close values from
        historical daily data.
        '''

        # Monthly start dates
        ms_dates = pandas.date_range(
            start=start_date,
            end=end_date,
            freq='MS'
        ).date.tolist()

        # DataFrame of monthly open close value
        month_df = pandas.DataFrame()
        for idx, dates in enumerate(zip(ms_dates[:-1], ms_dates[1:])):
            idx_df = df[(df['Date'] >= dates[0]) & (df['Date'] < dates[1])]
            month_df.loc[idx, 'Date'] = idx_df.iloc[0, 0]
            month_df.loc[idx, 'Open'] = idx_df.iloc[0, 1]
            month_df.loc[idx, 'Close'] = idx_df.iloc[-1, -1]

        return month_df

    def _df_cagr_column(
        self,
        df: pandas.DataFrame
    ) -> pandas.DataFrame:
        '''
        Compute CAGR(%) column from Base Date, Base Value, Close Date, and Close Value columns.
        '''

        # DataFrame processing
        df['YMD_diff'] = df.apply(
            lambda row: dateutil.relativedelta.relativedelta(row['Close Date'], row['Base Date']),
            axis=1
        )
        df['Years'] = df.apply(
            lambda row: row['YMD_diff'].years,
            axis=1
        )
        df['Months'] = df.apply(
            lambda row: row['YMD_diff'].months,
            axis=1
        )
        df['Days'] = df.apply(
            lambda row: row['YMD_diff'].days,
            axis=1
        )
        df['Y-M-D'] = df.apply(
            lambda row: f'{row['Years']:02d}Y-{row['Months']:02d}M-{row['Days']:02d}D',
            axis=1
        )
        df['tot_years'] = df['Years'] + (df['Months'] / 12) + (df['Days'] / 365)
        df['CAGR(%)'] = 100 * (pow(df['Close Value'] / df['Base Value'], 1 / df['tot_years']) - 1)

        return df

    def _validate_same_end_date_in_dfs(
        self,
        indices: list[str],
        dir_path: str,
    ) -> list[pandas.DataFrame]:
        '''
        Validate that all index CSV files share the same end date.
        '''

        dfs = [
            self._csv_date_format(
                csv_file=os.path.join(dir_path, f'{index}.csv'),
                date_cols=['Date']
            ) for index in indices
        ]

        # Check equal end date for all DataFrames
        close_date = dfs[0]['Date'].iloc[-1]
        for index, df in zip(indices, dfs):
            if df['Date'].iloc[-1] != close_date:
                raise ValueError(
                    f'Mismatch of end date for the index "{index}" with others'
                )

        return dfs

    def _cagr_sort(
        self,
        df: pandas.DataFrame
    ) -> pandas.DataFrame:
        '''
        Sort DataFrame by the CAGR column
        '''

        df = df.sort_values(
            by=['CAGR(%)'],
            ascending=[False]
        ).reset_index(drop=True)
        df = df.drop(
            columns=['ID', 'YMD_diff', 'Years', 'Months', 'Days', 'tot_years']
        )

        return df

    def _cagr_sort_within_category(
        self,
        df: pandas.DataFrame
    ) -> pandas.DataFrame:
        '''
        Sort DataFrame by the CAGR column within category
        '''

        df = df.groupby(
            by='Category',
            sort=False,
            group_keys=True
        ).apply(
            lambda x: x.sort_values(
                by=['CAGR(%)'],
                ascending=[False]
            )
        )
        df = df.reset_index()
        df = df.drop(
            columns=['ID', 'level_1', 'YMD_diff', 'Years', 'Months', 'Days', 'tot_years']
        )

        return df

    def _indices_metric_comparison(
        self,
        indices: list[str],
        dfs: list[pandas.DataFrame],
        remove_cols: list[str],
        common_cols: list[str],
        rename_col: str,
        excel_file: str,
        sheet_names: list[str]
    ) -> pandas.DataFrame:
        '''
        Compare year-wise performance metrics and growth multiples across indices,
        and assign scores based on their relative performance.
        '''

        # Filtered DataFrames based on common year
        common_year = min(
            map(lambda df: int(df['Year'].max()), dfs)
        )
        dfs = [
            df[df['Year'] <= common_year] for df in dfs
        ]
        dfs = [
            df.drop(columns=remove_cols) for df in dfs
        ]

        # CAGR DataFrame of indices
        metric_dfs = [
            df.drop(columns=['Multiple(X)']) for df in dfs
        ]
        metric_dfs = [
            df.rename(columns={rename_col: f'{index}'}) for df, index in zip(metric_dfs, indices)
        ]
        metric_df = metric_dfs[0]
        for df in metric_dfs[1:]:
            metric_df = pandas.merge(
                left=metric_df,
                right=df,
                on=common_cols,
                how='inner'
            )

        # Growth DataFrame of investment
        growth_dfs = [
            df.drop(columns=[rename_col]) for df in dfs
        ]
        growth_dfs = [
            df.rename(columns={'Multiple(X)': f'{index}'}) for df, index in zip(growth_dfs, indices)
        ]
        growth_df = growth_dfs[0]
        for df in growth_dfs[1:]:
            growth_df = pandas.merge(
                left=growth_df,
                right=df,
                on=common_cols,
                how='inner'
            )

        # Rounding of column values to catch exact maximum and minimum with floating point precision
        for index in indices:
            metric_df[index] = metric_df[index].round(5)
            growth_df[index] = growth_df[index].round(5)

        # Score DataFrame based on growth multiple
        score_df = growth_df.copy()
        for idx, row in growth_df.iterrows():
            sort_growth = row.iloc[len(common_cols):].sort_values().index
            score_df.loc[idx, sort_growth] = range(1, len(indices) + 1)
        score_df = score_df.iloc[:, len(common_cols):]

        # Rank DataFrame of total score
        rank_df = score_df.sum().sort_values(ascending=False).reset_index()
        rank_df.columns = ['Index Name', 'Score']

        # Arrange DataFrame accoring to score
        metric_df = metric_df[common_cols + rank_df['Index Name'].tolist()]
        growth_df = growth_df[common_cols + rank_df['Index Name'].tolist()]

        # Saving DataFrames
        with pandas.ExcelWriter(
            path=excel_file,
            engine='xlsxwriter'
        ) as excel_writer:
            # Writing rank DataFrame
            rank_df.to_excel(
                excel_writer=excel_writer,
                index=False,
                sheet_name='Score'
            )
            workbook = excel_writer.book
            worksheet = excel_writer.sheets['Score']
            header_format = workbook.add_format(
                {'bold': True, 'align': 'center'}
            )
            worksheet.set_column(0, 0, 75)
            worksheet.set_column(1, 1, 15)
            for idx, col in enumerate(rank_df.columns):
                worksheet.write(0, idx, col, header_format)
            # Writing CAGR and Growth DataFrames
            header_format = workbook.add_format(
                {
                    'bold': True,
                    'text_wrap': True,
                    'align': 'center',
                    'valign': 'vcenter'
                }
            )
            for df, sheet in zip([metric_df, growth_df], sheet_names):
                df.to_excel(
                    excel_writer=excel_writer,
                    index=False,
                    sheet_name=sheet
                )
                workbook = excel_writer.book
                worksheet = excel_writer.sheets[sheet]
                worksheet.set_column(
                    0, len(common_cols) - 1, 15
                )
                worksheet.set_column(
                    len(common_cols), df.shape[1] - 1, 15,
                    workbook.add_format({'num_format': '#,##0.0'})
                )
                for idx, col in enumerate(df.columns):
                    worksheet.write(0, idx, col, header_format)
                # Coloring maximum and minimum value cells in each row
                for row in range(df.shape[0]):
                    # minimum value
                    worksheet.conditional_format(
                        row + 1, len(common_cols), row + 1, df.shape[1] - 1,
                        {
                            'type': 'cell',
                            'criteria': 'equal to',
                            'value': df.iloc[row, len(common_cols):].min(),
                            'format': workbook.add_format({'bg_color': '#F4A460'})
                        }
                    )
                    # maximim value
                    worksheet.conditional_format(
                        row + 1, len(common_cols), row + 1, df.shape[1] - 1,
                        {
                            'type': 'cell',
                            'criteria': 'equal to',
                            'value': df.iloc[row, len(common_cols):].max(),
                            'format': workbook.add_format({'bg_color': '#ADFF2F'})
                        }
                    )

        return rank_df
