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
    return mo, pd


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
    return


@app.cell
def _(pd):
    # Loading dataset

    Diets_Dataset = pd.read_csv('./Datasets/Diets_Dataset_Clean.csv')
    return


@app.cell
def _(mo):
    mo.md(r"# Introduction")
    return


@app.cell
def _(mo):
    mo.md(r"The aim of this notebook is to develop the hypothesis test concerning the [General Aim](../README.md#general-aim) of the project. The interpretation of the test values and the implications related to these results are presented.")
    return


if __name__ == "__main__":
    app.run()
