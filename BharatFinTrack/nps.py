import requests
import pandas
import io
import os
import json


class NPS:
    '''
    Provide functionalities to download National Pension Scheme (NPS) data,
    parse the raw files, and perform analytical operations.
    '''

    def _download_base_parameters(
        self
    ) -> pandas.DataFrame:
        '''
        Return a DataFrame containing Pension Fund Manager names,
        scheme names, and their corresponding NPS identifiers.
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
        df = df.drop(columns=['ID', 'DATE OF NAV', 'NAV VALUE'])
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
        with pandas.ExcelWriter(excel_file) as excel_writer:
            df.to_excel(excel_writer, index=False)
            workbook = excel_writer.book
            worksheet = excel_writer.sheets['Sheet1']
            worksheet.set_column(0, 0, 50, workbook.add_format({'align': 'left'}))
            worksheet.set_column(1, 1, 120, workbook.add_format({'align': 'left'}))
            worksheet.set_column(2, 2, 15, workbook.add_format({'align': 'left'}))
            header_format = workbook.add_format(
                {'bold': True, 'align': 'center'}
            )
            for idx, col in enumerate(df.columns):
                worksheet.write(0, idx, col, header_format)

        return df

    @property
    def pfm(
        self
    ) -> pandas.Series:
        '''
        Return a Series of all available Pension Fund Manager names.
        '''

        file_path = os.path.join(
            os.path.dirname(__file__), 'base_data', 'base_nps.xlsx'
        )

        df = pandas.read_excel(
            io=file_path
        )

        pfm = df['PFM'].unique()

        return pfm

    def pfm_schemes(
        self,
        pfm_name: str
    ) -> dict[str, str]:
        '''
        Return a dictionary of scheme names and corresponding IDs
        for a given Pension Fund Manager.

        Parameters
        ----------
        pfm_name : str
            Name of the Pension Fund Manager, typically obtained
            from :attr:`BharatFinTrack.NPS.pfm`.

        Returns
        -------
        dict
            A dictionary where keys are scheme names and values are their
            corresponding NPS identifiers.
        '''

        file_path = os.path.join(
            os.path.dirname(__file__), 'base_data', 'base_nps.xlsx'
        )

        df = pandas.read_excel(
            io=file_path
        )

        if pfm_name not in df['PFM'].tolist():
            raise ValueError(
                f'Invalid name: {pfm_name}\n'
                '\nThe list of valid names are:\n'
                f'{json.dumps(df['PFM'].unique().tolist(), indent=4)}'
            )

        df = df[df['PFM'].isin([pfm_name])]
        df = df.drop(columns=['PFM']).reset_index(drop=True)

        scheme_id = dict(zip(df['SCHEME'], df['ID']))

        return scheme_id
