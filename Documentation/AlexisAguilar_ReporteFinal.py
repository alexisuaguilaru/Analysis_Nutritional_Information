import marimo

__generated_with = "0.13.11"
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
    from scipy import stats

    import matplotlib.pyplot as plt
    import seaborn as sns
    return mo, np, pd, plt


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
    return Cuisine, Diet, Diets, Macronutrients, RANDOM_STATE, Recipe, Total


@app.cell
def _(mo):
    mo.md(r"## 0.2 Carga de Datos")
    return


@app.cell
def _(pd):
    # Carga de datos

    macronutrients = ['Carbs(g)','Protein(g)','Fat(g)']

    Diets_Dataset__0 = pd.read_csv('Datasets/Diets_Dataset.csv')
    Diets_Dataset__0.drop(columns=['Extraction_day','Extraction_time'],inplace=True)
    Diets_Dataset__0.rename(columns={macronutrient : macronutrient[:-3] for macronutrient in macronutrients},inplace=True)
    return (Diets_Dataset__0,)


@app.cell
def _(mo):
    mo.md(r"# 3. Presentación de los Datos")
    return


@app.cell
def _(Diets_Dataset__0):
    # Ejemplos de registros del conjunto de datos

    Diets_Dataset__0
    return


@app.cell
def _(Diets_Dataset__0):
    # Valore únicos por variable en el conjunto de datos

    Diets_Dataset__0.apply(lambda column: column.unique().shape[0],axis=0)
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
def _(Diets_Dataset__0, Macronutrients, Total):
    # Normalización de los Macronutrientes
    Diets_Dataset__1 = Diets_Dataset__0.copy()
    Diets_Dataset__1[Total] = Diets_Dataset__1[Macronutrients].sum(axis=1)
    Diets_Dataset__1[Macronutrients] /= Diets_Dataset__1[Total].to_numpy()[:,None]
    return (Diets_Dataset__1,)


@app.cell
def _(Cuisine, Diet, Diets_Dataset__1, Recipe):
    # Recetas por Dieta y Cocina

    Diets_Dataset__1.pivot_table(Recipe,Cuisine,Diet,'count',margins=True,margins_name='Total').sort_values('Total')
    return


@app.cell
def _(Cuisine, Diets_Dataset__1):
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

    Diets_Dataset__2 = Diets_Dataset__1.copy()
    Diets_Dataset__2[Cuisine] = Diets_Dataset__1[Cuisine].apply(GroupsCuisine.get).apply(groups_names.get)
    return (Diets_Dataset__2,)


@app.cell
def _(mo):
    mo.md(r"## 4.3 Visión General de los Datos")
    return


@app.cell
def _(Diets_Dataset__2, src):
    # Calculo de las medidas de tendencia central, dispersión y asimetría 

    src.SummaryMeasures(Diets_Dataset__2)
    return


@app.cell
def _(Cuisine, Diet, Diets_Dataset__2, Recipe):
    Diets_Dataset__2.pivot_table(Recipe,Cuisine,Diet,'count')
    return


@app.cell
def _(Diets_Dataset__2, src):
    VisionGeneral_1 = src.Plot_DistributionMacronutrients(Diets_Dataset__2)
    # src.SaveFig(VisionGeneral_1,'EDA','VisionGeneral_1')

    VisionGeneral_1
    return


@app.cell
def _(Diets_Dataset__2, src):
    VisionGeneral_2 = src.Plot_DistributionMacronutrientsByCuisine(Diets_Dataset__2)
    # src.SaveFig(VisionGeneral_2,'EDA','VisionGeneral_2')

    VisionGeneral_2
    return


@app.cell
def _(Cuisine, Diets_Dataset__2):
    # Eliminar la cocian world

    Diets_Dataset = Diets_Dataset__2.query(f"{Cuisine} != 'world'")
    return (Diets_Dataset,)


@app.cell
def _(mo):
    mo.md(r"## 4.4 Estratificación de las Recetas por Dieta")
    return


@app.cell
def _(Diet, Diets, Diets_Dataset, src):
    # Medidas por dieta

    summary_diet_measures = []
    for __diet in Diets:
        summary_diet = src.SummaryMeasures(Diets_Dataset.query(f'{Diet} == @__diet'))
        summary_diet_measures.append((__diet,summary_diet))
    return (summary_diet_measures,)


@app.cell
def _(Diets, Macronutrients, pd, summary_diet_measures):
    # Obteniendo el resumen final

    summary_macronutrients = []
    for __macronutrient in Macronutrients:
        summary_macronutrient = pd.concat([summary[1][__macronutrient].rename(__diet) for __diet , summary in zip(Diets,summary_diet_measures)],axis=1)
        summary_macronutrients.append((__macronutrient,summary_macronutrient))

    summary_macronutrients
    return


