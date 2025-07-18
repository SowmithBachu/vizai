import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

def generate_plot(df, chart_type, x_axis=None, y_axis=None):
    fig, ax = plt.subplots()
    if chart_type == "scatterplot":
        sns.scatterplot(data=df, x=x_axis, y=y_axis, ax=ax)
    elif chart_type == "lineplot":
        sns.lineplot(data=df, x=x_axis, y=y_axis, ax=ax)
    elif chart_type == "barplot":
        sns.barplot(data=df, x=x_axis, y=y_axis, ax=ax)
    elif chart_type == "countplot":
        sns.countplot(data=df, x=x_axis, ax=ax)
    elif chart_type == "boxplot":
        sns.boxplot(data=df, x=x_axis, y=y_axis, ax=ax)
    elif chart_type == "violinplot":
        sns.violinplot(data=df, x=x_axis, y=y_axis, ax=ax)
    elif chart_type == "stripplot":
        sns.stripplot(data=df, x=x_axis, y=y_axis, ax=ax)
    elif chart_type == "swarmplot":
        sns.swarmplot(data=df, x=x_axis, y=y_axis, ax=ax)
    elif chart_type == "histplot":
        sns.histplot(data=df, x=x_axis, ax=ax)
    elif chart_type == "kdeplot":
        sns.kdeplot(data=df[x_axis], ax=ax)
    elif chart_type == "pairplot":
        return sns.pairplot(df)
    elif chart_type == "heatmap":
        return sns.heatmap(df.corr(), annot=True, fmt=".2f", cmap="coolwarm")
    elif chart_type == "annotated_heatmap":
        return sns.heatmap(df.corr(), annot=True, fmt=".2f", cmap="YlGnBu")
    elif chart_type == "clustermap":
        return sns.clustermap(df.corr(), annot=True, fmt=".2f", cmap="mako")
    elif chart_type == "jointplot":
        return sns.jointplot(data=df, x=x_axis, y=y_axis, kind="scatter")
    elif chart_type == "rugplot":
        sns.rugplot(data=df, x=x_axis, ax=ax)
    else:
        return None
    return fig 