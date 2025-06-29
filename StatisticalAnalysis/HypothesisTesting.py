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
    mo.md(
        r"""
        The aim of this notebook is to develop the hypothesis test concerning the [General Aim](../README.md#general-aim) of the project. The interpretation of the test values and the implications related to these results are presented.
    
        In the section [1. Beta Distributions of Macronutrients by Diet](#1-beta-distributions-of-macronutrients-by-diet) the Q-Q plots of the different distributions are presented to show the fit of the data to a theoretical beta distribution, in order to show how each macronutrient in the different diets follows certain patterns or trends in their contributions or values. In general, it allows to reinforce the statistical discussion on diets presented in [Exploratory Data Analysis](ExploratoryDataAnalysis.py).
    
        Finally, in [2. Hypothesis Test for Difference between Diets](#2-hypothesis-test-for-difference-between-diets), the results obtained to test the differences between diets at the macronutrient level are presented, from which it is concluded that the diets differ significantly. In addition, the means of the test statistics are presented in order to define a notion of distance between diets, this allows to illustrate how similar are diets based on the macronutrient contributions that characterize each one.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(r"# 1. Beta Distributions of Macronutrients by Diet")
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


@app.cell
def _(mo):
    mo.md(r"# 2. Hypothesis Test for Difference between Diets")
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        As the aim of the project is to test whether diets are different from a statistical perspective, it becomes equivalent to test that their macronutrient distributions are different, that is, to test that each diet follows certain patterns of macronutrient and/or food consumption. To test this, use is made of the [Kolmogorov-Smirnov test](https://en.wikipedia.org/wiki/Kolmogorov%E2%80%93Smirnov_test) with two samples.
    
        Using this test allows us to show statistically how much the distributions of some macronutrient differ in two different diets. Therefore, it is applied for each pair of diets and for each macronutrient. For each test its statistic and p-value are obtained. Using the p-values together with a significance $\alpha$ of $5\%$, the amount of significant differences per macronutrient can be determined, which in the table below can show that all diets differ significantly from all others.
    
        Using the statistics obtained for each test, a notion of distance between diets can be generated by averaging the statistics obtained for the macronutrients and generating the second table. With these averages it is possible to measure how similar two diets are. 
    
        Using these averages one could group the recipes as follows: DASH and Vegan, Paleo and Mediterranean, Keto. These groups can be explained by looking at which foods and products are most consumed in each diet along with the macronutrients themselves which are exposed in [Exploratory Data Analysis](ExploratoryDataAnalysis.py).
        """
    )
    return


@app.cell
def _(Diets_Dataset, src):
    # Applying the hypothesis test

    StatisticResults , PValueResults = src.TestDifferenceDiets(Diets_Dataset)
    return PValueResults, StatisticResults


@app.cell
def _(PValueResults, mo):
    mo.vstack(
        [
            mo.md("**Count of Significant Differences**"),
            PValueResults
        ]
    )
    return


@app.cell
def _(StatisticResults, mo):
    mo.vstack(
        [
            mo.md("**Mean of Test Statistics**"),
            StatisticResults
        ]
    )
    return


if __name__ == "__main__":
    app.run()
