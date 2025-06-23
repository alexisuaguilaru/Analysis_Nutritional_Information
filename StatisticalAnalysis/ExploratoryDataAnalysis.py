import marimo

__generated_with = "0.13.15"
app = marimo.App(width="medium")


@app.cell
def _():
    # Import required libraries

    import marimo as mo

    import pandas as pd
    import numpy as np

    import seaborn as sns
    import matplotlib.pyplot as plt
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

    Recipe = 'Recipe_name'

    RANDOM_STATE = 8013
    return Diet, Macronutrients, RANDOM_STATE, Recipe


@app.cell
def _(mo):
    mo.md(r"# Introduction")
    return


@app.cell
def _(mo):
    mo.md(r"# 1. Load Dataset and First Exploration")
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        The dataset of interest consists of five features that represent the following:
    
        * `Diet_type` [string]: Type of diet to which a recipe belongs
    
        * `Recipe_name` [string]: Name of the recipe
    
        * `Protein` [float]: Grams of protein provided by a recipe
    
        * `Carbs` [float]: Grams of carbohydrates provided by a recipe
    
        * `Fat` [float]: Grams of fat provided by a recipe
    
        The dataset consists of `7806` recipes from five different diets: [DASH](https://en.wikipedia.org/wiki/DASH_diet), [Keto](https://en.wikipedia.org/wiki/Ketogenic_diet), [Mediterranean](https://en.wikipedia.org/wiki/Mediterranean_diet), [Paleo](https://en.wikipedia.org/wiki/Paleolithic_diet) and [Vegan](https://en.wikipedia.org/wiki/Veganism). Considering the distribution of the recipes by diet, it is found that they are not uniformly distributed and, therefore, the dataset is unbalanced with respect to `Diet_type`.
    
        The values of the contributions of the three macronutrients can take a wide range of values, so it becomes difficult to generate a comparison of the nutritional contributions of the recipes in the different diets. To address this problem, a transformation will be applied to the values.
        """
    )
    return


@app.cell
def _(Macronutrients, pd):
    # Loading dataset

    Diets_Dataset = pd.read_csv('./Datasets/Diets_Dataset.csv')
    Diets_Dataset.drop(columns=['Cuisine_type','Extraction_day','Extraction_time'],inplace=True)
    Diets_Dataset.rename(columns={macronutrient+'(g)':macronutrient for macronutrient in Macronutrients},inplace=True)
    return (Diets_Dataset,)


@app.cell
def _(Diets_Dataset, mo):
    mo.vstack(
        [    
            mo.md('**Data Types of Each Feature**'),
            Diets_Dataset.dtypes,
        ],
        align='center',
    )
    return


@app.cell
def _(Diet, Diets_Dataset, RANDOM_STATE, mo):
    _SampleRecipes = Diets_Dataset.groupby(Diet).sample(2,random_state=RANDOM_STATE)

    mo.vstack(
        [    
            mo.md('**Example of Recipes**'),
            _SampleRecipes,
        ],
        align='center',
    )
    return


@app.cell
def _(Diet, Diets_Dataset, Recipe, mo):
    _RecipesByDiet = Diets_Dataset.groupby(Diet)[Recipe].count()
    _RecipesByDiet.loc['Total'] = _RecipesByDiet.sum()

    mo.vstack(
        [    
            mo.md('**Recipes By Diet**'),
            _RecipesByDiet,
        ],
        align='center',
    )
    return


if __name__ == "__main__":
    app.run()
