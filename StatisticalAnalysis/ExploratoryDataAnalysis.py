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
    return (
        Carbs,
        Dash,
        Diet,
        Fat,
        Keto,
        Macronutrients,
        Mediterranean,
        Paleo,
        RANDOM_STATE,
        Recipe,
        Total,
        Vegan,
    )


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
            mo.md('**Statistics by Macronutrient in DASH Diet**'),
            _Statistics,
        ],
    )
    return (Dash_Dataset,)


@app.cell
def _(mo):
    mo.md(r"In both proteins and fats, a positive skewness can be appreciated, causing that the recipes tend to have low contributions of these two macronutrients or, even, recipes with a high contribution are not seen; this because these two macronutrients, when considering foods, are not accompanied by high contributions of micronutrients or rich in nutritional contributions. Therefore, carbohydrates are left as the main source of nutrient-rich foods, so it can be seen how they are distributed throughout the possible porcetanjes that can be taken along with having a tendency to be the predominant macronutrient in this diet.")
    return


@app.cell
def _(Dash, Dash_Dataset, src):
    src.PlotMacronutrients(Dash_Dataset,Dash.upper())
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 3.2. Keto Diet
    
        [[1]](#references) A low-carbohydrate (low-carb) diet is an eating pattern that restricts the intake of carbohydrates, typically replacing them with higher amounts of protein and fat. The ketogenic diet is a form of a lowcarb diet that is high in fat relative to protein and carbohydrate intake. The macronutrient breakdown for a ketogenic diet is 70% fat, 20% protein, and 10% carbohydrate. The goal with ketogenic diet is to induce ketosis, a metabolic state that occurs when a body burns fat for energy instead of glucose, which induces weight loss.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(r"Being a high-fat diet, two main facts could be expected: that fats are the dominant macronutrient or the one with the highest contribution, while carbohydrates are a macronutrient that has a lower presence in the contributions. These two facts can be seen in the summary of the statistics, where an average recipe has $50\%$ of its macronutrients in fats, $30\%$ in proteins and $20\%$ in carbohydrates, where these last two values are consistent with the fact of being a ketogenic diet, that is, low in carbohydrates and rich in fats.")
    return


@app.cell
def _(Diet, Diets_Dataset, Keto, Macronutrients, mo):
    Keto_Dataset = Diets_Dataset.query(f"{Diet} == '{Keto}'")

    _Statistics = Keto_Dataset[Macronutrients].describe().iloc[1:]

    mo.vstack(
        [    
            mo.md('**Statistics by Macronutrient in Keto Diet**'),
            _Statistics,
        ],
    )
    return (Keto_Dataset,)


@app.cell
def _(mo):
    mo.md(r"Carbohydrates have a notorious positive skew, this is related to the fact that the diet favors that the recipes have low contributions of carbohydrates, making that the contributions of this macronutrient are concentrated in low values. Although a negative skew can also be seen in proteins, this is less, because proteins are not harmed, this is due to the fact that this macronutrient is not restricted or limited on the amount or intake of foods associated with this macronutrient; this is reflected in the fact that the distribution is more dispersed over the different values in contrast to the distribution of the values of carbohydrates which is more accumulated in low values.")
    return


@app.cell
def _(Keto, Keto_Dataset, src):
    src.PlotMacronutrients(Keto_Dataset,Keto.capitalize())
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 3.3. Mediterranean Diet
    
        [[1]](#references) The Mediterranean diet is a dietary pattern inspired by the traditional eating habits of countries bordering the Mediterranean Sea. It is characterized by high consumption of fruits, vegetables, whole grains, legumes, nuts, and olive oil; moderate intake of fish and poultry; and low consumption of red meat, processed foods, and sweets. The health benefits of the Mediterranean diet have been investigated in numerous studies.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        When considering the foods that are consumed, it can be seen that there is a diversity among the different products, so that the macronutrients tend to be balanced or that none is the most representative of them. Carbohydrates are the most present macronutrient in this diet, with an average contribution of $42\%$ of the total macronutrients, and this is mainly due to the food groups that are most consumed.
    
        While $28\%$ and $30\%$ of the average contributions are proteins and fats, respectively, these values represent how this diet tends to be rich and diversified in different products and foods.
        """
    )
    return


@app.cell
def _(Diet, Diets_Dataset, Macronutrients, Mediterranean, mo):
    Mediterranean_Dataset = Diets_Dataset.query(f"{Diet} == '{Mediterranean}'")

    _Statistics = Mediterranean_Dataset[Macronutrients].describe().iloc[1:]

    mo.vstack(
        [    
            mo.md('**Statistics by Macronutrient in Mediterranean Diet**'),
            _Statistics,
        ],
    )
    return (Mediterranean_Dataset,)


@app.cell
def _(mo):
    mo.md(r"Although they do not have a notorious skew, the distribution of proteins and fats are skewed because, although representative foods of these groups are consumed, they are not so present in this diet; therefore, they tend to have lower values. In contrast with carbohydrates, which have a higher consumption of foods rich in this macronutrient, they are even more dispersed and presented in different proportions or levels of contributions. This can be appreciated when considering that it has a negative skew, so that the recipes tend to have high carbohydrate contributions.")
    return


@app.cell
def _(Mediterranean, Mediterranean_Dataset, src):
    src.PlotMacronutrients(Mediterranean_Dataset,Mediterranean.capitalize())
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 3.4. Paleo Diet
    
        [[1]](#references) The Paleo diet, also known as the Paleolithic diet or caveman diet, is a dietary approach that aims to mimic the eating habits of our ancient ancestors from the Paleolithic era. It emphasizes consuming whole, unprocessed foods that would have been available to early humans, such as lean meats, fish, fruits, vegetables, nuts, and seeds, and excluding grains, legumes, dairy products, processed foods, and added sugars. Although the Paleo diet has gained popularity, it is important to note that scientific evidence supporting its specific health benefits is limited.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        When considering the origin of the foods that are consumed, the distribution of macronutrient contributions depends on the availability of these foods or natural products; where the easiest to obtain are all those that are not of animal origin, that is, of vegetable origin. Therefore, an average recipe of this tends to have a higher intake or contribution of these two macronutrients, specifically, $37% and $38% of the macronutrients consumed are carbohydrates and fats, respectively.
    
        These values allow us to show how the macronutrients and the food groups that are consumed are related, with those that are high in carbohydrates and fats being the most present in this diet. On the other hand, proteins are in less presence because protein-rich foods require more energy and effort to get them; leaving them to be the $25% of the macronutrients consumed.
        """
    )
    return


@app.cell
def _(Diet, Diets_Dataset, Macronutrients, Paleo, mo):
    Paleo_Dataset = Diets_Dataset.query(f"{Diet} == '{Paleo}'")

    _Statistics = Paleo_Dataset[Macronutrients].describe().iloc[1:]

    mo.vstack(
        [    
            mo.md('**Statistics by Macronutrient in Mediterranean Diet**'),
            _Statistics,
        ],
    )
    return (Paleo_Dataset,)


@app.cell
def _(mo):
    mo.md(r"In the three distributions a positive skew can be appreciated, this is linked to the fact that foods, in their natural state, do not tend to have high contributions of a single macronutrient. Therefore, when preparing a recipe, it tends to have a more uniform distribution of nutritional contributions, making the different macronutrients equally present; except for proteins, which have a more noticeable positive skew and their values are more concentrated in low values.")
    return


@app.cell
def _(Paleo, Paleo_Dataset, src):
    src.PlotMacronutrients(Paleo_Dataset,Paleo.capitalize())
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 3.4. Vegan Diet
    
        [[1]](#references) The vegan diet is a plant-based dietary pattern that excludes the consumption of all animal products, including meat, poultry, seafood, dairy products, eggs, and honey. It focuses on consuming a variety of plant-based foods, such as fruits, vegetables, grains, legumes, nuts, and seeds. Scientific research has explored the health benefits of vegan diets and shown the benefits are similar to the health benefits of vegetarians diets,
        """
    )
    return


@app.cell
def _(mo):
    mo.md(r"Being a diet that favors only the consumption of foods and products of vegetable origin, protein intake will tend to low values, while carbohydrates are in the opposite situation, due to the foods themselves that are consumed. This can be appreciated when considering the average values of the macronutrients that are consumed in this diet, specifically: $59\%$ are carbohydrates, $15\%$ are proteins and $26\%$ are fats. These last values allow us to conclude that this diet requires a better balance and control over the macronutrients that are consumed, since it only favors a single macronutrient (carbohydrates) while the consumption of the other two is impaired.")
    return


@app.cell
def _(Diet, Diets_Dataset, Macronutrients, Vegan, mo):
    Vegan_Dataset = Diets_Dataset.query(f"{Diet} == '{Vegan}'")

    _Statistics = Vegan_Dataset[Macronutrients].describe().iloc[1:]

    mo.vstack(
        [    
            mo.md('**Statistics by Macronutrient in Vegan Diet**'),
            _Statistics,
        ],
    )
    return (Vegan_Dataset,)


@app.cell
def _(mo):
    mo.md(r"The notorious positive skew presented by the distribution of proteins shows the almost null intake of foods rich in proteins in this diet, that is, the recipes will have low protein intake. While carbohydrates will be favored to be the predominant macronutrient of the recipes, because it has a negative skew, and this is related to the exclusive consumption of foods of vegetable origin.")
    return


@app.cell
def _(Vegan, Vegan_Dataset, src):
    src.PlotMacronutrients(Vegan_Dataset,Vegan.capitalize())
    return


@app.cell
def _(mo):
    mo.md(r"# 4. Analysis of Correlations")
    return


@app.cell
def _(mo):
    mo.md(r"## 4.1. DASH Diet")
    return


@app.cell
def _(mo):
    mo.md(r"Carbohydrates have a strong negative correlation with the other macronutrients, this may be due to the fact that in this diet the recipes tend to have high carbohydrate intake or to consume foods rich in this macronutrient. Therefore, the increase in the amount of carbohydrates in a recipe generates a decompensation in the other two macronutrients, so that if more fruits or vegetables are consumed, the consumption of proteins and foods rich in fats is lowered.")
    return


@app.cell
def _(Dash, Dash_Dataset, src):
    src.PlotRegressions(Dash_Dataset,Dash.upper())
    return


@app.cell
def _(mo):
    mo.md(r"By using the first two PCA-generated components of the dataset, a two-dimensional projection of the distribution of the recipes is generated, which allows us to observe how they accumulate more towards the regions where they tend to have a greater presence of carbohydrates. Thus, PC1 explains how the carbohydrate contributions of the different recipes vary, while PC2 explains the variance or distribution of the remaining two macronutrients.")
    return


@app.cell
def _(Carbs, Dash, Dash_Dataset, src):
    src.PlotCorrelationsPCA(Dash_Dataset,Dash.upper(),Carbs)
    return


@app.cell
def _(mo):
    mo.md(r"## 4.2. Keto Diet")
    return


@app.cell
def _(mo):
    mo.md(r"Knowing that this diet favors a high fat intake and a low carbohydrate intake, this generates negative correlations. This is due to the fact that this diet tries to favor the consumption of foods rich in fats, so that if a recipe is rich in this macronutrient, the other two macronutrients tend to go down, where carbohydrates will tend to take lower values than proteins.")
    return


@app.cell
def _(Keto, Keto_Dataset, src):
    src.PlotRegressions(Keto_Dataset,Keto.capitalize())
    return


@app.cell
def _(mo):
    mo.md(r"By using PCA, it is possible to generate the projection of the recipes on the plane, where it can be seen how the recipes are distributed according to their macronutrient contributions. Specifically, by having similar variances and correlations, the principal components of PCA do not generate a specific or subtle distinction between the interaction between macronutrients, but by using PC1 it is possible to explain the variability that the recipes have on the contributions in fats, making PC2 show how the other two macronutrients interact in the contributions of a recipe.")
    return


@app.cell
def _(Fat, Keto, Keto_Dataset, src):
    src.PlotCorrelationsPCA(Keto_Dataset,Keto.capitalize(),Fat)
    return


@app.cell
def _(mo):
    mo.md(r"## 4.3. Mediterranean Diet")
    return


@app.cell
def _(mo):
    mo.md(r"When considering the types of foods that are consumed in this diet, it can be assumed that they are rich in mraconutrients and, specifically, rich in carbohydrates, so this macronutrient determines how the contributions of the other two will be. This is reflected when considering the correlations, which are high and negative values, so the trend of increasing carbohydrates will cause proteins and fats to decrease in the same sense; therefore, carbohydrates determine how the nutritional contributions of a recipe will be.")
    return


@app.cell
def _(Mediterranean, Mediterranean_Dataset, src):
    src.PlotRegressions(Mediterranean_Dataset,Mediterranean.capitalize())
    return


@app.cell
def _(mo):
    mo.md(r"When transforming the dataset under PCA, the projection in the plane of the distribution of the recipes based on their nutritional contributions is created. The PC1 allows to explain how the carbohydrate contributions are distributed, or how the variation of this macronutrient alters the distribution of the nutrinional contributions; while PC2, allows to show the distribution of the contributions of proteins and fats.")
    return


@app.cell
def _(Carbs, Mediterranean, Mediterranean_Dataset, src):
    src.PlotCorrelationsPCA(Mediterranean_Dataset,Mediterranean.capitalize(),Carbs)
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
