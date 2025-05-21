import marimo

__generated_with = "0.13.10"
app = marimo.App()


@app.cell
def _(mo):
    mo.md(r"# 0. Carga del Dataset y Otro Código")
    return


@app.cell
def _(mo):
    mo.md(r"## 0.1 Importar Librerías y Funciones")
    return


@app.cell
def _():
    # Importar librerías
    import marimo as mo

    import pandas as pd
    import numpy as np

    import matplotlib.pyplot as plt
    import seaborn as sns
    return mo, pd, plt


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
    return Cuisine, Diet, Diets, Macronutrients, Recipe, Total


@app.cell
def _(mo):
    mo.md(r"## 0.2 Carga de Datos")
    return


@app.cell
def _(pd):
    # Carga de datos

    macronutrients = ['Carbs(g)','Protein(g)','Fat(g)']

    Diets_Dataset = pd.read_csv('Datasets/Diets_Dataset.csv')
    Diets_Dataset.drop(columns=['Extraction_day','Extraction_time'],inplace=True)
    Diets_Dataset.rename(columns={macronutrient : macronutrient[:-3] for macronutrient in macronutrients},inplace=True)
    return (Diets_Dataset,)


@app.cell
def _(mo):
    mo.md(r"# 3. Presentación de los Datos")
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


@app.cell
def _(mo):
    mo.md(r"# 4. Estadística Descriptiva")
    return


@app.cell
def _(mo):
    mo.md(r"## 4.1 Preprocesamiento (Transformación) de los Datos")
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


@app.cell
def _(mo):
    mo.md(r"## 4.3 Visión General de los Datos")
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
    VisionGeneral_2 = src.Plot_DistributionMacronutrientsByCuisine(Diets_Dataset)
    src.SaveFig(VisionGeneral_2,'EDA','VisionGeneral_2')

    VisionGeneral_2
    return


@app.cell
def _(Cuisine, Diets_Dataset):
    Diets_Dataset.query(f"{Cuisine} != 'world'",inplace=True)
    return


@app.cell
def _(mo):
    mo.md(r"## 4.4 Dieta DASH")
    return


@app.cell
def _(Diet, Diets_Dataset, src):
    dash = 'dash'

    src.SummaryMeasures(Diets_Dataset.query(f'{Diet} == @dash'))
    return


@app.cell
def _(Diet, Diets_Dataset, src):
    PlotDash_1 = src.Plot_DistributionMacronutrients(Diets_Dataset.query(f'{Diet} == @dash'),'DASH')
    src.SaveFig(PlotDash_1,'EDA','Dash_1')

    PlotDash_1
    return


@app.cell
def _(Diet, Diets_Dataset, src):
    PlotDash_2 = src.Plot_DistributionMacronutrientsByCuisine(Diets_Dataset.query(f'{Diet} == @dash'),'DASH')
    src.SaveFig(PlotDash_2,'EDA','Dash_2')

    PlotDash_2
    return


@app.cell
def _(mo):
    mo.md(r"## 4.5 Dieta Keto")
    return


@app.cell
def _(Diet, Diets_Dataset, src):
    keto = 'keto'

    src.SummaryMeasures(Diets_Dataset.query(f'{Diet} == @keto'))
    return


@app.cell
def _(Diet, Diets_Dataset, src):
    PlotKeto_1 = src.Plot_DistributionMacronutrients(Diets_Dataset.query(f'{Diet} == @keto'),'Keto')
    src.SaveFig(PlotKeto_1,'EDA','Keto_1')

    PlotKeto_1
    return


@app.cell
def _(Diet, Diets_Dataset, src):
    PlotKeto_2 = src.Plot_DistributionMacronutrientsByCuisine(Diets_Dataset.query(f'{Diet} == @keto'),'Keto')
    src.SaveFig(PlotKeto_2,'EDA','Keto_2')

    PlotKeto_2
    return


@app.cell
def _(mo):
    mo.md(r"## 4.6 Dieta Mediterránea")
    return


@app.cell
def _(Diet, Diets_Dataset, src):
    mediterranean = 'mediterranean'

    src.SummaryMeasures(Diets_Dataset.query(f'{Diet} == @mediterranean'))
    return


@app.cell
def _(Diet, Diets_Dataset, src):
    PlotMediterranean_1 = src.Plot_DistributionMacronutrients(Diets_Dataset.query(f'{Diet} == @mediterranean'),'Mediterranean')
    src.SaveFig(PlotMediterranean_1,'EDA','Mediterranean_1')

    PlotMediterranean_1
    return


