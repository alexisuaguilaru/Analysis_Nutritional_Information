import marimo

__generated_with = "0.13.10"
app = marimo.App()


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""# 0. Carga del Dataset y Otro Código""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## 0.1 Importar Librerías y Funciones""")
    return


@app.cell
def _():
    # Importar librerías
    import marimo as mo

    import pandas as pd
    import numpy as np

    import matplotlib.pyplot as plt
    import seaborn as sns
    return mo, pd


@app.cell
def _():
    # Importar funciones varias

    import Source as src
    return (src,)


@app.cell
def _():
    # Definiendo variables y constantes

    Color_Palette = ['green','red','gold']
    Color_Map = 'seismic'

    Macronutrients = ['Carbs','Protein','Fat']
    Diets = ['dash', 'keto', 'mediterranean', 'paleo', 'vegan']
    Cuisine = 'Cuisine_type'
    Diet = 'Diet_type'
    Total = 'Total_macronutrients'
    Recipe = 'Recipe_name'

    MapTranslate = {
        'Carbs' : 'Carbohidratos',
        'Protein' : 'Proteínas',
        'Fat' : 'Grasas',
    }
    InverseMacronutrient = {
        'Carbs' : 0,
        'Protein' : 1,
        'Fat' : 2,
    }

    RANDOM_STATE = 8013
    return Cuisine, Diet, Macronutrients, Recipe, Total


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## 0.2 Carga de Datos""")
    return


@app.cell
def _(pd):
    # Carga de datos

    macronutrients = ['Carbs(g)','Protein(g)','Fat(g)']

    Diets_Dataset = pd.read_csv('Datasets/Diets_Dataset.csv')
    Diets_Dataset.drop(columns=['Extraction_day','Extraction_time'],inplace=True)
    Diets_Dataset.rename(columns={macronutrient : macronutrient[:-3] for macronutrient in macronutrients},inplace=True)
    return (Diets_Dataset,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""# 3. Presentación de los Datos""")
    return


@app.cell
def _(Diets_Dataset):
    # Ejemplos de registros del conjunto de datos

    Diets_Dataset
    return


@app.cell
def _(Diets_Dataset):
    # Valore únicos por variable en el conjunto de datos

    Diets_Dataset.apply(lambda column: column.unique().shape[0],axis=0)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""# 4. Estadística Descriptiva""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## 4.1 Preprocesamiento (Transformación) de los Datos""")
    return


@app.cell
def _(Diets_Dataset, Macronutrients, Total):
    # Normalización de los Macronutrientes

    Diets_Dataset[Total] = Diets_Dataset[Macronutrients].sum(axis=1)
    Diets_Dataset[Macronutrients] /= Diets_Dataset[Total].to_numpy()[:,None]
    return


@app.cell
def _(Cuisine, Diet, Diets_Dataset, Recipe):
    # Recetas por Dieta y Cocina

    Diets_Dataset.pivot_table(Recipe,Cuisine,Diet,'count',margins=True,margins_name='Total').sort_values('Total')
    return


@app.cell
def _(Cuisine, Diets_Dataset):
    # Agrupación de Tipos de Cocina por Regiones Geográficas

    GroupsCuisine = {
        'american' : 0,
        'mediterranean' : 1,
        'world' : 2,
        'mexican' : 3,
        'south american' : 3,
        'caribbean' : 3,
        'italian' : 4, 
        'french' : 4,
        'nordic' : 4,
        'eastern europe' : 4,
        'central europe' : 4,
        'kosher' : 4,
        'british' : 4,
        'chinese' : 5,
        'indian' : 5,
        'south east asian' : 5,
        'middle eastern' : 5,
        'asian' : 5,
        'japanese' : 5,
    }

    groups_names = {
        0 : 'american',
        1 : 'mediterranean',
        2 : 'world',
        3 : 'latin american',
        4 : 'european',
        5 : 'asian'
    }

    Diets_Dataset[Cuisine] = Diets_Dataset[Cuisine].apply(GroupsCuisine.get).apply(groups_names.get)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## 4.3 Visión General de los Datos""")
    return


@app.cell
def _(Diets_Dataset, src):
    # Calculo de las medidas de tendencia central, dispersión y asimetría 

    src.SummaryMeasures(Diets_Dataset)
    return


@app.cell
def _(Cuisine, Diet, Diets_Dataset, Recipe):
    Diets_Dataset.pivot_table(Recipe,Cuisine,Diet,'count')
    return


@app.cell
def _(Diets_Dataset, src):
    VisionGeneral_1 = src.Plot_DistributionMacronutrients(Diets_Dataset)
    src.SaveFig(VisionGeneral_1,'EDA','VisionGeneral_1')

    VisionGeneral_1
    return


@app.cell
def _(Diets_Dataset, src):
    VisionGeneral_2 = src.Plot_DistributionMacronutientsByCuisine(Diets_Dataset)
    src.SaveFig(VisionGeneral_2,'EDA','VisionGeneral_2')

    VisionGeneral_2
    return


@app.cell
def _(Cuisine, Diets_Dataset):
    Diets_Dataset.query(f"{Cuisine} != 'world'",inplace=True)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## 4.4 Dieta DASH""")
    return


@app.cell
def _(Diet, Diets_Dataset, src):
    dash = 'dash'

    src.SummaryMeasures(Diets_Dataset.query(f'{Diet} == @dash'))
    return


@app.cell
def _(Diet, Diets_Dataset, src):
    PlotDash_1 = src.Plot_DistributionMacronutrients(Diets_Dataset.query(f'{Diet} == @dash'))
    src.SaveFig(PlotDash_1,'EDA','Dash_1')

    PlotDash_1
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""# 5. Análisis Bivariado""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""# 6. Muestreo e Intervalos de Confianza""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""# 7. Pruebas de Hipótesis""")
    return


if __name__ == "__main__":
    app.run()
