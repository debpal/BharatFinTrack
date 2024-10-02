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
    Download and analyze NSE index price data.
    '''

    def all_equity_index_cagr_from_inception(
        self,
        excel_file: str,
        http_headers: typing.Optional[dict[str, str]] = None
    ) -> pandas.DataFrame:

        '''
        Returns a DataFrame with the CAGR(%) of all NSE equity indices
        (excluding dividend reinvestment) from inception.

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
            A multi-index DataFrame with the CAGR(%) for all NSE equity indices from inception,
            sorted in descending order by CAGR(%) within each index category.
        '''

        # web request headers
        headers = Core().default_http_headers if http_headers is None else http_headers

        # download data
        main_url = 'https://www.niftyindices.com'
        csv_url = main_url + '/reports/daily-reports'
        response = requests.get(csv_url, headers=headers)
        soup = bs4.BeautifulSoup(response.content, 'html.parser')
        for anchor in soup.find_all('a'):
            if anchor['href'].endswith('.csv') and anchor['id'] == 'dailysnapOneDaybefore':
                csv_link = main_url + anchor['href']
            else:
                pass
        response = requests.get(csv_link, headers=headers)
        with tempfile.TemporaryDirectory() as tmp_dir:
            daily_file = os.path.join(tmp_dir, 'daily.csv')
            with open(daily_file, 'wb') as daily_data:
                daily_data.write(response.content)
            daily_df = pandas.read_csv(daily_file)

        # processing downloaded data
        date_string = datetime.datetime.strptime(
            daily_df.loc[0, 'Index Date'], '%d-%m-%Y'
        )
        daily_date = date_string.date()
        daily_df = daily_df[['Index Name', 'Index Date', 'Closing Index Value']]
        daily_df.columns = ['Index Name', 'Date', 'Close']
        daily_df['Index Name'] = daily_df['Index Name'].apply(lambda x: x.upper())
        exclude_word = [
            'G-SEC',
            '1D RATE',
            'INDIA VIX',
            'DIVIDEND POINTS'
        ]
        exclude_index = daily_df['Index Name'].apply(
            lambda x: any(word in x for word in exclude_word)
        )
        daily_df = daily_df[~exclude_index].reset_index(drop=True)
        daily_df['Date'] = daily_date

        # processing base DataFrame
        base_df = NSEProduct()._dataframe_equity_index
        base_df = base_df.reset_index()
        category = list(base_df['Category'].unique())
        base_df = base_df.drop(columns=['ID', 'API TRI'])
        base_df['Base Date'] = base_df['Base Date'].apply(lambda x: x.date())

        # checking absent indices in both files
        base_unmatch = {
            'NIFTY 50 FUTURES INDEX': 'NIFTY 50 FUTURES PR',
            'NIFTY 50 FUTURES TR INDEX': 'NIFTY 50 FUTURES TR',
            'NIFTY HEALTHCARE INDEX': 'NIFTY HEALTHCARE'
        }
        daily_df['Index Name'] = daily_df['Index Name'].apply(
            lambda x: base_unmatch.get(x, x)
        )
        # base_index = base_df['Index Name']
        # daily_index = daily_df['Index Name']
        # unavailable_base = list(base_index[~base_index.isin(daily_index)])
        # print(f'Base indices {unavailable_base} are not available in daily indices.')
        # unavailable_daily = list(daily_index[~daily_index.isin(base_index)])
        # print(f'Daily indices {unavailable_daily} are not available in base indices.')

        # merging data
        cagr_df = base_df.merge(daily_df)
        cagr_df['Return(1 INR)'] = (cagr_df['Close'] / cagr_df['Base Value']).round(2)
        cagr_df['Years'] = list(
            map(
                lambda x: dateutil.relativedelta.relativedelta(daily_date, x).years, cagr_df['Base Date']
            )
        )
        cagr_df['Days'] = list(
            map(
                lambda x, y: (daily_date - x.replace(year=x.year + y)).days, cagr_df['Base Date'], cagr_df['Years']
            )
        )
        total_years = cagr_df['Years'] + (cagr_df['Days'] / 365)
        cagr_df['CAGR(%)'] = 100 * (pow(cagr_df['Close'] / cagr_df['Base Value'], 1 / total_years) - 1)

        # Convert 'Category' column to categorical data types with a defined order
        cagr_df['Category'] = pandas.Categorical(
            cagr_df['Category'],
            categories=category,
            ordered=True
        )

        # Sort the dataframe
        cagr_df = cagr_df.sort_values(
            by=['Category', 'CAGR(%)', 'Years', 'Days'],
            ascending=[True, False, False, False]
        )

        # output
        dfs_category = map(lambda x: cagr_df[cagr_df['Category'] == x], category)
        dataframes = list(
            map(
                lambda x: x.drop(columns=['Category']).reset_index(drop=True), dfs_category
            )
        )
        output = pandas.concat(
            dataframes,
            keys=[word.upper() for word in category],
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
                worksheet.set_column(index_cols, index_cols, 60)
                worksheet.set_column(index_cols + 1, index_cols + output.shape[1] - 2, 15)
                worksheet.set_column(
                    index_cols + output.shape[1] - 1,
                    index_cols + output.shape[1] - 1, 15,
                    workbook.add_format({'num_format': '#,##0.0'})
                )
                # Dataframe colors
                get_colormap = matplotlib.colormaps.get_cmap('Pastel2')
                colors = [
                    get_colormap(count / len(category)) for count in range(len(category))
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
