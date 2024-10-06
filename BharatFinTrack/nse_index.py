import os
import tempfile
import typing
import datetime
import dateutil.relativedelta
import pandas
import requests
import bs4
import matplotlib
from .nse_product import NSEProduct
from .core import Core


class NSEIndex:

    '''
    Download and analyze NSE index price data
    (excluding dividend reinvestment).
    '''

    def download_daily_summary_report(
        self,
        folder_path: str,
        http_headers: typing.Optional[dict[str, str]] = None
    ) -> pandas.DataFrame:

        '''
        Download the daily summary for all NSE indices and save it as the
        'daily_summary_report.csv' file in the specified folder path.

        Parameters
        ----------
        folder_path: str
            Folder path to save the CSV file of the daily summary for all NSE indices.

        http_headers : dict, optional
            HTTP headers for the web request. Defaults to
            :attr:`BharatFinTrack.core.Core.default_http_headers` if not provided.

        Returns
        -------
        DataFrame
            A DataFrame containing the daily summary for all NSE indices.
        '''

        # web request headers
        headers = Core().default_http_headers if http_headers is None else http_headers

        # download data
        main_url = 'https://www.niftyindices.com'
        csv_url = main_url + '/reports/daily-reports'
        response = requests.get(
            url=csv_url,
            headers=headers,
            timeout=30
        )
        soup = bs4.BeautifulSoup(
            markup=response.content,
            features='html.parser'
        )
        for anchor in soup.find_all('a'):
            if anchor['href'].endswith('.csv') and anchor['id'] == 'dailysnapOneDaybefore':
                csv_link = main_url + anchor['href']
                response = requests.get(
                    url=csv_link,
                    headers=headers
                )
                if os.path.isdir(folder_path):
                    download_file = os.path.join(folder_path, 'daily_summary_report.csv')
                    with open(download_file, 'wb') as download_data:
                        download_data.write(response.content)
                    output = pandas.read_csv(download_file)
                else:
                    raise Exception('The folder path does not exist.')
            else:
                pass

        return output

    def equity_cagr_from_launch(
        self,
        http_headers: typing.Optional[dict[str, str]] = None,
        untracked_indices: bool = False
    ) -> pandas.DataFrame:

        '''
        Returns the CAGR (%) since launch for all NSE equity indices.

        Parameters
        ----------
        http_headers : dict, optional
            HTTP headers for the web request. Defaults to
            :attr:`BharatFinTrack.core.Core.default_http_headers` if not provided.

        untracked_indices : bool, optional
            Defaults to False. If True, print two lists of untracked indices
            from downloaded and based files.

        Returns
        -------
        DataFrame
            A DataFrame with the CAGR (%) since launch for all NSE equity indices.
        '''

        # downlod daily summary of NSE indices
        with tempfile.TemporaryDirectory() as tmp_dir:
            download_df = self.download_daily_summary_report(tmp_dir)

        # processing downloaded data
        date_string = datetime.datetime.strptime(
            download_df.loc[0, 'Index Date'], '%d-%m-%Y'
        )
        download_date = date_string.date()
        download_df = download_df[
            ['Index Name', 'Index Date', 'Closing Index Value']
        ]
        download_df.columns = ['Index Name', 'Close Date', 'Close Value']
        download_df['Index Name'] = download_df['Index Name'].apply(lambda x: x.upper())
        download_df['Close Date'] = download_date

        # processing base DataFrame
        base_df = NSEProduct()._dataframe_equity_index
        base_df = base_df.reset_index()
        base_df = base_df.drop(columns=['ID', 'API TRI'])
        base_df['Base Date'] = base_df['Base Date'].apply(lambda x: x.date())

        # fixing unmatched indices with base indinces in the download Dataframe
        download_unmatch = {
            'NIFTY 50 FUTURES INDEX': 'NIFTY 50 FUTURES PR',
            'NIFTY 50 FUTURES TR INDEX': 'NIFTY 50 FUTURES TR',
            'NIFTY HEALTHCARE INDEX': 'NIFTY HEALTHCARE'
        }
        download_df['Index Name'] = download_df['Index Name'].apply(
            lambda x: download_unmatch.get(x, x)
        )

        # computing CAGR(%)
        cagr_df = base_df.merge(download_df)
        cagr_df['Close/Base'] = cagr_df['Close Value'] / cagr_df['Base Value']
        cagr_df['Years'] = list(
            map(
                lambda x: dateutil.relativedelta.relativedelta(download_date, x).years, cagr_df['Base Date']
            )
        )
        cagr_df['Days'] = list(
            map(
                lambda x, y: (download_date - x.replace(year=x.year + y)).days, cagr_df['Base Date'], cagr_df['Years']
            )
        )
        total_years = cagr_df['Years'] + (cagr_df['Days'] / 365)
        cagr_df['CAGR(%)'] = 100 * (pow(cagr_df['Close Value'] / cagr_df['Base Value'], 1 / total_years) - 1)

        # output
        if untracked_indices is False:
            pass
        else:
            download_index = download_df['Index Name']
            base_index = base_df['Index Name']
            untracked_download = list(download_index[~download_index.isin(base_index)])
            print(f'List of untracked download indices: {untracked_download}')
            untracked_base = list(base_index[~base_index.isin(download_index)])
            print(f'List of untracked base indices: {untracked_base}')

        return cagr_df

    def sort_equity_cagr_from_launch(
        self,
        excel_file: str,
        http_headers: typing.Optional[dict[str, str]] = None
    ) -> pandas.DataFrame:

        '''
        Returns equity indices sorted in descending order by CAGR (%) since launch.

        Parameters
        ----------
        excel_file : str
            Path to an Excel file to save the DataFrame.

        http_headers : dict, optional
            HTTP headers for the web request. Defaults to
            :attr:`BharatFinTrack.core.Core.default_http_headers` if not provided.

        Returns
        -------
        DataFrame
            A DataFrame sorted in descending order by CAGR (%) since launch for all NSE equity indices.
        '''

        # DataFrame of CAGR(%)
        cagr_df = self.equity_cagr_from_launch(
            http_headers=http_headers,
            untracked_indices=False
        )

        # sorting DataFrame by CAGR(%)
        cagr_df = cagr_df.drop(columns=['Category'])
        cagr_df = cagr_df.sort_values(
            by=['CAGR(%)', 'Years', 'Days'],
            ascending=[False, False, False]
        )
        output = cagr_df.reset_index(drop=True)

        # saving DataFrame
        excel_ext = Core()._excel_file_extension(excel_file)
        if excel_ext != '.xlsx':
            raise Exception(
                f'Input file extension "{excel_ext}" does not match the required ".xlsx".'
            )
        else:
            with pandas.ExcelWriter(excel_file, engine='xlsxwriter') as excel_writer:
                output.to_excel(excel_writer, index=False)
                workbook = excel_writer.book
                worksheet = excel_writer.sheets['Sheet1']
                # format columns
                for col_num, col_df in enumerate(output.columns):
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

        return output

    def category_sort_equity_cagr_from_launch(
        self,
        excel_file: str,
        http_headers: typing.Optional[dict[str, str]] = None
    ) -> pandas.DataFrame:

        '''
        Returns equity indices sorted in descending order by CAGR (%)
        since launch within each index category.

        Parameters
        ----------
        excel_file : str
            Path to an Excel file to save the DataFrame.

        http_headers : dict, optional
            HTTP headers for the web request. Defaults to
            :attr:`BharatFinTrack.core.Core.default_http_headers` if not provided.

        Returns
        -------
        DataFrame
            A multi-index DataFrame sorted in descending order by CAGR (%)
            since launch within each index category.
        '''

        # DataFrame of CAGR(%)
        cagr_df = self.equity_cagr_from_launch(
            http_headers=http_headers
        )

        # Convert 'Category' column to categorical data types with a defined order
        categories = list(cagr_df['Category'].unique())
        cagr_df['Category'] = pandas.Categorical(
            cagr_df['Category'],
            categories=categories,
            ordered=True
        )

        # Sorting Dataframe
        cagr_df = cagr_df.sort_values(
            by=['Category', 'CAGR(%)', 'Years', 'Days'],
            ascending=[True, False, False, False]
        )
        dataframes = []
        for category in categories:
            category_df = cagr_df[cagr_df['Category'] == category]
            category_df = category_df.drop(columns=['Category']).reset_index(drop=True)
            dataframes.append(category_df)
        output = pandas.concat(
            dataframes,
            keys=[word.upper() for word in categories],
            names=['Category', 'ID']
        )

        # saving the DataFrame
        excel_ext = Core()._excel_file_extension(excel_file)
        if excel_ext != '.xlsx':
            raise Exception(
                f'Input file extension "{excel_ext}" does not match the required ".xlsx".'
            )
        else:
            with pandas.ExcelWriter(excel_file, engine='xlsxwriter') as excel_writer:
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