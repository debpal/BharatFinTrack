import pandas
import typing
from .helper import Helper


class NSEProduct:
    '''
    Provides functionality for accessing the characteristics of
    NSE related financial products.
    '''

    def equity_base_parameter_midf(
        self,
        excel_file: str
    ) -> pandas.DataFrame:
        '''
        Generate a MultiIndex DataFrame containing the base parameters
        of equity indices and save it to an Excel file.

        Parameters
        ----------
        excel_file : str
            Path to the Excel file where the DataFrame will be saved.

        Returns
        -------
        DataFrame
            A MultiIndex DataFrame containing the base parameters
            (identifier, start date, and base value) of the available equity indices.
        '''

        # Check static type of input variable origin
        Helper()._validate_variable_origin_static_type(
            vars_types=typing.get_type_hints(
                obj=self.equity_base_parameter_midf
            ),
            vars_values=locals()
        )

        # Validate file path
        Helper()._validate_file_path(
            input_file=excel_file,
            input_ext='.xlsx'
        )

        # Save the multi-index DataFrame
        df = Helper()._equity_base_midf
        df = df[df.columns[:3]]
        df['Base Date'] = df['Base Date'].apply(lambda x: x.date())
        with pandas.ExcelWriter(path=excel_file, engine='xlsxwriter') as excel_writer:
            df.to_excel(
                excel_writer=excel_writer,
                index=True
            )
            # Column cell value formatting
            workbook = excel_writer.book
            worksheet = excel_writer.sheets['Sheet1']
            worksheet.set_column(
                0, 1, 12,
                workbook.add_format({'align': 'center', 'valign': 'vcenter'})
            )
            worksheet.set_column(
                2, 2, 60,
                workbook.add_format({'align': 'left'})
            )
            worksheet.set_column(
                3, 4, 12,
                workbook.add_format({'align': 'right'})
            )
            # Column header formatting
            header_names = list(df.index.names) + list(df.columns)
            header_format = workbook.add_format(
                {'bold': True, 'align': 'center'}
            )
            for idx, col in enumerate(header_names):
                worksheet.write(0, idx, col, header_format)

        return df

    def equity_categorical_indices(
        self,
        category: str
    ) -> list[str]:
        '''
        Return the equity index identifiers for a specified category.

        Parameters
        ----------
        category : str
            Equity index category. Must be one of:
            ``broad``, ``sector``, ``thematic``, or ``strategy``.

        Returns
        -------
        list
            List of equity index identifiers corresponding to the specified category.
        '''

        # Check static type of input variable origin
        Helper()._validate_variable_origin_static_type(
            vars_types=typing.get_type_hints(
                obj=self.equity_categorical_indices
            ),
            vars_values=locals()
        )

        # DataFrame of index base parameters
        df = Helper()._equity_base_midf.reset_index()

        # List of category
        valid_category = list(df['Category'].unique())

        # Validate input category
        if category not in valid_category:
            raise ValueError(
                f'Invalid category "{category}"; must be one of {valid_category}'
            )

        # List of category indices
        category_index = df[df['Category'] == category]['Index Name']
        output = list(category_index.sort_values())

        return output

    def equity_index_base_parameters(
        self,
        index: str
    ) -> pandas.DataFrame:
        '''
        Return a DataFrame of base parameters for a specified equity index.

        Parameters
        ----------
        index : str
            Name of the index.

        Returns
        -------
        DataFrame
            DataFrame of base parameters for the specified equity index
        '''

        # Check static type of input variable origin
        Helper()._validate_variable_origin_static_type(
            vars_types=typing.get_type_hints(
                obj=self.equity_index_base_parameters
            ),
            vars_values=locals()
        )

        # DataFrame of index base parameters
        df = Helper()._equity_index_base_param(
            index=index,
            check_open_source=False
        )
        df = df.drop(
            columns=['API TRI']
        )

        return df
