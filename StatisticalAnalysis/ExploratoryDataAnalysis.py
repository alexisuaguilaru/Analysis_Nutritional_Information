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
    return Dash, Diet, Macronutrients, RANDOM_STATE, Recipe, Total


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

    Diets_Dataset_Raw = pd.read_csv('./Datasets/Diets_Dataset.csv')
    Diets_Dataset_Raw.drop(columns=['Cuisine_type','Extraction_day','Extraction_time'],inplace=True)
    Diets_Dataset_Raw.rename(columns={macronutrient+'(g)':macronutrient for macronutrient in Macronutrients},inplace=True)
    return (Diets_Dataset_Raw,)


@app.cell
def _(Diets_Dataset_Raw, mo):
    mo.vstack(
        [    
            mo.md('**Data Types of Each Feature**'),
            Diets_Dataset_Raw.dtypes,
        ],
    )
    return


@app.cell
def _(Diet, Diets_Dataset_Raw, RANDOM_STATE, mo):
    _SampleRecipes = Diets_Dataset_Raw.groupby(Diet).sample(2,random_state=RANDOM_STATE)

    mo.vstack(
        [    
            mo.md('**Example of Recipes**'),
            _SampleRecipes,
        ],
    )
    return


@app.cell
def _(Diet, Diets_Dataset_Raw, Recipe, mo):
    _RecipesByDiet = Diets_Dataset_Raw.groupby(Diet)[Recipe].count()
    _RecipesByDiet.loc['Total'] = _RecipesByDiet.sum()

    mo.vstack(
        [    
            mo.md('**Recipes By Diet**'),
            _RecipesByDiet,
        ],
    )
    return


@app.cell
def _(mo):
    mo.md(r"# 2. Transformation of Macronutrient Values")
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        As mentioned in [previous section](#1-load-dataset-and-first-exploration), it is difficult to compare the nutritional contributions of different recipes across diets without being biased because some diets tend to have higher macronutrient contributions than others. Therefore, it becomes relevant to use a consistent scale across different macronutrients and diets.
    
        Hence, when considering the relative contributions of each macronutrient in a recipe, the values are limited to a well-defined range, $[0,1]$, so that only how the macronutrient distributions change across diets is considered. And this way in which they change becomes the fundamental factor in determining whether two diets behave in the same way or not, this is, whether they follow similar patterns in their nutritional contributions.
        """
    )
    return


@app.cell
def _(Diets_Dataset_Raw, Macronutrients, mo):
    _RangeMacronutrientValues = Diets_Dataset_Raw[Macronutrients].describe().loc[['min','25%','50%','75%','max']]

    mo.vstack(
        [    
            mo.md('**Ranges of Macronutrient Values**'),
            _RangeMacronutrientValues,
        ],
    )
    return


@app.cell
def _(Diets_Dataset_Raw, Macronutrients, Total):
    # Transforming macronutrient values

    Diets_Dataset = Diets_Dataset_Raw.copy()
    Diets_Dataset[Total] = Diets_Dataset[Macronutrients].sum(axis=1)

    Diets_Dataset[Macronutrients] /= Diets_Dataset[Total].to_numpy()[:,None]
    return (Diets_Dataset,)


@app.cell
def _(Diet, Diets_Dataset, RANDOM_STATE, mo):
    _SampleRecipes = Diets_Dataset.groupby(Diet).sample(2,random_state=RANDOM_STATE)

    mo.vstack(
        [    
            mo.md('**Example of Recipes after Transformation**'),
            _SampleRecipes,
        ],
    )
    return


@app.cell
def _(mo):
    mo.md(r"# 3. Analysis of Statistics by Type of Diet")
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 3.1. DASH Diet
    
        [[1]](#references) The Dietary Approaches to Stop Hypertension (DASH) diet is a dietary pattern specifically designed to help lower blood pressure and promote overall heart health. It emphasizes consuming a variety of nutrient-rich foods, including fruits, vegetables, whole grains, lean proteins, and low-fat dairy products, and limiting the intake of sodium, saturated fats, and added sugars. Scientific research has demonstrated the effectiveness of the DASH diet in reducing blood pressure and improving cardiovascular health.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        Being a diet that tends to be healthy, it shows that it favors the intake of carbohydrates, because carbohydrates are the most representative macronutrient in this diet. This is explained by considering that vegetables and fruits are the main food groups that are present in this diet, and from which the greatest amount of micronutrients are obtained. Leaving foods with low nutritional contributions, such as those associated with fats and proteins, in second place.
    
        The above is reflected when considering how an average recipe of this diet tends to have $55\%$ of its macronutrients as carbohydrates, $20\%$ in proteins and $25\%$ in fats. Emphasizing that this fat intake is originated by foods with fats and oils beneficial to health, such as omegas.
        """
    )
    return


@app.cell
def _(Dash, Diet, Diets_Dataset, Macronutrients, mo):
    Dash_Dataset = Diets_Dataset.query(f"{Diet} == '{Dash}'")

    _Statistics = Dash_Dataset[Macronutrients].describe().iloc[1:]

    mo.vstack(
        [    
            mo.md('**Statistics by Macronutrien in DASH Diet**'),
            _Statistics,
        ],
    )
    return (Dash_Dataset,)


@app.cell
def _(mo):
    mo.md(r"In both proteins and fats, a positive bias can be appreciated, causing that the recipes tend to have low contributions of these two macronutrients or, even, recipes with a high contribution are not seen; this because these two macronutrients, when considering foods, are not accompanied by high contributions of micronutrients or rich in nutritional contributions. Therefore, carbohydrates are left as the main source of nutrient-rich foods, so you can see how they are distributed throughout the possible porcetanjes that can be taken along with having a tendency to be the predominant macronutrient in this diet.")
    return


@app.cell
def _(Dash, Dash_Dataset, src):
    src.PlotMacronutrients(Dash_Dataset,Dash.upper())
    return


@app.cell
def _(mo):
    mo.md(r"# References")
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        * [1] F. F. Marvasti, "Popular Diets and Health", *Culinary Medicine*
    
        *
        """
    )
    return


if __name__ == "__main__":
    app.run()
