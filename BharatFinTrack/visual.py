import pandas
import matplotlib
import matplotlib.pyplot
import matplotlib.figure
from .core import Core


class Visual:

    '''
    Provides functionality for plotting data.
    '''

    def _mi_df_bar_graph_closing_value(
        self,
        df: pandas.DataFrame,
        figure_file: str,
    ) -> matplotlib.figure.Figure:

        '''
        Helper function to create a bar plot of the closing values (Price/TRI)
        of NSE indices from a multi-index DataFrame.
        '''

        # catgory of indices
        categories = df.index.get_level_values('Category').unique()
        close_date = df['Close Date'].iloc[0].strftime('%d-%b-%Y')

        # color for NSE indices category
        colormap = matplotlib.colormaps.get_cmap('Set2')
        category_color = {
            categories[count]: colormap(count / len(categories)) for count in range(len(categories))
        }

        # figure
        fig_height = int(len(df) / 3.5) + 1 if len(df) > 7 else 5
        xtick_gap = 10000
        xaxis_max = int(((df['Close Value'].max() + 20000) / xtick_gap) + 1) * xtick_gap
        fig_width = int((xaxis_max / xtick_gap) * 1.5)
        figure = matplotlib.pyplot.figure(
            figsize=(fig_width, fig_height)
        )
        subplot = figure.subplots(1, 1)

        # check validity of input figure file path
        check_file = Core().is_valid_figure_extension(figure_file)
        if check_file is True:
            pass
        else:
            # close the figure to prevent a blank plot from appearing
            matplotlib.pyplot.close(figure)
            raise Exception('Input figure file extension is not supported.')

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
        subplot.set_xticks(
            list(range(0, xaxis_max + 1, xtick_gap))
        )
        xtick_labels = [
            f'{int(val / 1000)}k' for val in list(range(0, xaxis_max + 1, xtick_gap))
        ]
        subplot.set_xticklabels(xtick_labels, fontsize=12)
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
            'Index Name',
            fontsize=20,
            labelpad=15
        )
        subplot.set_ylim(len(df), -1)

        # legend
        subplot.legend(
            title="Index Category",
            loc='lower right',
            fontsize=12,
            title_fontsize=12
        )

        # figure customization
        figure.suptitle(
            'NSE Equity Indices Since Launch: Closing Value Bars with CAGR (%), Multiplier (X), and Age (Y)',
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
        figure_file: str,
        threshold_cagr: float = 10
    ) -> matplotlib.figure.Figure:

        '''
        Returns a bar plot of the closing values (Price/TRI) of NSE indices,
        filtered by a specified threshold CAGR (%) since their launch.

        Parameters
        ----------
        excel_file : str
            Path of the input Excel file containing the data.

        figure_file : str
            File Path to save the output figue.

        threshold_cagr : float
            Only plot indices with a CAGR (%) higher than the specified threshold.
            Default is 10.

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
        else:
            pass

        # figure
        figure = self._mi_df_bar_graph_closing_value(
            df=df,
            figure_file=figure_file
        )

        return figure

    def plot_top_cagr_indices_by_category(
        self,
        excel_file: str,
        figure_file: str,
        top_cagr: int = 5
    ) -> matplotlib.figure.Figure:

        '''
        Returns a bar plot of the closing values (Price/TRI) of NSE indices
        with the top CAGR (%) in each category since their launch.

        Parameters
        ----------
        excel_file : str
            Path of the input Excel file containing the data.

        figure_file : str
            File Path to save the output figue.

        top_cagr : int
            The number of top indices by CAGR (%) to plot for each category.
            Default is 3.

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
        figure = self._mi_df_bar_graph_closing_value(
            df=df,
            figure_file=figure_file
        )

        return figure
