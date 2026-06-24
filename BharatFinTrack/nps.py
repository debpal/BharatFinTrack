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
        self,
        save_base: bool = False
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
        if save_base:
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

        # DataFrame
        file_path = os.path.join(
            os.path.dirname(__file__), 'base_data', 'base_nps.xlsx'
        )
        df = pandas.read_excel(
            io=file_path
        )

        # Write the DataFrame
        if excel_file is not None:
            self._base_df_to_excel(
                df=df,
                excel_file=excel_file
            )

        return df

    @property
    def _pfm_info(
        self
    ) -> dict[str, dict[str, str]]:
        '''
        Return a nested dictionary mapping Pension Fund Manager names to their information.
        '''

        info_dict = {
            'Aditya Birla': {
                'company': 'Aditya Birla Sunlife Pension Fund management Limited',
                'code': 'PFM010'
            },
            'Axis': {
                'company': 'AXIS PENSION FUND MANAGEMENT LIMITED',
                'code': 'PFM013'
            },
            'DSP': {
                'company': 'DSP PENSION FUND MANAGERS PRIVATE LIMITED',
                'code': 'PFM014'
            },
            'HDFC': {
                'company': 'HDFC Pension Fund Management Limited',
                'code': 'PFM008'
            },
            'ICICI': {
                'company': 'ICICI Prudential Pension Fund Management Co. Ltd.',
                'code': 'PFM007'
            },
            'Kotak': {
                'company': 'Kotak Mahindra Pension Fund Ltd.',
                'code': 'PFM005'
            },
            'LIC': {
                'company': 'LIC Pension Fund Ltd.',
                'code': 'PFM003'
            },
            'SBI': {
                'company': 'SBI Pension Funds Pvt. Ltd.',
                'code': 'PFM001'
            },
            'TATA': {
                'company': 'Tata Pension Fund Management Private Limited',
                'code': 'PFM011'
            },
            'UTI': {
                'company': 'UTI Pension Fund Limited.',
                'code': 'PFM002'
            }
        }

        return info_dict

    @property
    def pfm_options(
        self
    ) -> list[str]:
        '''
        Return a list of valid Pension Fund Manager names.
        '''

        pfm_list = list(self._pfm_info.keys())

        return pfm_list

    def _validate_pfm_name(
        self,
        pfm_name: str
    ) -> None:
        '''
        Validate the Pension Fund Manager name.
        '''

        # PFM list
        pfm_list = self.pfm_options

        # Check valid PFM option
        if pfm_name not in pfm_list:
            raise ValueError(
                f'Invalid PFM name: {pfm_name}, valid options are: {pfm_list}'
            )

        return None

    def pfm_schemes(
        self,
        pfm_name: str
    ) -> str:
        '''
        Return scheme names and corresponding identifiers for a given Pension Fund Manager.

        Parameters
        ----------
        pfm_name : str
            Name of the Pension Fund Manager. Valid options can be obtained
            from :attr:`BharatFinTrack.NPS.pfm_options`.

        Returns
        -------
        str
            A JSON-formatted string dictionary where keys are scheme names and values
            are their corresponding NPS identifiers.
        '''

        # Check static type of input variable origin
        Helper()._validate_variable_origin_static_type(
            vars_types=typing.get_type_hints(
                obj=self.pfm_schemes
            ),
            vars_values=locals()
        )

        # Check valid PFM option
        self._validate_pfm_name(
            pfm_name=pfm_name
        )

        pfm_info = self._pfm_info

        # Schemes
        company = pfm_info[pfm_name]['company']
        df = self.base_df()
        df = df[df['PFM'].isin([company])]
        df = df.drop(columns=['PFM']).reset_index(drop=True)
        scheme_id = json.dumps(
            obj=dict(zip(df['SCHEME'], df['ID'])),
            indent=4
        )

        return scheme_id

    def _validate_scheme_ids(
        self,
        scheme_ids: list[str]
    ) -> None:
        '''
        Validate each scheme identifier from the given list.
        '''

        # Check validity of scheme identifiers
        base_df = self.base_df()
        for scheme in scheme_ids:
            if scheme not in base_df['ID'].values:
                raise ValueError(
                    f'Invalid scheme identifier: {scheme}'
                )

        return None

    def schemes_latest_nav(
        self,
        scheme_ids: typing.Optional[list[str]] = None,
        excel_file: typing.Optional[str] = None
    ) -> pandas.DataFrame:
        '''
        Fetch the latest NAV for the specified NPS schemes across different Pension Fund Managers.

        Parameters
        ----------
        scheme_ids : list, optional
            A list of scheme identifiers, typically obtained from the ``ID``
            column of :meth:`BharatFinTrack.NPS.base_df`. If None (default),
            the NAV data for all available schemes is retrieved.

        excel_file : str, optional
            Path to an Excel file to save the output DataFrame.

        Returns
        -------
        DataFrame
            A DataFrame containing scheme names, identifiers, and their corresponding NAV dates and values.
        '''

        # Check static type of input variable origin
        Helper()._validate_variable_origin_static_type(
            vars_types=typing.get_type_hints(
                obj=self.schemes_latest_nav
            ),
            vars_values=locals()
        )

        # Check validity of scheme identifiers
        if scheme_ids is not None:
            self._validate_scheme_ids(
                scheme_ids=scheme_ids
            )

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

    def scheme_historical_nav(
        self,
        pfm_name: str,
        scheme_id: str,
        csv_file: typing.Optional[str] = None
    ) -> pandas.DataFrame:
        '''
        Download historical daily NAV values for a specified Pension Fund Manager and scheme identifier.

        Additionally, this method prints the associated scheme name(s) to verify that the
        correct data is being downloaded. The printed list may contain multiple names due to
        the Multiple NAV Framework implementation effective from April 1, 2026.

        Parameters
        ----------
        pfm_name : str
            Name of the Pension Fund Manager. Valid options can be obtained
            from :attr:`BharatFinTrack.NPS.pfm_options`.

        scheme_id : str
            Name of scheme identifier, typically obtained from the ``ID``
            column of :meth:`BharatFinTrack.NPS.base_df`.

        csv_file : str, optional
            Path to an CSV file to save the output DataFrame.

        Returns
        -------
        DataFrame
            A DataFrame containing daily dates (``Date`` column) and their
            corresponding NAV values (``Close`` column) from inception.
        '''

        # Check static type of input variable origin
        Helper()._validate_variable_origin_static_type(
            vars_types=typing.get_type_hints(
                obj=self.scheme_historical_nav
            ),
            vars_values=locals()
        )

        # Check valid PFM option
        self._validate_pfm_name(
            pfm_name=pfm_name
        )

        # Check validity of scheme identifiers
        self._validate_scheme_ids(
            scheme_ids=[scheme_id]
        )

        # Download Data
        url_main = 'https://npstrust.org.in/scheme-wise-nav-report-excel?'
        pfm_info = self._pfm_info
        pfm_code = pfm_info[pfm_name]['code']
        url_sub = f'navcatdataxls={pfm_code}&navyearselxls=all&navsubdataxls={scheme_id}'
        response = requests.get(
            url=url_main + url_sub
        )
        content = response.content.decode('utf-8')

        # DataFrame processing
        df = pandas.read_csv(
            filepath_or_buffer=io.StringIO(content),
            sep='\t'
        )
        scheme_name = df['SCHEME NAME'].unique()
        print(f'Scheme name: {scheme_name}')
        df = df[['DATE OF NAV', 'NAV VALUE']]
        df.columns = ['Date', 'Close']
        df = df[::-1].reset_index(drop=True)
        df['Date'] = pandas.to_datetime(
            arg=df['Date'],
            format='%Y-%m-%d'
        ).dt.date

        # Save the DataFrame
        if csv_file is not None:
            # Validate output file path
            Helper()._validate_file_path(
                input_file=csv_file,
                input_ext='.csv'
            )
            # Write DataFrame to the CSV file
            Helper()._df_date_to_csv(
                df=df,
                csv_file=csv_file,
                date_cols=['Date']
            )

        return df
