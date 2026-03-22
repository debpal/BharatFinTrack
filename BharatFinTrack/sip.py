import pandas
import pyxirr
import typing
import os
from .helper import Helper


class SIP:
    '''
    Provide functionalities for computing and analyzing Systematic Investment Plan (SIP).
    '''

    def index_return_from_given_date(
        self,
        csv_file: str,
        yr_mon: typing.Optional[tuple[int, int]] = None,
        invest: int = 1000
    ) -> pandas.Series:
        '''
        Compute the closing value, growth multiple, and annualized XIRR (%) of a fixed
        monthly SIP starting from a specified date, assuming investments are made on
        the first available trading date of each month.

        Parameters
        ----------
        csv_file : str
            Path to the CSV file obtained from :meth:`BharatFinTrack.NSETRI.download_daily_data`
            and :meth:`BharatFinTrack.NSETRI.update_daily_data` methods.

        yr_mon : tuple, optional
            Tuple containing the year and month (1–12), respectively, from which the SIP investment begins.

        invest : int, optional
            Fixed investment amount contributed on the first date of each month. Default is 1000.

        Returns
        -------
        Series
            Series containing the closing value, growth multiple, and annualized
            XIRR (%) for the SIP investment starting from the specified date.
        '''

        # Check static type of input variable origin
        Helper()._validate_variable_origin_static_type(
            vars_types=typing.get_type_hints(
                obj=self.index_return_from_given_date
            ),
            vars_values=locals()
        )

        # Read DataFrame
        df = Helper()._csv_date_format(
            csv_file=csv_file,
            date_cols=['Date']
        )

        # Date from year and month
        if yr_mon is not None:
            ym_date = df['Date'].iloc[0].replace(
                year=yr_mon[0],
                month=yr_mon[1],
                day=1
            )

        # Start and end dates
        min_date = df['Date'].min()
        start_date = ym_date if yr_mon is not None else min_date
        end_date = df['Date'].max()
        if not min_date <= start_date <= end_date:
            raise ValueError(
                f'SIP start date {start_date.strftime(Helper()._date_str_fmt)} '
                'is outside the CSV date range '
                f'({min_date.strftime(Helper()._date_str_fmt)}, {end_date.strftime(Helper()._date_str_fmt)})'
            )

        # DataFrame of monthly open and close values
        month_df = Helper()._df_tri_monthly_open_close(
            df=df,
            start_date=start_date,
            end_date=end_date
        )

        # Investment return value
        index_divisor = 1000
        month_df['Investment'] = invest
        month_df['Cumulative Investment'] = month_df['Investment'].cumsum()
        open_nav = month_df['Open'] / index_divisor
        month_df['Unit'] = month_df['Investment'] / open_nav
        month_df['Cumulative Unit'] = month_df['Unit'].cumsum()
        close_nav = month_df['Close'] / index_divisor
        month_df['Portfolio Value'] = month_df['Cumulative Unit'] * close_nav
        month_df['Multiple(X)'] = month_df['Portfolio Value'] / month_df['Cumulative Investment']

        # XIRR
        sip_dates = list(month_df['Date']) + [end_date]
        sip_transactions = list(-1 * month_df['Investment']) + [month_df['Portfolio Value'].iloc[-1]]
        xirr = pyxirr.xirr(zip(sip_dates, sip_transactions))

        # SIP investment summary
        summary = month_df.iloc[-1, :]
        summary['XIRR(%)'] = 100 * (xirr if xirr is not None else 0.0)
        summary = summary.drop(
            index=['Open', 'Close', 'Unit', 'Cumulative Unit']
        )
        summary['Date'] = month_df['Date'].iloc[0]
        summary = summary.rename(
            index={
                'Date': 'Start Date',
                'Investment': 'Investment (Monthly)'
            }
        )
        date_diff = Helper()._date_difference(
            start_date=start_date,
            end_date=end_date
        )

        idx1_loc = summary.index.get_loc(
            key='Investment (Monthly)'
        )
        idx2_loc = summary.index.get_loc(
            key='Cumulative Investment'
        )
        summary = pandas.concat(
            [
                summary.iloc[:idx1_loc + 1],
                pandas.Series(
                    {
                        'End Date': end_date,
                        'Duration': f"{date_diff['years']}Y-{date_diff['months']}M-{date_diff['days']}D"
                    }
                ),
                summary.iloc[idx2_loc:]
            ]
        )

        return summary

    def index_yearly_return(
        self,
        csv_file: str,
        invest: int = 1000,
        excel_file: typing.Optional[str] = None
    ) -> pandas.DataFrame:
        '''
        Compute the year-wise closing value, growth multiples, and annualized XIRR (%)
        of a fixed monthly SIP tracking an index, assuming investments are made on the
        first available trading date of each month.

        Parameters
        ----------
        csv_file : str
            Path to the CSV file obtained from :meth:`BharatFinTrack.NSETRI.download_daily_data`
            and :meth:`BharatFinTrack.NSETRI.update_daily_data` methods.

        invest : int
            Fixed investment amount contributed on the first date of each month.

        excel_file : str, optional
            Path to an Excel file to save the output DataFrame. Default is None.

        Returns
        -------
        DataFrame
            DataFrame containing the year-wise closing value, growth multiples,
            and annualized XIRR (%) for the fixed monthly SIP investment.
        '''

        # Check static type of input variable origin
        Helper()._validate_variable_origin_static_type(
            vars_types=typing.get_type_hints(
                obj=self.index_yearly_return
            ),
            vars_values=locals()
        )

        # Read DataFrame
        df = Helper()._csv_date_format(
            csv_file=csv_file,
            date_cols=['Date']
        )

        # Start and end dates
        start_date = df['Date'].min()
        end_date = df['Date'].max()

        # DataFrame of monthly open and close values
        month_df = Helper()._df_tri_monthly_open_close(
            df=df,
            start_date=start_date,
            end_date=end_date
        )

        # Date difference
        date_diff = Helper()._date_difference(
            start_date=month_df['Date'].iloc[0],
            end_date=end_date
        )
        year_diff = date_diff['years']

        # SIP DataFrame
        sip_df = pandas.DataFrame()
        index_divisor = 1000
        for idx in range(year_diff + 1):
            # year-wise SIP investment
            if idx < year_diff:
                sip_year: float = idx + 1
                sip_start = end_date.replace(year=end_date.year - (idx + 1))
                yi_df = month_df[(month_df['Date'] >= sip_start) & (month_df['Date'] < end_date)].reset_index(drop=True)
            else:
                sip_year = year_diff + (date_diff['months'] / 12)
                yi_df = month_df.copy()
            # print(yi_df)
            yi_df['Investment'] = invest
            yi_df['Cumulative Investment'] = yi_df['Investment'].cumsum()
            open_nav = yi_df['Open'] / index_divisor
            yi_df['Unit'] = yi_df['Investment'] / open_nav
            yi_df['Cumulative Unit'] = yi_df['Unit'].cumsum()
            close_nav = yi_df['Close'] / index_divisor
            yi_df['Portfolio Value'] = yi_df['Cumulative Unit'] * close_nav
            # year-wise SIP summary
            sip_df.loc[idx, 'Year'] = sip_year
            sip_df.loc[idx, 'Start Date'] = yi_df.loc[0, 'Date']
            sip_df.loc[idx, 'Investment'] = yi_df['Cumulative Investment'].iloc[-1]
            sip_df.loc[idx, 'Close Date'] = end_date
            sip_df.loc[idx, 'Close Value'] = yi_df['Portfolio Value'].iloc[-1]
            sip_df.loc[idx, 'Multiple(X)'] = sip_df.loc[idx, 'Close Value'] / sip_df.loc[idx, 'Investment']
            sip_dates = list(yi_df['Date']) + [end_date]
            sip_transactions = list(-1 * yi_df['Investment']) + [sip_df.loc[idx, 'Close Value']]
            xirr = pyxirr.xirr(zip(sip_dates, sip_transactions))
            sip_df.loc[idx, 'XIRR(%)'] = 100 * (xirr if xirr is not None else 0.0)

        # Drop duplicates row if any
        sip_df = sip_df.drop_duplicates(ignore_index=True)

        # Saving DataFrame
        if excel_file is not None:
            # Validate output file path
            Helper()._validate_file_path(
                input_file=excel_file,
                input_ext='.xlsx'
            )
            # Write DataFrame to the Excel file
            with pandas.ExcelWriter(
                path=excel_file,
                engine='xlsxwriter'
            ) as excel_writer:
                sip_df.to_excel(
                    excel_writer=excel_writer,
                    index=False
                )
                workbook = excel_writer.book
                worksheet = excel_writer.sheets['Sheet1']
                header_format = workbook.add_format(
                    {
                        'bold': True,
                        'align': 'center'
                    }
                )
                for idx, col in enumerate(sip_df.columns):
                    worksheet.set_column(
                        idx, idx, 15,
                        workbook.add_format({'num_format': '#,##0.0'})
                    )
                    worksheet.write(0, idx, col, header_format)

        return sip_df

    def indices_comparison(
        self,
        indices: list[str],
        dir_path: str,
        excel_file: str,
    ) -> pandas.DataFrame:
        '''
        Generate two DataFrames that compares year-wise XIRR (%) and
        growth multiple (X) on the first date SIP investment of each month across multiple indices.
        The output DataFrame are saved to an Excel file, where the cells with
        the best performance among indices for each year are highlighted in green-yellow,
        and those with the worst performance are highlighted in sandy brown.

        Additionally, a scoring mechanism is implemented for the indices based on their growth values.
        For each year, indices are ranked in ascending order of growth, with the lowest value
        receiving the lowest score (1), and the highest value receiving the highest score.
        The total scores for each index are calculated by summing their yearly scores.
        Indices are then sorted in descending order based on their total scores,
        and the results are converted into a DataFrame with columns 'Index Name' and 'Score'.

        Parameters
        ----------
        indices : list
            A list of index names to compare in the monthly SIP XIRR (%) and growth multiple (X).

        dir_path : str
            Path to the directory containing CSV files with historical data for each index.
            Each CSV file must be named as ``{index}.csv`` corresponding to the index names
            provided in the ``indices`` list. These files should be obtained from
            :meth:`BharatFinTrack.NSETRI.download_daily_data` and
            :meth:`BharatFinTrack.NSETRI.update_daily_data` methods.

        excel_file : str
            Path to an Excel file to save the output DataFrames.

        Returns
        -------
        DataFrame
            DataFrame containing the index names and their total scores.
        '''

        # Check static type of input variable origin
        Helper()._validate_variable_origin_static_type(
            vars_types=typing.get_type_hints(
                obj=self.indices_comparison
            ),
            vars_values=locals()
        )

        # Validate output file path
        Helper()._validate_file_path(
            input_file=excel_file,
            input_ext='.xlsx'
        )

        # Validate equal close date across all indices
        Helper()._validate_same_end_date_in_dfs(
            indices=indices,
            dir_path=dir_path,
        )

        # Year-wise SIP analysis for all indices
        dfs = [
            self.index_yearly_return(
                csv_file=os.path.join(dir_path, f'{index}.csv')
            ) for index in indices
        ]

        # Compare XIRR and Growth with score
        rank_df = Helper()._indices_metric_comparison(
            indices=indices,
            dfs=dfs,
            remove_cols=[
                'Investment',
                'Close Value'
            ],
            common_cols=[
                'Year',
                'Start Date',
                'Close Date'
            ],
            rename_col='XIRR(%)',
            excel_file=excel_file,
            sheet_names=[
                'XIRR(%)',
                'Growth(X)'
            ]
        )

        return rank_df

    def investment_growth(
        self,
        invest: int,
        frequency: str,
        annual_return: int | float,
        years: int,
        excel_file: typing.Optional[str] = None
    ) -> pandas.DataFrame:

        '''
        Calculate the SIP growth over a specified number of years for a fixed investment amount.

        Parameters
        ----------
        invest : int
            Fixed amount invested at each SIP interval.

        frequency : str
            Frequency of SIP contributions; must be one of
            ``yearly``, ``quarterly``, ``monthly``, and ``weekly``.

        annual_return : float
            Expected annual return rate in percentage.

        years : int
            Total number of years for the SIP investment duration.

        excel_file : str, optional
            Path to an Excel file to save the output DataFrame. Default is None.

        Returns
        -------
        DataFrame
            A DataFrame containing columns for the annual investment,
            closing balance, and cumulative growth over the investment period.
        '''

        # Check static type of input variable origin
        Helper()._validate_variable_origin_static_type(
            vars_types=typing.get_type_hints(
                obj=self.investment_growth
            ),
            vars_values=locals()
        )

        # Time frequency dictionary
        freq_value = {
            'yearly': 1,
            'quarterly': 4,
            'monthly': 12,
            'weekly': 52
        }

        # Check valid time frequency
        if frequency not in freq_value:
            raise KeyError(
                f'Invalid frequency "{frequency}"; choose from [{", ".join(freq_value)}]'
            )

        # CAGR rate for the given time frequency
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
        df['Multiple(X)'] = df['Value'] / df['Invest']

        # Save the DataFrame
        if excel_file is not None:
            # Validate output file path
            Helper()._validate_file_path(
                input_file=excel_file,
                input_ext='.xlsx'
            )
            # Write DataFrame to the Excel file
            with pandas.ExcelWriter(
                path=excel_file,
                engine='xlsxwriter'
            ) as excel_writer:
                df.to_excel(
                    excel_writer=excel_writer,
                    index=False
                )
                workbook = excel_writer.book
                worksheet = excel_writer.sheets['Sheet1']
                header_format = workbook.add_format(
                    {
                        'bold': True,
                        'align': 'center'
                    }
                )
                for idx, col in enumerate(df.columns):
                    worksheet.set_column(
                        idx, idx, 20,
                        workbook.add_format({'num_format': '#,##0.0'})
                    )
                    worksheet.write(0, idx, col, header_format)

        return df