@app.cell
def _(mo):
    mo.md(r"# 5. Análisis Bivariado")
    return


@app.cell
def _(Diets_Dataset, src):
    PlotCorrelation = src.Plot_CorrelationMacronutrients(Diets_Dataset)
    #src.SaveFig(PlotCorrelation,'Bivariado','Correlation')

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

    pd.DataFrame(dataset_biv)
    return


@app.cell
def _(mo):
    mo.md(r"# 6. Muestreo e Intervalos de Confianza")
    return


@app.cell
def _(mo):
    mo.md(r"## 6.1 Muestreo Simple Aleatorio")
    return


@app.cell
def _(Diets_Dataset, Macronutrients, RANDOM_STATE):
    random_sampling = Diets_Dataset.sample(50,random_state=RANDOM_STATE)

    random_sampling[Macronutrients[0]]
    return (random_sampling,)


@app.cell
def _(Macronutrients, random_sampling, src):
    src.Sample_FrequencyTable(random_sampling[Macronutrients[0]],7)
    return


@app.cell
def _(random_sampling, src):
    src.SummaryMeasures(random_sampling)
    return


@app.cell
def _(Macronutrients, random_sampling, src):
    PlotRandomSample = src.Plot_Sampling(random_sampling,Macronutrients[0])
    #src.SaveFig(PlotRandomSample,'Sampling','Random')

    PlotRandomSample
    return


@app.cell
def _(mo):
    mo.md(r"## 6.2 Muestreo Aleatorio Estratificado")
    return


@app.cell
def _(Diet, Diets_Dataset, Recipe, np):
    proportion_diets = (Diets_Dataset.groupby(Diet)[Recipe].count()/Diets_Dataset.shape[0])
    size_strata_diet = np.round(proportion_diets*50)
    return (size_strata_diet,)


@app.cell
def _(Diet, Diets_Dataset, Macronutrients, RANDOM_STATE, pd, size_strata_diet):
    stratified_sampling = []
    for strata_diet ,  size in  size_strata_diet.items():
        sampling = Diets_Dataset.query(f'{Diet} == @strata_diet').sample(int(size),random_state=RANDOM_STATE)
        stratified_sampling.append(sampling)

    stratified_sampling = pd.concat(stratified_sampling)

    stratified_sampling[Macronutrients[0]]

    stratified_sampling[Macronutrients[0]]
    return (stratified_sampling,)


@app.cell
def _(Macronutrients, src, stratified_sampling):
    src.Sample_FrequencyTable(stratified_sampling[Macronutrients[0]],7)
    return


@app.cell
def _(src, stratified_sampling):
    src.SummaryMeasures(stratified_sampling)
    return


@app.cell
def _(Macronutrients, src, stratified_sampling):
    PlotStratifiedSample = src.Plot_Sampling(stratified_sampling,Macronutrients[0])
    #src.SaveFig(PlotStratifiedSample,'Sampling','Stratified')

    PlotStratifiedSample
    return


@app.cell
def _(mo):
    mo.md(r"## 6.3 Intervalos de Confianza")
    return


@app.cell
def _():
    confidence_levels = [0.85,0.95,0.99]
    return (confidence_levels,)


@app.cell
def _(Macronutrients, confidence_levels, random_sampling, src):
    src.Sample_ConfidenceInterval(random_sampling[Macronutrients[0]],confidence_levels)
    return


@app.cell
def _(Macronutrients, confidence_levels, src, stratified_sampling):
    src.Sample_ConfidenceInterval(stratified_sampling[Macronutrients[0]],confidence_levels)
    return


@app.cell
def _(mo):
    mo.md(r"# 7. Pruebas de Hipótesis")
    return


@app.cell
def _(mo):
    mo.md(r"## 7.2 Dieta DASH")
    return


@app.cell
def _(Diets_Dataset, Macronutrients, RANDOM_STATE, Total):
    # Muestreo de las recetas

    test_dash_sample = Diets_Dataset.query("Diet_type == 'dash'").sample(250,random_state=RANDOM_STATE,ignore_index=True)[Macronutrients+[Total]]
    test_dash_sample[Macronutrients] *= test_dash_sample[Total].to_numpy()[:,None]
    return (test_dash_sample,)


