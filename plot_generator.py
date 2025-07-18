import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend for server environments
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from prophet import Prophet

def generate_plot(df, chart_type, x_col=None, y_col=None):
    if chart_type in ["pairplot", "clustermap", "jointplot"]:
        # These return their own figure objects
        if chart_type == "pairplot":
            plot = sns.pairplot(df.select_dtypes(include='number'))
            return plot
        elif chart_type == "clustermap":
            corr = df.select_dtypes(include='number').corr()
            plot = sns.clustermap(corr, cmap="viridis", annot=True)
            return plot
        elif chart_type == "jointplot":
            if x_col and y_col:
                plot = sns.jointplot(data=df, x=x_col, y=y_col, kind="scatter")
                return plot
            else:
                return None
    else:
        fig, ax = plt.subplots(figsize=(10, 5))
        plot = None
        if chart_type == "scatterplot":
            plot = sns.scatterplot(data=df, x=x_col, y=y_col, ax=ax)
        elif chart_type == "lineplot":
            plot = sns.lineplot(data=df, x=x_col, y=y_col, ax=ax)
        elif chart_type == "barplot":
            plot = sns.barplot(data=df, x=x_col, y=y_col, ax=ax)
        elif chart_type == "countplot":
            plot = sns.countplot(data=df, x=x_col, ax=ax)
        elif chart_type == "boxplot":
            plot = sns.boxplot(data=df, x=x_col, y=y_col, ax=ax)
        elif chart_type == "violinplot":
            plot = sns.violinplot(data=df, x=x_col, y=y_col, ax=ax)
        elif chart_type == "stripplot":
            plot = sns.stripplot(data=df, x=x_col, y=y_col, ax=ax)
        elif chart_type == "swarmplot":
            plot = sns.swarmplot(data=df, x=x_col, y=y_col, ax=ax)
        elif chart_type == "histplot":
            plot = sns.histplot(data=df[x_col], bins=20, ax=ax)
        elif chart_type == "kdeplot":
            plot = sns.kdeplot(data=df[x_col], fill=True, ax=ax)
        elif chart_type == "heatmap":
            corr = df.select_dtypes(include='number').corr()
            mask = np.triu(np.ones_like(corr, dtype=bool))
            plot = sns.heatmap(corr, mask=mask, annot=True, cmap='coolwarm', vmin=-1, vmax=1, linewidths=0.5, square=True, cbar_kws={"shrink": .75}, ax=ax)
            ax.set_title('Correlation Heatmap (lower triangle)')
        elif chart_type == "annotated_heatmap":
            corr = df.select_dtypes(include='number').corr()
            plot = sns.heatmap(corr, annot=True, fmt=".2f", cmap="vlag", vmin=-1, vmax=1, linewidths=1, square=True, cbar_kws={"shrink": .75}, ax=ax)
            ax.set_title('Full Correlation Heatmap (annotated)')
        elif chart_type == "rugplot":
            plot = sns.rugplot(data=df[x_col], ax=ax)
        elif chart_type == "forecast":
            if x_col and y_col and x_col in df.columns and y_col in df.columns:
                df_fc = df[[x_col, y_col]].dropna().copy()
                df_fc = df_fc.rename(columns={x_col: 'ds', y_col: 'y'})
                df_fc['ds'] = pd.to_datetime(df_fc['ds'], errors='coerce')
                df_fc = df_fc.dropna(subset=['ds', 'y'])
                m = Prophet()
                m.fit(df_fc)
                future = m.make_future_dataframe(periods=10)
                forecast = m.predict(future)
                ax.plot(df_fc['ds'], df_fc['y'], label='History')
                ax.plot(forecast['ds'], forecast['yhat'], label='Forecast')
                ax.fill_between(forecast['ds'], forecast['yhat_lower'], forecast['yhat_upper'], color='gray', alpha=0.2, label='Confidence Interval')
                ax.legend()
                ax.set_title(f"Forecast for {y_col} over time")
            else:
                plt.close(fig)
                return None
        else:
            plt.close(fig)
            return None
        if chart_type not in ["heatmap", "annotated_heatmap"]:
            ax.set_title(f"{chart_type} of {x_col} and {y_col}" if y_col else f"{chart_type} of {x_col}")
            for label in ax.get_xticklabels():
                label.set_rotation(45)
        fig.tight_layout()
        return fig