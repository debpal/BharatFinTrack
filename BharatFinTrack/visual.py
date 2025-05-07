import os
import tempfile
import pandas
import matplotlib
import matplotlib.pyplot
import matplotlib.figure
from .core import Core
from .nse_tri import NSETRI


class Visual:

    '''
    Provides functionality for plotting data.
    '''

    def _mi_df_bar_closing_with_category(
        self,
        df: pandas.DataFrame,
        close_type: str,
        index_type: str,
        figure_title: str,
        figure_file: str
    ) -> matplotlib.figure.Figure:

        '''
        Helper function to create a bar plot of the closing values (PRICE/TRI)
        of NSE indices from a multi-index DataFrame.
        '''

        # check validity of input figure file path
        check_file = Core().is_valid_figure_extension(figure_file)
        if not check_file:
            raise Exception('Input figure file extension is not supported.')

        # check close value type
        if close_type not in ['PRICE', 'TRI']:
            raise Exception(f'Invalid indices close value type: {close_type}; must be one of [PRICE, TRI].')

        # catgory of indices
        categories = df.index.get_level_values('Category').unique()

        # close date
        close_date = df['Close Date'].iloc[0].strftime('%d-%b-%Y')

        # color for NSE indices category
        colormap = matplotlib.colormaps.get_cmap('Set2')
        category_color = {
            categories[count]: colormap(count / len(categories)) for count in range(len(categories))
        }

        # figure
        fig_height = int(len(df) / 3.5) + 1 if len(df) >= 18 else 5
        xtick_gap = 10000
        xaxis_max = int(((df['Close Value'].max() + 20000) / xtick_gap) + 1) * xtick_gap
        fig_width = int((xaxis_max / xtick_gap) * 1.5)
        figure = matplotlib.pyplot.figure(
            figsize=(fig_width, fig_height)
        )
        subplot = figure.subplots(1, 1)

        # plotting indices closing values
        categories_legend = set()
        for count, (index, row) in enumerate(df.iterrows()):
            category = index[0]
            color = category_color[category]
            if category not in categories_legend:
                subplot.barh(
                    row['Index Name'], row['Close Value'],
                    color=color,
                    label=category
                )
                categories_legend.add(category)
            else:
                subplot.barh(
                    row['Index Name'], row['Close Value'],
                    color=color
                )
            age = row['Years'] + (row['Days'] / 365)
            bar_label = f"({row['CAGR(%)']:.1f}%,{round(row['Close/Base'])}X,{age:.1f}Y)"
            subplot.text(
                row['Close Value'] + 100, count, bar_label,
                va='center',
                fontsize=10
            )

        # x-axis customization
        subplot.set_xlim(0, xaxis_max)
        xticks = range(0, xaxis_max + 1, xtick_gap)
        subplot.set_xticks(
            ticks=xticks
        )
        xticklabels = [
            f'{int(val / 1000)}k' for val in xticks
        ]
        subplot.set_xticklabels(
            labels=xticklabels,
            fontsize=12
        )
        subplot.tick_params(
            axis='x', which='both',
            direction='in', length=6, width=1,
            top=True, bottom=True,
            labeltop=True, labelbottom=True
        )
        subplot.grid(
            visible=True,
            which='major', axis='x',
            color='gray',
            linestyle='--', linewidth=0.3
        )
        subplot.set_xlabel(
            f'Close Value (Date: {close_date})',
            fontsize=15,
            labelpad=15
        )

        # reverse y-axis
        subplot.invert_yaxis()

        # y-axis customization
        subplot.set_ylabel(
            f'{index_type} Index',
            fontsize=15,
            labelpad=15
        )
        subplot.set_ylim(len(df), -1)

        # legend
        subplot.legend(
            title='Index Category',
            loc='lower right',
            fontsize=12,
            title_fontsize=12
        )

        # figure customization
        figure.suptitle(
            figure_title,
            fontsize=15,
            y=1
        )
        figure.tight_layout()
        figure.savefig(
            figure_file,
            bbox_inches='tight'
        )

        # close the figure to prevent duplicate plots from displaying
        matplotlib.pyplot.close(figure)

        return figure

    def plot_cagr_filtered_indices_by_category(
        self,
        excel_file: str,
        close_type: str,
        figure_file: str,
        threshold_cagr: float = 10.0,
        index_type: str = 'NSE Equity'
    ) -> matplotlib.figure.Figure:

        '''
        Returns a bar plot of the closing values (PRICE/TRI) of NSE indices grouped by categoty,
        filtered by a specified threshold CAGR (%) since their launch.

        Parameters
        ----------
        excel_file : str
            Path of the input Excel file containing the data.

        close_type : str
            Type of closing value for indices, either 'PRICE' or 'TRI'.

        figure_file : str
            File Path to save the output figure.

        threshold_cagr : float, optional
            Only plot indices with a CAGR (%) higher than the specified threshold.
            Default is 10.

        index_type : str, optional
            Type of index. Default is 'NSE Equity'.

        Returns
        -------
        Figure
            A bar plot displaying closing values of NSE indices, along with
            CAGR (%), Multiplier (X), and Age (Y) since launch.
        '''

        # input DataFrame
        df = pandas.read_excel(excel_file, index_col=[0, 1])
        df = df[df['CAGR(%)'] >= threshold_cagr]

        # check filtered dataframe
        if len(df) == 0:
            raise Exception('Threshold values return an empty DataFrame.')

        # figure
        figure_title = (
            f'Category-wise Threshold CAGR (>= {threshold_cagr} %) Since Launch: '
            f'Closing {close_type} (Bar) with CAGR (%), Multiplier (X), and Age (Y)'
        )
        figure = self._mi_df_bar_closing_with_category(
            df=df,
            close_type=close_type,
            index_type=index_type,
            figure_title=figure_title,
            figure_file=figure_file
        )

        return figure

    def plot_top_cagr_indices_by_category(
        self,
        excel_file: str,
        close_type: str,
        figure_file: str,
        top_cagr: int = 5,
        index_type: str = 'NSE Equity'
    ) -> matplotlib.figure.Figure:

        '''
        Returns a bar plot of the closing values (PRICE/TRI) of NSE indices
        with the top CAGR (%) since their launch, grouped by category.

        Parameters
        ----------
        excel_file : str
            Path of the input Excel file containing the data.

        close_type : str
            Type of closing value for indices, either 'PRICE' or 'TRI'.

        figure_file : str
            File Path to save the output figure.

        top_cagr : int, optional
            The number of top indices by CAGR (%) to plot for each category.
            Default is 5.

        index_type : str, optional
            Type of index. Default is 'NSE Equity'.

        Returns
        -------
        Figure
            A bar plot displaying closing values of NSE indices, along with
            CAGR (%), Multiplier (X), and Age (Y) since launch.
        '''

        # input DataFrame
        df = pandas.read_excel(excel_file, index_col=[0, 1])
        df = df.groupby(level='Category').head(top_cagr)

        # figure
        figure_title = (
            f'Category-wise Top {top_cagr} CAGR (%) Since Launch: '
            f'Closing {close_type} (Bar) with CAGR (%), Multiplier (X), and Age (Y)'
        )
        figure = self._mi_df_bar_closing_with_category(
            df=df,
            close_type=close_type,
            index_type=index_type,
            figure_title=figure_title,
            figure_file=figure_file
        )

        return figure

    def _df_bar_closing(
        self,
        df: pandas.DataFrame,
        close_type: str,
        index_type: str,
        figure_title: str,
        figure_file: str
    ) -> matplotlib.figure.Figure:

        '''
        Helper function to create a bar plot of the closing values (PRICE/TRI)
        for NSE indices from a DataFrame where index categories are not specified.
        '''

        # check validity of input figure file path
        check_file = Core().is_valid_figure_extension(figure_file)
        if not check_file:
            raise Exception('Input figure file extension is not supported.')

        # check close value type
        if close_type not in ['PRICE', 'TRI']:
            raise Exception(f'Invalid indices close value type: {close_type}; must be one of [PRICE, TRI].')

        # close date
        close_date = df['Close Date'].iloc[0].strftime('%d-%b-%Y')

        # figure
        fig_height = int(len(df) / 3.5) + 1 if len(df) >= 18 else 5
        xtick_gap = 10000
        xaxis_max = int(((df['Close Value'].max() + 20000) / xtick_gap) + 1) * xtick_gap
        fig_width = int((xaxis_max / xtick_gap) * 1.5)
        figure = matplotlib.pyplot.figure(
            figsize=(fig_width, fig_height)
        )
        subplot = figure.subplots(1, 1)

        # plotting indices closing values
        bar_color = 'lawngreen' if close_type == 'TRI' else 'cyan'
        for count, (index, row) in enumerate(df.iterrows()):
            subplot.barh(
                row['Index Name'], row['Close Value'],
                color=bar_color
            )
            age = row['Years'] + (row['Days'] / 365)
            bar_label = f"({row['CAGR(%)']:.1f}%,{round(row['Close/Base'])}X,{age:.1f}Y)"
            subplot.text(
                row['Close Value'] + 100, count, bar_label,
                va='center',
                fontsize=10
            )

        # x-axis customization
        subplot.set_xlim(0, xaxis_max)
        xticks = range(0, xaxis_max + 1, xtick_gap)
        subplot.set_xticks(
            ticks=xticks
        )
        xticklabels = [
            f'{int(val / 1000)}k' for val in xticks
        ]
        subplot.set_xticklabels(
            labels=xticklabels,
            fontsize=12
        )
        subplot.tick_params(
            axis='x', which='both',
            direction='in', length=6, width=1,
            top=True, bottom=True,
            labeltop=True, labelbottom=True
        )
        subplot.grid(
            visible=True,
            which='major', axis='x',
            color='gray',
            linestyle='--', linewidth=0.3
        )
        subplot.set_xlabel(
            f'Close Value (Date: {close_date})',
            fontsize=15,
            labelpad=15
        )

        # reverse y-axis
        subplot.invert_yaxis()

        # y-axis customization
        subplot.set_ylabel(
            f'{index_type} Index',
            fontsize=15,
            labelpad=15
        )
        subplot.set_ylim(len(df), -1)

        # figure customization
        figure.suptitle(
            figure_title,
            fontsize=15,
            y=1
        )
        figure.tight_layout()
        figure.savefig(
            figure_file,
            bbox_inches='tight'
        )

        # close the figure to prevent duplicate plots from displaying
        matplotlib.pyplot.close(figure)

        return figure

    def plot_cagr_filtered_indices(
        self,
        excel_file: str,
        close_type: str,
        figure_file: str,
        threshold_cagr: float = 20.0,
        index_type: str = 'NSE Equity'
    ) -> matplotlib.figure.Figure:

        '''
        Returns a bar plot of the closing values (PRICE/TRI) of NSE indices,
        filtered by a specified threshold CAGR (%) since their launch.

        Parameters
        ----------
        excel_file : str
            Path of the input Excel file containing the data.

        close_type : str
            Type of closing value for indices, either 'PRICE' or 'TRI'.

        figure_file : str
            File Path to save the output figue.

        threshold_cagr : float, optional
            Only plot indices with a CAGR (%) higher than the specified threshold.
            Default is 20.

        index_type : str, optional
            Type of index. Default is 'NSE Equity'.

        Returns
        -------
        Figure
            A bar plot displaying closing values of NSE indices, along with
            CAGR (%), Multiplier (X), and Age (Y) since launch.
        '''

        # input DataFrame
        df = pandas.read_excel(excel_file)
        df = df[df['CAGR(%)'] >= threshold_cagr]

        # check filtered dataframe
        if len(df) == 0:
            raise Exception('Threshold values return an empty DataFrame.')

        # figure
        figure_title = (
            f'Threshold CAGR (>= {threshold_cagr} %) Since Launch: '
            f'Closing {close_type} (Bar) with CAGR (%), Multiplier (X), and Age (Y)'
        )
        figure = self._df_bar_closing(
            df=df,
            close_type=close_type,
            index_type=index_type,
            figure_title=figure_title,
            figure_file=figure_file
        )

        return figure

    def plot_top_cagr_indices(
        self,
        excel_file: str,
        close_type: str,
        figure_file: str,
        top_cagr: int = 20,
        index_type: str = 'NSE Equity'
    ) -> matplotlib.figure.Figure:

        '''
        Returns a bar plot of the closing values (PRICE/TRI) of NSE indices
        with the top CAGR (%) since their launch.

        Parameters
        ----------
        excel_file : str
            Path of the input Excel file containing the data.

        close_type : str
            Type of closing value for indices, either 'PRICE' or 'TRI'.

        figure_file : str
            File Path to save the output figue.

        top_cagr : int, optional
            The number of top indices by CAGR (%) to plot for each category.
            Default is 20.

        index_type : str, optional
            Type of index. Default is 'NSE Equity'.

        Returns
        -------
        Figure
            A bar plot displaying closing values of NSE indices, along with
            CAGR (%), Multiplier (X), and Age (Y) since launch.
        '''

        # input DataFrame
        df = pandas.read_excel(excel_file)
        df = df.head(top_cagr)

        # figure
        figure_title = (
            f'Top {top_cagr} CAGR (%) Since Launch: '
            f'Closing {close_type} (Bar) with CAGR (%), Multiplier (X), and Age (Y)'
        )
        figure = self._df_bar_closing(
            df=df,
            close_type=close_type,
            index_type=index_type,
            figure_title=figure_title,
            figure_file=figure_file
        )

        return figure

    def plot_yearwise_sip_returns(
        self,
        index: str,
        excel_file: str,
        figure_file: str,
        ytick_gap: int = 500
    ) -> matplotlib.figure.Figure:

        '''
        Generates and returns a bar plot of investments and returns for a
        monthly SIP of 1,000 Rupees over the years for a specified index.

        Parameters
        ----------
        index : str
            Name of the index.

        excel_file : str
            Path to the Excel file obtained from :meth:`BharatFinTrack.NSETRI.download_historical_daily_data`
            and :meth:`BharatFinTrack.NSETRI.update_historical_daily_data` methods.

        figure_file : str
            File Path to save the output figue.

        ytick_gap : int, optional
            Gap between two y-axis ticks. Default is 500.

        Returns
        -------
        Figure
            A bar plot displaying the investment and returns of a
            monthly SIP of 1,000 Rupees over years for the specified index.
        '''

        # check validity of input figure file path
        check_file = Core().is_valid_figure_extension(figure_file)
        if not check_file:
            raise Exception('Input figure file extension is not supported.')

        # monthly investment amount
        monthly_invest = 1000

        # SIP DataFrame of index
        with tempfile.TemporaryDirectory() as tmp_dir:
            df = NSETRI().yearwise_sip_analysis(
                input_excel=excel_file,
                monthly_invest=monthly_invest,
                output_excel=os.path.join(tmp_dir, 'output.xlsx')

            )

        # figure
        fig_width = len(df) * 1.2 if len(df) >= 9 else 10
        figure = matplotlib.pyplot.figure(
            figsize=(fig_width, 10)
        )
        subplot = figure.subplots(1, 1)

        # plot bars
        xticks = pandas.Series(
            range(len(df['Year']))
        )
        bar_width = 0.4
        subplot.bar(
            x=xticks - bar_width / 2,
            height=df['Invest'] / monthly_invest,
            width=bar_width,
            label='Invest',
            color='gold'
        )
        subplot.bar(
            x=xticks + bar_width / 2,
            height=df['Value'] / monthly_invest,
            width=bar_width,
            label='Return',
            color='lightgreen'
        )
        for xt in xticks:
            multiple = df['Multiple (X)'][xt]
            xirr = df['XIRR (%)'][xt]
            subplot.annotate(
                f'{multiple:.1f}X,{xirr:.0f}%',
                xy=(xticks[xt] + bar_width / 2, df['Value'][xt] / monthly_invest),
                ha='center', va='bottom',
                fontsize=12
            )

        # x-axis customization
        subplot.set_xticks(
            ticks=xticks
        )
        xticklabels = list(
            map(
                lambda x: x[0].strftime('%d-%b-%Y') + f' ({x[1] + 1}Y)', zip(df['Start Date'], xticks)
            )
        )
        xticklabels[-1] = xticklabels[-1].replace(xticklabels[-1][12:], '\n(Launch)')
        subplot.set_xticklabels(
            labels=xticklabels,
            rotation=45,
            fontsize=12
        )
        subplot.set_xlabel(
            xlabel='SIP Start Date',
            fontsize=15
        )

        # y-axis customization
        yaxis_max = (round((df['Value'].max() / monthly_invest + 50) / ytick_gap) + 1) * ytick_gap
        subplot.set_ylim(0, yaxis_max)
        yticks = range(0, yaxis_max + 1, ytick_gap)
        subplot.set_yticks(
            ticks=yticks
        )
        yticklabels = [str(yt) + 'K' for yt in yticks]
        subplot.set_yticklabels(
            labels=yticklabels,
            fontsize=12
        )
        subplot.tick_params(
            axis='y', which='both',
            direction='in', length=6, width=1,
            left=True, right=True,
            labelleft=True, labelright=True
        )
        subplot.grid(
            visible=True,
            which='major', axis='y',
            color='gray',
            linestyle='--', linewidth=0.3
        )
        close_date = df['Close Date'].iloc[0].strftime('%d-%b-%Y')
        subplot.set_ylabel(
            ylabel=f'Amount (Date: {close_date})',
            fontsize=15
        )

        # legend
        subplot.legend(
            loc='upper left',
            fontsize=15
        )

        # figure customization
        figure_title = (
            f'{index.upper()}\n\nReturn with Multiples (X) and XIRR (%) for SIP 1000 Rupees on First Date of Each Month Over Years'
        )
        figure.suptitle(
            t=figure_title,
            fontsize=15
        )
        figure.tight_layout()
        figure.savefig(
            figure_file,
            bbox_inches='tight'
        )

        # close the figure to prevent duplicate plots from displaying
        matplotlib.pyplot.close(figure)

        return figure

    def plot_sip_index_vs_gsec(
        self,
        index: str,
        excel_file: str,
        figure_file: str,
        gsec_return: float = 8,
        ytick_gap: int = 500
    ) -> matplotlib.figure.Figure:

        '''
        Generates a bar plot comparing the returns of a specified index
        and government bonds for a monthly SIP of 1,000 Rupees over the years.'

        Parameters
        ----------
        index : str
            Name of the index.

        excel_file : str
            Path to the Excel file obtained from :meth:`BharatFinTrack.NSETRI.download_historical_daily_data`
            and :meth:`BharatFinTrack.NSETRI.update_historical_daily_data` methods.

        figure_file : str
            File Path to save the output figue.

        gsec_return : float, optional
            Expected annual return rate of government bond in percentage. Default is 8.

        ytick_gap : int, optional
            Gap between two y-axis ticks. Default is 500.

        Returns
        -------
        Figure
            A bar plot showing the return comparison between the specified index
            and government bonds for a monthly SIP of 1,000 Rupees over the years.
        '''

        # check validity of input figure file path
        check_file = Core().is_valid_figure_extension(figure_file)
        if not check_file:
            raise Exception('Input figure file extension is not supported.')

        # monthly investment amount
        monthly_invest = 1000

        # SIP DataFrame of index
        with tempfile.TemporaryDirectory() as tmp_dir:
            df = NSETRI().yearwise_sip_analysis(
                input_excel=excel_file,
                monthly_invest=monthly_invest,
                output_excel=os.path.join(tmp_dir, 'output.xlsx')

            )

        # filted DataFrame
        sip_years = int(df['Year'].max())
        df = df[df['Year'] <= sip_years].reset_index(drop=True)

        # bank fixed deposit DataFrame
        bank_df = Core().sip_growth(
            invest=monthly_invest,
            frequency='monthly',
            annual_return=gsec_return,
            years=sip_years
        )

        # figure
        fig_width = len(df) * 1.2 if len(df) >= 9 else 10
        figure = matplotlib.pyplot.figure(
            figsize=(fig_width, 10)
        )
        subplot = figure.subplots(1, 1)

        # plot bars
        xticks = pandas.Series(
            range(len(df['Year']))
        )
        bar_width = 0.3
        subplot.bar(
            x=xticks - bar_width,
            height=df['Invest'] / monthly_invest,
            width=bar_width,
            label='Invest',
            color='gold'
        )
        subplot.bar(
            x=xticks,
            height=bank_df['Value'] / monthly_invest,
            width=bar_width,
            label=f'Government ({gsec_return:.1f}%)',
            color='cyan'
        )
        subplot.bar(
            x=xticks + bar_width,
            height=df['Value'] / monthly_invest,
            width=bar_width,
            label=index.upper(),
            color='lightgreen'
        )
        for xt in xticks:
            multiple = df['Multiple (X)'][xt]
            xirr = df['XIRR (%)'][xt]
            subplot.annotate(
                f'{multiple:.1f}X,{xirr:.0f}%',
                xy=(xticks[xt] + bar_width, df['Value'][xt] / monthly_invest),
                ha='center', va='bottom',
                fontsize=12
            )

        # x-axis customization
        subplot.set_xticks(
            ticks=xticks
        )
        xticklabels = list(
            map(
                lambda x: x[0].strftime('%d-%b-%Y') + f' ({x[1] + 1}Y)', zip(df['Start Date'], xticks)
            )
        )
        subplot.set_xticklabels(
            labels=xticklabels,
            rotation=45,
            fontsize=12
        )
        subplot.set_xlabel(
            xlabel='Start Date',
            fontsize=15
        )

        # y-axis customization
        yaxis_max = (round((df['Value'].max() / monthly_invest + 50) / ytick_gap) + 1) * ytick_gap
        subplot.set_ylim(0, yaxis_max)
        yticks = range(0, yaxis_max + 1, ytick_gap)
        subplot.set_yticks(
            ticks=yticks
        )
        yticklabels = [str(yt) + 'K' for yt in yticks]
        subplot.set_yticklabels(
            labels=yticklabels,
            fontsize=12
        )
        subplot.tick_params(
            axis='y', which='both',
            direction='in', length=6, width=1,
            left=True, right=True,
            labelleft=True
        )
        subplot.grid(
            visible=True,
            which='major', axis='y',
            color='gray',
            linestyle='--', linewidth=0.3
        )
        close_date = df['Close Date'].iloc[0].strftime('%d-%b-%Y')
        subplot.set_ylabel(
            ylabel=f'Amount (Date: {close_date})',
            fontsize=15
        )

        # legend
        subplot.legend(
            loc='upper left',
            fontsize=15
        )

        # figure customization
        figure_title = (
            f'{index.upper()} Return with Multiples (X) and XIRR (%)\n\nComparison Return Between Index and Government Bond for SIP 1000 Rupees on First Date of Each Month Over Years'
        )
        figure.suptitle(
            t=figure_title,
            fontsize=15
        )
        figure.tight_layout()
        figure.savefig(
            figure_file,
            bbox_inches='tight'
        )

        # close the figure to prevent duplicate plots from displaying
        matplotlib.pyplot.close(figure)

        return figure

    def plot_sip_growth_comparison_across_indices(
        self,
        indices: list[str],
        folder_path: str,
        figure_file: str,
        ytick_gap: int = 2
    ) -> matplotlib.figure.Figure:

        '''
        Generates a line plot comparing monthly SIP investment growth across multiple indices over the years.

        Parameters
        ----------
        indices : list
            A list of index names to compare in the SIP growth plot.

        folder_path : str
            Path to the directory containing Excel files with historical data for each index. Each Excel file must be
            named as '{index}.xlsx' corresponding to the index names provided in the `indices` list. These files should
            be obtained from :meth:`BharatFinTrack.NSETRI.download_historical_daily_data` or
            :meth:`BharatFinTrack.NSETRI.update_historical_daily_data`.

        figure_file : str
            File Path to save the output figue.

        ytick_gap : int, optional
            Gap between two y-axis ticks. Default is 2.

        Returns
        -------
        Figure
            A line plot figure showing cumulative SIP investment growth for each index over time.
        '''

        # check validity of input figure file path
        check_file = Core().is_valid_figure_extension(figure_file)
        if not check_file:
            raise Exception('Input figure file extension is not supported.')

        # monthly investment amount
        monthly_invest = 1000

        # SIP dataframe of index
        dataframes = []
        with tempfile.TemporaryDirectory() as tmp_dir:
            for index in indices:
                index_excel = os.path.join(folder_path, f'{index}.xlsx')
                df = NSETRI().yearwise_sip_analysis(
                    input_excel=index_excel,
                    monthly_invest=monthly_invest,
                    output_excel=os.path.join(tmp_dir, 'output.xlsx')
                )
                dataframes.append(df)

        # check equal close date for all DataFrames
        close_date = dataframes[0]['Close Date'].iloc[0]
        equal_closedate = all(map(lambda df: df['Close Date'].iloc[0] == close_date, dataframes))
        if not equal_closedate:
            raise Exception('Last date must be equal across all indices in the Excel files.')

        # filtered dataframes
        common_year = min(
            map(lambda df: int(df['Year'].max()), dataframes)
        )
        dataframes = list(
            map(
                lambda df: df[df['Year'] <= common_year], dataframes
            )
        )

        # figure
        figure = matplotlib.pyplot.figure(figsize=(25, 10))
        subplot = figure.subplots(1, 1)

        # plot
        colormap = matplotlib.colormaps.get_cmap('hsv')
        colors = [colormap(df / len(dataframes)) for df in range(len(dataframes))]
        for df, color, index in zip(dataframes, colors, indices):
            subplot.plot(
                df.index, df['Multiple (X)'],
                marker='o', markersize=8,
                color=color,
                label=index
            )

        # x-axis customization
        xticks = pandas.Series(
            range(common_year)
        )
        subplot.set_xticks(
            ticks=xticks
        )
        xticklabels = list(
            map(
                lambda x: x[0].strftime('%d-%b-%Y') + f' ({x[1] + 1}Y)', zip(dataframes[0]['Start Date'], xticks)
            )
        )
        subplot.set_xticklabels(
            labels=xticklabels,
            rotation=45,
            fontsize=12
        )
        subplot.set_xlabel(
            xlabel='SIP Start Date',
            fontsize=15
        )

        # y-axis customization
        growth_max = max(
            map(lambda df: int(df['Multiple (X)'].max()) + 1, dataframes)
        )
        yaxis_max = (int(growth_max / ytick_gap) + 1) * ytick_gap
        subplot.set_ylim(0, yaxis_max)
        yticks = range(0, yaxis_max + 1, ytick_gap)
        subplot.set_yticks(
            ticks=yticks
        )
        subplot.set_yticklabels(
            labels=[str(yt) for yt in yticks],
            fontsize=12
        )
        subplot.tick_params(
            axis='y', which='both',
            direction='in', length=6, width=1,
            left=True, right=True,
            labelleft=True, labelright=True
        )
        subplot.grid(
            visible=True,
            which='major', axis='y',
            color='gray',
            linestyle='--', linewidth=0.3
        )
        subplot.set_ylabel(
            ylabel=f'Multiples (X) of Investment (Date: {close_date.strftime("%d-%b-%Y")})',
            fontsize=15
        )

        # legend
        subplot.legend(
            loc='upper left',
            fontsize=12
        )

        # figure customization
        figure_title = (
            'Growth of Monthly SIP Investment on First Date of each Month Over Years'
        )
        figure.suptitle(
            t=figure_title,
            fontsize=15
        )
        figure.tight_layout()
        figure.savefig(
            figure_file,
            bbox_inches='tight'
        )

        # close the figure to prevent duplicate plots from displaying
        matplotlib.pyplot.close(figure)

        return figure