@app.cell
def _(Macronutrients, Total, np, test_dash_sample):
    # Formar la ingesta diaria siguiendo la receta

    test_dash_daily = test_dash_sample.groupby(np.arange(250)//5).sum()
    test_dash_daily[Macronutrients] /= test_dash_daily[Total].to_numpy()[:,None]
    return (test_dash_daily,)


@app.cell
def _(src, test_dash_daily):
    # Resultados de la prueba

    src.TestDashDiet(test_dash_daily)
    return


@app.cell
def _(mo):
    mo.md(r"## 7.3 Dieta Keto")
    return


@app.cell
def _(Cuisine, Diets_Dataset):
    # Obtener las recetas por cocina

    test_keto_recipes = Diets_Dataset.query("Diet_type == 'keto'").groupby(Cuisine)
    return (test_keto_recipes,)


@app.cell
def _(src, test_keto_recipes):
    # Resultados de la prueba

    src.TestKetoDiet(test_keto_recipes)
    return


@app.cell
def _(mo):
    mo.md(r"## 7.4 Dieta Mediterráneo")
    return


@app.cell
def _(Diets_Dataset):
    # Obtener recetas por región

    test_mediterranean_local = Diets_Dataset.query("Diet_type == 'mediterranean' & Cuisine_type == 'mediterranean'")
    test_mediterranean_others = Diets_Dataset.query("Diet_type == 'mediterranean' & Cuisine_type != 'mediterranean'")
    return test_mediterranean_local, test_mediterranean_others


@app.cell
def _(src, test_mediterranean_local, test_mediterranean_others):
    # Resultados de la prueba

    src.TestMediterraneanDiet(test_mediterranean_local,test_mediterranean_others)
    return


@app.cell
def _(mo):
    mo.md(r"## 7.5 Dieta Paleo")
    return


@app.cell
def _(Cuisine, Diets_Dataset):
    # Obtener recetas por cocina

    test_paleo_recipes = Diets_Dataset.query("Diet_type == 'paleo'").groupby(Cuisine)
    return (test_paleo_recipes,)


@app.cell
def _(src, test_paleo_recipes):
    # Resultados de la prueba

    src.TestPaleoDiet_1(test_paleo_recipes)
    return


@app.cell
def _(src, test_paleo_recipes):
    # Resultados de la prueba post-hoc

    src.TestPaleoDiet_2(test_paleo_recipes)
    return


@app.cell
def _(mo):
    mo.md(r"## 7.6 Dieta Vegana")
    return


@app.cell
def _(Cuisine, Diets_Dataset):
    # Obtener recetas por cocina

    test_vegan_recipes = Diets_Dataset.query("Diet_type == 'vegan'").groupby(Cuisine)
    return (test_vegan_recipes,)


@app.cell
def _(src, test_vegan_recipes):
    src.TestVeganDiet(test_vegan_recipes)
    return


@app.cell
def _(mo):
    mo.md(r"## 7.7 Diferencias entre Dietas")
    return


@app.cell
def _(Diets_Dataset, src):
    # Resultados de la prueba

    src.TestDifferenceDiets(Diets_Dataset)
    return


@app.cell
def _(mo):
    mo.md(r"## 7.8 Interacción entre Dietas y Cocinas")
    return


@app.cell
def _(Diets_Dataset, Macronutrients, src):
    # Resultados de prueba

    test_result_interaction = []
    for macronutrient in Macronutrients:
        result_interaction = src.TestInteractionDietCuisine(Diets_Dataset,macronutrient)
        test_result_interaction.append((macronutrient,result_interaction))

    test_result_interaction
    return


@app.cell
def _(mo):
    mo.md(r"## 7.9 Regresión Lineal")
    return


@app.cell
def _(Diet, Diets, Diets_Dataset, src):
    # Resultados de la prueba

    test_result_regression = []
    for diet_test in Diets:
        result_regression = src.TestLinealDependency(Diets_Dataset.query(f'{Diet} == @diet_test'))
        test_result_regression.append([diet_test,result_regression])

    test_result_regression
    return


@app.cell
def _(Diet, Diets, Diets_Dataset, src):
    # Parámetros de regresión lineal

    test_result_fit = []
    for diet_fit in Diets:
        result_fit = src.FitLinealRegression(Diets_Dataset.query(f'{Diet} == @diet_fit'))
        test_result_fit.append((diet_fit,result_fit))

    test_result_fit
    return


@app.cell
def _(Diet, Diets, Diets_Dataset, plt, src):
    for diet_reg in Diets:
        case_str_reg = str.capitalize if diet_reg != 'dash' else str.upper
        PlotRegression = src.Plot_RegressionMacronutrients(Diets_Dataset.query(f'{Diet} == @diet_reg'),case_str_reg(diet_reg))
        # src.SaveFig(PlotRegression,'Bivariado','Regression'+diet_reg.capitalize())

    plt.show()
    return


@app.cell
def _(mo):
    mo.md(r"# Anexo B: Estratificación de las Recetas por Dieta")
    return


@app.cell
def _(mo):
    mo.md(r"## B.1 Dieta DASH")
    return


@app.cell
def _(Diet, Diets_Dataset, src):
    dash = 'dash'

    src.SummaryMeasures(Diets_Dataset.query(f'{Diet} == @dash'))
    return


@app.cell
def _(Diet, Diets_Dataset, src):
    PlotDash_1 = src.Plot_DistributionMacronutrients(Diets_Dataset.query(f'{Diet} == @dash'),'DASH')
    #src.SaveFig(PlotDash_1,'EDA','Dash_1')

    PlotDash_1
    return


@app.cell
def _(Diet, Diets_Dataset, src):
    PlotDash_2 = src.Plot_DistributionMacronutrientsByCuisine(Diets_Dataset.query(f'{Diet} == @dash'),'DASH')
    #src.SaveFig(PlotDash_2,'EDA','Dash_2')

    PlotDash_2
    return


@app.cell
def _(mo):
    mo.md(r"## B.2 Dieta Keto")
    return


@app.cell
def _(Diet, Diets_Dataset, src):
    keto = 'keto'

    src.SummaryMeasures(Diets_Dataset.query(f'{Diet} == @keto'))
    return


@app.cell
def _(Diet, Diets_Dataset, src):
    PlotKeto_1 = src.Plot_DistributionMacronutrients(Diets_Dataset.query(f'{Diet} == @keto'),'Keto')
    #src.SaveFig(PlotKeto_1,'EDA','Keto_1')

    PlotKeto_1
    return


@app.cell
def _(Diet, Diets_Dataset, src):
    PlotKeto_2 = src.Plot_DistributionMacronutrientsByCuisine(Diets_Dataset.query(f'{Diet} == @keto'),'Keto')
    #src.SaveFig(PlotKeto_2,'EDA','Keto_2')

    PlotKeto_2
    return


@app.cell
def _(mo):
    mo.md(r"## B.3 Dieta Mediterránea")
    return


@app.cell
def _(Diet, Diets_Dataset, src):
    mediterranean = 'mediterranean'

    src.SummaryMeasures(Diets_Dataset.query(f'{Diet} == @mediterranean'))
    return


@app.cell
def _(Diet, Diets_Dataset, src):
    PlotMediterranean_1 = src.Plot_DistributionMacronutrients(Diets_Dataset.query(f'{Diet} == @mediterranean'),'Mediterranean')
    #src.SaveFig(PlotMediterranean_1,'EDA','Mediterranean_1')

    PlotMediterranean_1
    return


@app.cell
def _(Diet, Diets_Dataset, src):
    PlotMediterranean_2 = src.Plot_DistributionMacronutrientsByCuisine(Diets_Dataset.query(f'{Diet} == @mediterranean'),'Mediterranean')
    #src.SaveFig(PlotMediterranean_2,'EDA','Mediterranean_2')

    PlotMediterranean_2
    return


@app.cell
def _(mo):
    mo.md(r"## B.4 Dieta Paleo")
    return


@app.cell
def _(Diet, Diets_Dataset, src):
    paleo = 'paleo'

    src.SummaryMeasures(Diets_Dataset.query(f'{Diet} == @paleo'))
    return


@app.cell
def _(Diet, Diets_Dataset, src):
    PlotPaleo_1 = src.Plot_DistributionMacronutrients(Diets_Dataset.query(f'{Diet} == @paleo'),'Paleo')
    #src.SaveFig(PlotPaleo_1,'EDA','Paleo_1')

    PlotPaleo_1
    return


@app.cell
def _(Diet, Diets_Dataset, src):
    PlotPaleo_2 = src.Plot_DistributionMacronutrientsByCuisine(Diets_Dataset.query(f'{Diet} == @paleo'),'Paleo')
    #src.SaveFig(PlotPaleo_2,'EDA','Paleo_2')

    PlotPaleo_2
    return


@app.cell
def _(mo):
    mo.md(r"## B.5 Dieta Vegana")
    return


@app.cell
def _(Diet, Diets_Dataset, src):
    vegan = 'vegan'

    src.SummaryMeasures(Diets_Dataset.query(f'{Diet} == @vegan'))
    return


@app.cell
def _(Diet, Diets_Dataset, src):
    PlotVegan_1 = src.Plot_DistributionMacronutrients(Diets_Dataset.query(f'{Diet} == @vegan'),'Vegan')
    #src.SaveFig(PlotVegan_1,'EDA','Vegan_1')

    PlotVegan_1
    return


@app.cell
def _(Diet, Diets_Dataset, src):
    PlotVegan_2 = src.Plot_DistributionMacronutrientsByCuisine(Diets_Dataset.query(f'{Diet} == @vegan'),'Vegan')
    #src.SaveFig(PlotVegan_2,'EDA','Vegan_2')

    PlotVegan_2
    return


if __name__ == "__main__":
    app.run()
