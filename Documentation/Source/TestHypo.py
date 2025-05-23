from itertools import combinations
from scipy import stats
from scikit_posthocs import posthoc_dunn
from pingouin import anova

import pandas as pd
import numpy as np

from .Base import *

def TestDashDiet(Dataset:pd.DataFrame):
    """
    Función para aplicar la prueba de hipótesis 
    sobre la dieta DASH

    Parameters
    ----------
        Dataset : pd.DataFrame
    """
    test_result = []
    for macronutrient in Macronutrients:
        result = stats.ttest_1samp(Dataset[macronutrient],1/3,alternative='two-sided')
        test_result.append([macronutrient,result.pvalue,result.statistic])

    return pd.DataFrame(test_result,columns=['Macronutrient','P_value','Statistic_t'])

def TestKetoDiet(Dataset:pd.DataFrame):
    """
    Función para aplicar la prueba de hipótesis 
    sobre la dieta Keto

    Parameters
    ----------
        Dataset : pd.DataFrame
    """
    test_result = []
    for cuisine in Dataset.groups.keys():
        recipes_by_cuisine = Dataset.get_group(cuisine)
        homoscedasticity = stats.levene(recipes_by_cuisine['Carbs'],recipes_by_cuisine['Fat'],center='mean').pvalue >= 0.05
        result = stats.ttest_ind(recipes_by_cuisine['Carbs'],recipes_by_cuisine['Fat'],equal_var=homoscedasticity,alternative='less')
        
        test_result.append([cuisine,result.pvalue,result.statistic])
    
    return pd.DataFrame(test_result,columns=['Cuisine','P_value','Statistic_t'])

def TestMediterraneanDiet(Dataset_Local:pd.DataFrame,Dataset_Other:pd.DataFrame):
    """
    Función para aplicar la prueba de hipótesis 
    sobre la dieta Mediterránea

    Parameters
    ----------
        Dataset_Local : pd.DataFrame
        Dataset_Other : pd.DataFrame
    """
    test_result = []
    for macronutrient in Macronutrients:
        result = stats.ks_2samp(Dataset_Local[macronutrient],Dataset_Other[macronutrient])
        test_result.append([macronutrient,result.pvalue,result.statistic])

    return pd.DataFrame(test_result,columns=['Macronutrient','P_value','Statistic_d'])

def TestPaleoDiet_1(Dataset:pd.DataFrame):
    """
    Función para aplicar la primera prueba de hipótesis 
    sobre la dieta Paleo

    Parameters
    ----------
        Dataset : pd.DataFrame
    """
    result_test = stats.kruskal(*[Dataset.get_group(cuisine)['Protein'] for cuisine in Dataset.groups.keys()])

    return pd.DataFrame([[result_test.pvalue,result_test.statistic]],columns=['P_value','Statistic_h'])

def TestPaleoDiet_2(Dataset:pd.DataFrame):
    """
    Función para aplicar la segunda prueba de hipótesis 
    sobre la dieta Paleo

    Parameters
    ----------
        Dataset : pd.DataFrame
    """
    results = posthoc_dunn([Dataset.get_group(cuisine)['Protein'] for cuisine in Dataset.groups.keys()],p_adjust='holm')

    labels = dict(enumerate(Dataset.groups.keys(),1))
    results.rename(columns=labels,index=labels,inplace=True)
    return results

def TestVeganDiet(Dataset:pd.DataFrame):
    """
    Función para aplicar la prueba de hipótesis 
    sobre la dieta Keto

    Parameters
    ----------
        Dataset : pd.DataFrame
    """
    test_result = []
    for cuisine in Dataset.groups.keys():
        recipes_by_cuisine = Dataset.get_group(cuisine)
        homoscedasticity = stats.levene(recipes_by_cuisine['Protein'],recipes_by_cuisine['Carbs'],center='mean').pvalue >= 0.05
        result = stats.ttest_ind(recipes_by_cuisine['Protein'],recipes_by_cuisine['Carbs'],equal_var=homoscedasticity,alternative='less')

        test_result.append([cuisine,result.pvalue,result.statistic])
    
    return pd.DataFrame(test_result,columns=['Cuisine','P_value','Statistic_t'])

