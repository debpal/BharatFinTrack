import requests
import pandas
import io
import os
import json
import typing
import datetime
from .helper import Helper


class NPS:
    '''
    Provide functionalities to download National Pension Scheme (NPS) data,
    parse the raw files, and perform analytical operations.
    '''

    def _base_df_to_excel(
        self,
        df: pandas.DataFrame,
        excel_file: str
    ) -> None:
        '''
        Write the NPS base parameters DataFrame to an Excel file.
        '''

        # Check static type of input variable origin
        Helper()._validate_variable_origin_static_type(
            vars_types=typing.get_type_hints(
                obj=self._base_df_to_excel
            ),
            vars_values=locals()
        )

        # Validate output file path
        Helper()._validate_file_path(
            input_file=excel_file,
            input_ext='.xlsx'
        )

        # Write base parameter DataFrame to an Excel file
        with pandas.ExcelWriter(excel_file) as excel_writer:
            df.to_excel(excel_writer, index=False)
            workbook = excel_writer.book
            worksheet = excel_writer.sheets['Sheet1']
            col_format = workbook.add_format(
                {'align': 'left'}
            )
            worksheet.set_column(0, 0, 50, col_format)
            worksheet.set_column(1, 1, 120, col_format)
            worksheet.set_column(2, 2, 15, col_format)
            header_format = workbook.add_format(
                {'bold': True, 'align': 'center'}
            )
            for idx, col in enumerate(df.columns):
                worksheet.write(0, idx, col, header_format)

        return None

    def _download_base_parameters(
        self
    ) -> pandas.DataFrame:
        '''
        Download, clean, and return the latest NPS base parameters DataFrame.
        '''

        # Download data and convert to string representation
        url = "https://npstrust.org.in/nav-report-excel"
        response = requests.get(
            url=url
        )
        content = response.content.decode('utf-8')

        # DataFrame processing
        df = pandas.read_csv(
            filepath_or_buffer=io.StringIO(content),
            sep='\t'
        )
        df = df.drop(
            columns=[
                'ID',
                'DATE OF NAV',
                'NAV VALUE'
            ]
        )
        df = df.rename(
            columns={
                'PFM NAME': 'PFM',
                'SCHEME NAME': 'SCHEME',
                'SCHEME ID': 'ID'
            }
        )
        df = df[['PFM', 'SCHEME', 'ID']]

        # Writing Dataframe
        excel_file = os.path.join(
            os.path.dirname(__file__), 'base_data', 'base_nps.xlsx'
        )
        self._base_df_to_excel(
            df=df,
            excel_file=excel_file
        )

        return df

    def base_df(
        self,
        excel_file: typing.Optional[str] = None
    ) -> pandas.DataFrame:
        '''
        Get the NPS base parameters DataFrame.

        Parameters
        ----------
        excel_file : str, optional
            Path to an Excel file to save the DataFrame.

        Returns
        -------
        DataFrame
            A DataFrame containing Pension Fund Manager names,
            scheme names, and their corresponding identifiers.
        '''

        # Check static type of input variable origin
        Helper()._validate_variable_origin_static_type(
            vars_types=typing.get_type_hints(
                obj=self.base_df
            ),
            vars_values=locals()
        )

        file_path = os.path.join(
            os.path.dirname(__file__), 'base_data', 'base_nps.xlsx'
        )

        df = pandas.read_excel(
            io=file_path
        )

        if excel_file is not None:
            self._base_df_to_excel(
                df=df,
                excel_file=excel_file
            )

        return df

    @property
    def pfm(
        self
    ) -> pandas.Series:
        '''
        Return a Series of all available Pension Fund Manager names.
        '''

        df = self.base_df()

        pfm = df['PFM'].unique()

        return pfm

    def pfm_schemes(
        self,
        pfm_name: str
    ) -> str:
        '''
        Return scheme names and corresponding identifiers for a given Pension Fund Manager.

        Parameters
        ----------
        pfm_name : str
            Name of the Pension Fund Manager, typically obtained
            from :attr:`BharatFinTrack.NPS.pfm`.

        Returns
        -------
        str
            A JSON-formatted string dictionary where keys are scheme names and values
            are their corresponding NPS identifiers.
        '''

        df = self.base_df()

        if pfm_name not in df['PFM'].tolist():
            pfm_valid = json.dumps(
                obj=df['PFM'].unique().tolist(),
                indent=4
            )
            raise ValueError(
                f'Invalid name: {pfm_name}\n'
                '\nThe list of valid names is:\n'
                f'{pfm_valid}'
            )

        df = df[df['PFM'].isin([pfm_name])]
        df = df.drop(columns=['PFM']).reset_index(drop=True)

        scheme_id = json.dumps(
            obj=dict(zip(df['SCHEME'], df['ID'])),
            indent=4
        )

        return scheme_id

    def scheme_nav(
        self,
        scheme_ids: typing.Optional[list[str]] = None,
        excel_file: typing.Optional[str] = None
    ) -> pandas.DataFrame:
        '''
        Fetch the Net Asset Value (NAV) history for the specified NPS schemes.

        Parameters
        ----------
        scheme_ids : list, optional
            A list of scheme identifiers, typically obtained from :meth:`BharatFinTrack.NPS.pfm_schemes`.
            If None (default), the NAV data for all available schemes is retrieved.

        excel_file : str, optional
            Path to an Excel file to save the output DataFrame.

        Returns
        -------
        DataFrame
            A DataFrame containing scheme names, identifiers, and their corresponding NAV dates and values.
        '''

        # Download data and convert to string representation
        url = "https://npstrust.org.in/nav-report-excel"
        response = requests.get(
            url=url
        )
        content = response.content.decode('utf-8')

        # DataFrame processing
        df = pandas.read_csv(
            filepath_or_buffer=io.StringIO(content),
            sep='\t'
        )

        select_cols = [
            'SCHEME NAME',
            'SCHEME ID',
            'DATE OF NAV',
            'NAV VALUE'
        ]
        df = df[select_cols]

        df.columns = [
            'SCHEME',
            'ID',
            'DATE',
            'NAV'
        ]

        if scheme_ids is not None:
            df = df[df['ID'].isin(values=scheme_ids)].reset_index(drop=True)

        df['DATE'] = df['DATE'].apply(
            lambda x: datetime.datetime.strptime(x, '%Y-%m-%d').date()
        )

        # Writing DataFrame
        if excel_file is not None:
            Helper()._validate_file_path(
                input_file=excel_file,
                input_ext='.xlsx'
            )
            with pandas.ExcelWriter(excel_file) as excel_writer:
                df.to_excel(excel_writer, index=False)
                workbook = excel_writer.book
                worksheet = excel_writer.sheets['Sheet1']
                worksheet.set_column(0, 0, 50, workbook.add_format({'align': 'left'}))
                worksheet.set_column(1, 3, 15)
                header_format = workbook.add_format(
                    {'bold': True, 'align': 'center'}
                )
                for idx, col in enumerate(df.columns):
                    worksheet.write(0, idx, col, header_format)

        return df