@app.cell
def _(Diet, Diets_Dataset, src):
    PlotMediterranean_2 = src.Plot_DistributionMacronutrientsByCuisine(Diets_Dataset.query(f'{Diet} == @mediterranean'),'Mediterranean')
    src.SaveFig(PlotMediterranean_2,'EDA','Mediterranean_2')

    PlotMediterranean_2
    return


@app.cell
def _(mo):
    mo.md(r"## 4.7 Dieta Paleo")
    return


@app.cell
def _(Diet, Diets_Dataset, src):
    paleo = 'paleo'

    src.SummaryMeasures(Diets_Dataset.query(f'{Diet} == @paleo'))
    return


@app.cell
def _(Diet, Diets_Dataset, src):
    PlotPaleo_1 = src.Plot_DistributionMacronutrients(Diets_Dataset.query(f'{Diet} == @paleo'),'Paleo')
    src.SaveFig(PlotPaleo_1,'EDA','Paleo_1')

    PlotPaleo_1
    return


@app.cell
def _(Diet, Diets_Dataset, src):
    PlotPaleo_2 = src.Plot_DistributionMacronutrientsByCuisine(Diets_Dataset.query(f'{Diet} == @paleo'),'Paleo')
    src.SaveFig(PlotPaleo_2,'EDA','Paleo_2')

    PlotPaleo_2
    return


@app.cell
def _(mo):
    mo.md(r"## 4.8 Dieta Vegana")
    return


@app.cell
def _(Diet, Diets_Dataset, src):
    vegan = 'vegan'

    src.SummaryMeasures(Diets_Dataset.query(f'{Diet} == @vegan'))
    return


@app.cell
def _(Diet, Diets_Dataset, src):
    PlotVegan_1 = src.Plot_DistributionMacronutrients(Diets_Dataset.query(f'{Diet} == @vegan'),'Vegan')
    src.SaveFig(PlotVegan_1,'EDA','Vegan_1')

    PlotVegan_1
    return


@app.cell
def _(Diet, Diets_Dataset, src):
    PlotVegan_2 = src.Plot_DistributionMacronutrientsByCuisine(Diets_Dataset.query(f'{Diet} == @vegan'),'Vegan')
    src.SaveFig(PlotVegan_2,'EDA','Vegan_2')

    PlotVegan_2
    return


@app.cell
def _(mo):
    mo.md(r"# 5. Análisis Bivariado")
    return


@app.cell
def _(Diets_Dataset, src):
    PlotCorrelation = src.Plot_CorrelationMacronutrients(Diets_Dataset)
    src.SaveFig(PlotCorrelation,'Bivariado','Correlation')

    PlotCorrelation
    return


@app.cell
def _(Diet, Diets, Diets_Dataset, Macronutrients, pd):
    dataset_biv = {feature : [] for feature in ['Dieta','Macronutrients','Centroide','Covarianza','Coeficiente']}

    for diet in Diets:
        data_diet = Diets_Dataset.query(f'{Diet} == @diet')
        for macro_x , macro_y in [(Macronutrients[0],Macronutrients[1]),(Macronutrients[0],Macronutrients[2]),(Macronutrients[1],Macronutrients[2])]:
            dataset_biv['Dieta'].append(diet)
            dataset_biv['Macronutrients'].append(f'({macro_x},{macro_y})')

            centroide = data_diet[[macro_x,macro_y]].mean().to_numpy()
            dataset_biv['Centroide'].append(centroide)

            covariance = data_diet[[macro_x,macro_y]].cov(ddof=1).iloc[0,1]
            dataset_biv['Covarianza'].append(covariance)

            correlation = data_diet[[macro_x,macro_y]].corr(method='pearson').iloc[0,1]
            dataset_biv['Coeficiente'].append(correlation)

    print(pd.DataFrame(dataset_biv).to_latex())
    return


@app.cell
def _(Diet, Diets, Diets_Dataset, plt, src):
    for diet_reg in Diets:
        case_str_reg = str.capitalize if diet_reg != 'dash' else str.upper
        PlotRegression = src.Plot_RegressionMacronutrients(Diets_Dataset.query(f'{Diet} == @diet_reg'),case_str_reg(diet_reg))
        src.SaveFig(PlotRegression,'Bivariado','Regression'+diet_reg.capitalize())

    plt.show()
    return


@app.cell
def _(mo):
    mo.md(r"# 6. Muestreo e Intervalos de Confianza")
    return


@app.cell
def _(mo):
    mo.md(r"# 7. Pruebas de Hipótesis")
    return


if __name__ == "__main__":
    app.run()