def TestDifferenceDiets(Dataset:pd.DataFrame):
    """
    Función para aplicar la prueba de hipótesis 
    de las diferencias entre dietas

    Parameters
    ----------
        Dataset : pd.DataFrame
    """
    statistic_results = {macronutrient : pd.DataFrame(np.zeros((5,5),dtype=float),columns=Diets,index=Diets) for macronutrient in Macronutrients}
    pvalue_results = {macronutrient : pd.DataFrame(np.zeros((5,5),dtype=float),columns=Diets,index=Diets) for macronutrient in Macronutrients}
    for diet_1 , diet_2 in combinations(Diets,2):
        recipes_diet_1 = Dataset.query("Diet_type == @diet_1")
        recipes_diet_2 = Dataset.query("Diet_type == @diet_2")
        for macronutrient in Macronutrients:
            result_test = stats.ks_2samp(recipes_diet_1[macronutrient],recipes_diet_2[macronutrient])

            statistic_results[macronutrient].loc[diet_1,diet_2] = result_test.statistic
            statistic_results[macronutrient].loc[diet_2,diet_1] = result_test.statistic

            pvalue_results[macronutrient].loc[diet_1,diet_2] = result_test.pvalue
            pvalue_results[macronutrient].loc[diet_2,diet_1] = result_test.pvalue

            statistic_results[macronutrient].loc[diet_1,diet_1] = 0
            pvalue_results[macronutrient].loc[diet_1,diet_1] = 1

    return sum(statistic_results[macronutrient] for macronutrient in Macronutrients)/3 , sum(pvalue_results[macronutrient] < 0.05 for macronutrient in Macronutrients)

def TestInteractionDietCuisine(Dataset:pd.DataFrame,Macronutrient:str):
    """
    Función para aplicar la prueba de hipótesis 
    de la interacción entre dietas y cocina

    Parameters
    ----------
        Dataset : pd.DataFrame
        Macronutrient : str
    """
    interaction_diet_cuisine = Dataset[[Macronutrient,Diet,Cuisine]].copy()

    interaction_diet_cuisine[f'{Macronutrient}_Rank'] = stats.rankdata(interaction_diet_cuisine[Macronutrient])
    linear_model = anova(data=interaction_diet_cuisine, dv=f'{Macronutrient}_Rank', between=[Diet,Cuisine], detailed=True)
    
    return linear_model

def TestLinealDependency(Dataset:pd.DataFrame):
    """
    Función para aplicar la prueba de hipótesis 
    de la dependencia lineal entre macronutrientes 
    de una dieta

    Parameters
    ----------
        Dataset : pd.DataFrame
    """
    test_result = []
    for macronutrient_1 , macronutrient_2 in combinations(Macronutrients,2):
        correlation_value = Dataset[[macronutrient_1,macronutrient_2]].corr().iloc[0,1]
        sided = 'less' if correlation_value < 0 else 'greater'
        result_test = stats.pearsonr(Dataset[macronutrient_1],Dataset[macronutrient_2],alternative=sided)
        test_result.append([f'{macronutrient_1} {macronutrient_2}',result_test.pvalue,result_test.statistic])
    return pd.DataFrame(test_result,columns=['Macronutrients','P_value','Statistic'])

def FitLinealRegression(Dataset:pd.DataFrame):
    """
    Función para determinar la curva de regresión 
    lineal que mejor se ajusta a los datos

    Parameters
    ----------
        Dataset : pd.DataFrame
    """
    result_fit = []
    for macronutrient_1 , macronutrient_2 in combinations(Macronutrients,2):
        fit = stats.linregress(Dataset[macronutrient_1],Dataset[macronutrient_2])
        result_fit.append([f'{macronutrient_1} {macronutrient_2}',fit.slope,fit.intercept])
    
    return pd.DataFrame(result_fit,columns=['Macronutrients','Slope','Intercept'])