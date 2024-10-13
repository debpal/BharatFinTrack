import os
import datetime
import pandas
from .core import Core


class NSEProduct:

    '''
    Provides functionality for accessing the characteristics of
    NSE related financial products.
    '''

    @property
    def _dataframe_equity_index(
        self
    ) -> pandas.DataFrame:

        '''
        Returns a multi-index DataFrame containing
        the characteristics of equity indices.
        '''

        file_path = os.path.join(
            os.path.dirname(__file__), 'data', 'equity_indices.xlsx'
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

    def save_dataframe_equity_index_parameters(
        self,
        excel_file: str
    ) -> pandas.DataFrame:

        '''
        Saves a multi-index DataFrame containing the characteristics
        of equity indices to an Excel file.

        Parameters
        ----------
        excel_file : str
            Path of an Excel file to save the multi-index DataFrame.

        Returns
        -------
        DataFrame
            The multi-index DataFrame containing the characteristics of equity indices.
        '''

        # Excel file extension
        excel_ext = Core()._excel_file_extension(
            file_path=excel_file
        )

        # saving the multi-index dataframe
        if excel_ext == '.xlsx':
            df = self._dataframe_equity_index
            df = df[df.columns[:3]]
            df['Base Date'] = df['Base Date'].apply(lambda x: x.date())
            with pandas.ExcelWriter(excel_file, engine='xlsxwriter') as excel_writer:
                df.to_excel(excel_writer, index=True)
                workbook = excel_writer.book
                worksheet = excel_writer.sheets['Sheet1']
                worksheet.set_column(0, 1, 12, workbook.add_format({'align': 'center'}))
                worksheet.set_column(2, 2, 60, workbook.add_format({'align': 'left'}))
                worksheet.set_column(3, 4, 12, workbook.add_format({'align': 'right'}))
        else:
            raise Exception(
                f'Input file extension "{excel_ext}" does not match the required ".xlsx".'
            )

        return df

    @property
    def equity_index_category(
        self
    ) -> list[str]:

        '''
        Returns a list of categories for NSE equity indices.
        '''

        df = self._dataframe_equity_index.reset_index()
        output = list(df['Category'].unique())

        return output

    def get_equity_indices_by_category(
        self,
        category: str
    ) -> list[str]:

        '''
        Returns a list of NSE equity indices for a specified index category.

        Parameters
        ----------
        category : str
            The category of NSE indices.

        Returns
        -------
        list
            A list containing the equity indices for the specified category.
        '''

        if category in self.equity_index_category:
            df = self._dataframe_equity_index.reset_index()
            df = df[df['Category'] == category]
            output = list(df['Index Name'].sort_values())
        else:
            raise Exception(f'Input category "{category}" does not exist.')

        return output

    @property
    def all_equity_indices(
        self
    ) -> list[str]:

        '''
        Returns a list of equity indices for all categories.
        '''

        df = self._dataframe_equity_index
        output = list(df['Index Name'].sort_values())

        return output

    def is_index_exist(
        self,
        index: str
    ) -> bool:

        '''
        Returns whether the index exists in the list of equity indices.

        Parameters
        ----------
        index : str
            Name of the index.

        Returns
        -------
        bool
            True if the index exists, False otherwise.
        '''

        output = index in self.all_equity_indices

        return output

    def get_equity_index_base_date(
        self,
        index: str
    ) -> str:

        '''
        Returns the base date for a specified NSE equity index.

        Parameters
        ----------
        index : str
            Name of the index.

        Returns
        -------
        str
            The base date of the index in 'DD-MMM-YYYY' format.
        '''

        df = self._dataframe_equity_index
        df = df[['Index Name', 'Base Date']]
        df = df[df['Index Name'] == index]

        if df.shape[0] > 0 and isinstance(df.iloc[-1, -1], datetime.datetime):
            output = df.iloc[-1, -1].strftime('%d-%b-%Y')
        else:
            raise Exception(f'"{index}" index does not exist.')

        return output

    def get_equity_index_base_value(
        self,
        index: str
    ) -> float:

        '''
        Returns the base value for a specified NSE equity index.

        Parameters
        ----------
        index : str
            Name of the index.

        Returns
        -------
        float
            The base value of the index.
        '''

        df = self._dataframe_equity_index
        df = df[['Index Name', 'Base Value']]
        df = df[df['Index Name'] == index]

        if df.shape[0] > 0:
            output = float(df.iloc[-1, -1])
        else:
            raise Exception(f'"{index}" index does not exist.')

        return output
