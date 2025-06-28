import marimo

__generated_with = "0.14.9"
app = marimo.App()


@app.cell
def _():
    # Import required libraries

    import marimo as mo

    import pandas as pd
    import numpy as np

    import seaborn as sns
    import matplotlib.pyplot as plt

    import SourceStatisticalAnalysis as src
    return mo, pd, src


@app.cell
def _():
    # Definition of useful variables

    Carbs = 'Carbs'
    Protein = 'Protein'
    Fat = 'Fat'
    Macronutrients = [Carbs, Protein, Fat]

    Diet = 'Diet_type'
    Diets = ['dash', 'keto', 'mediterranean', 'paleo', 'vegan']

    Dash = 'dash'
    Keto = 'keto'
    Mediterranean = 'mediterranean'
    Paleo = 'paleo'
    Vegan = 'vegan'

    Recipe = 'Recipe_name'
    Total = 'Total_macronutrients'

    RANDOM_STATE = 8013
    return Dash, Diet, Keto, Mediterranean, Paleo, Vegan


@app.cell
def _(pd):
    # Loading dataset

    Diets_Dataset = pd.read_csv('./Datasets/Diets_Dataset_Clean.csv')
    return (Diets_Dataset,)


@app.cell
def _(Diet, Diets_Dataset):
    # Splitting dataset by diet

    Diets_SubDatasets = Diets_Dataset.groupby(Diet)
    return (Diets_SubDatasets,)


@app.cell
def _(mo):
    mo.md(r"# Introduction")
    return


@app.cell
def _(mo):
    mo.md(r"The aim of this notebook is to develop the hypothesis test concerning the [General Aim](../README.md#general-aim) of the project. The interpretation of the test values and the implications related to these results are presented.")
    return


@app.cell
def _(mo):
    mo.md(r"# 1. Beta Distributions of Macronutrient by Diet")
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        For each of the diets, the respective Q-Q plots of the distribution of their macronutrients are presented based on the beta distribution that best fits the data. The use of this distribution is due to the fact that it is bounded to values belonging to $(0,1)$, which are precisely the values taken by the nutritional contributions. For each of the distributions the parameters $alpha$ and $beta$ that determine the shape of a beta distribution are indicated.
    
        In most of the distributions it can be seen that the data fit the distribution adequately, so it could be concluded that those values in the macronutrients were obtained from beta distributions with the given parameters. On the other hand, Q-Q plots can be found where the tails are heavy, that is, they are skewed and it could be concluded that those values behave as outliers for the distribution and for the diet itself
    
        These outliers can be explained by considering how the recipes of each diet should behave statistically, according to [Exploratory Data Analysis](ExploratoryDataAnalysis.py). But even disregarding them, it can be observed that the parameters for the distributions differ across diets, so it is evident that the diets do differ statistically.
        """
    )
    return


@app.cell
def _(Dash, Diets_SubDatasets, src):
    _diet = Dash
    src.PlotBetaDistributions(Diets_SubDatasets.get_group(_diet),_diet.upper())
    return


@app.cell
def _(Diets_SubDatasets, Keto, src):
    _diet = Keto
    src.PlotBetaDistributions(Diets_SubDatasets.get_group(_diet),_diet.capitalize())
    return


@app.cell
def _(Diets_SubDatasets, Mediterranean, src):
    _diet = Mediterranean
    src.PlotBetaDistributions(Diets_SubDatasets.get_group(_diet),_diet.capitalize())
    return


@app.cell
def _(Diets_SubDatasets, Paleo, src):
    _diet = Paleo
    src.PlotBetaDistributions(Diets_SubDatasets.get_group(_diet),_diet.capitalize())
    return


@app.cell
def _(Diets_SubDatasets, Vegan, src):
    _diet = Vegan
    src.PlotBetaDistributions(Diets_SubDatasets.get_group(_diet),_diet.capitalize())
    return


if __name__ == "__main__":
    app.run()
