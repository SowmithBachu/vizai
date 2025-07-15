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
        plt.figure(figsize=(10, 5))

        if chart_type == "scatterplot":
            sns.scatterplot(data=df, x=x_col, y=y_col)
        elif chart_type == "lineplot":
            sns.lineplot(data=df, x=x_col, y=y_col)
        elif chart_type == "barplot":
            sns.barplot(data=df, x=x_col, y=y_col)
        elif chart_type == "countplot":
            sns.countplot(data=df, x=x_col)
        elif chart_type == "boxplot":
            sns.boxplot(data=df, x=x_col, y=y_col)
        elif chart_type == "violinplot":
            sns.violinplot(data=df, x=x_col, y=y_col)
        elif chart_type == "stripplot":
            sns.stripplot(data=df, x=x_col, y=y_col)
        elif chart_type == "swarmplot":
            sns.swarmplot(data=df, x=x_col, y=y_col)
        elif chart_type == "histplot":
            sns.histplot(data=df[x_col], bins=20)
        elif chart_type == "kdeplot":
            sns.kdeplot(data=df[x_col], fill=True)
        elif chart_type == "heatmap":
            corr = df.select_dtypes(include='number').corr()
            # Mask the upper triangle for clarity
            mask = np.triu(np.ones_like(corr, dtype=bool))
            sns.heatmap(corr, mask=mask, annot=True, cmap='coolwarm', vmin=-1, vmax=1, linewidths=0.5, square=True, cbar_kws={"shrink": .75})
            plt.title('Correlation Heatmap (lower triangle)')
        elif chart_type == "annotated_heatmap":
            corr = df.select_dtypes(include='number').corr()
            sns.heatmap(corr, annot=True, fmt=".2f", cmap="vlag", vmin=-1, vmax=1, linewidths=1, square=True, cbar_kws={"shrink": .75})
            plt.title('Full Correlation Heatmap (annotated)')
        elif chart_type == "rugplot":
            sns.rugplot(data=df[x_col])
        elif chart_type == "forecast":
            # Forecasting using Prophet
            if x_col and y_col and x_col in df.columns and y_col in df.columns:
                df_fc = df[[x_col, y_col]].dropna().copy()
                df_fc = df_fc.rename(columns={x_col: 'ds', y_col: 'y'})
                # Try to parse datetime
                df_fc['ds'] = pd.to_datetime(df_fc['ds'], errors='coerce')
                df_fc = df_fc.dropna(subset=['ds', 'y'])
                m = Prophet()
                m.fit(df_fc)
                future = m.make_future_dataframe(periods=10)
                forecast = m.predict(future)
                plt.plot(df_fc['ds'], df_fc['y'], label='History')
                plt.plot(forecast['ds'], forecast['yhat'], label='Forecast')
                plt.fill_between(forecast['ds'], forecast['yhat_lower'], forecast['yhat_upper'], color='gray', alpha=0.2, label='Confidence Interval')
                plt.legend()
                plt.title(f"Forecast for {y_col} over time")
            else:
                return None
        else:
            return None

        plt.title(f"{chart_type} of {x_col} and {y_col}" if y_col else f"{chart_type} of {x_col}")
        plt.xticks(rotation=45)
        plt.tight_layout()
        return plt