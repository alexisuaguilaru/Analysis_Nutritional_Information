from itertools import combinations
from copy import deepcopy
import pandas as pd
import numpy as np
from scipy import stats

from .Base import *

def TestDifferenceDiets(
        Dataset:pd.DataFrame
    ) -> tuple[pd.DataFrame,pd.DataFrame]:
    """
    Function for testing hypothesis about 
    differences between nutritional contributions 
    of diets

    Parameters
    ----------
    Dataset : pd.DataFrame
        Dataset which contains macronutrients and diet of recipes 

    Returns
    -------
    StatisticResults : pd.DataFrame
        Dataframe with the mean of test statistics
    PValueResults : pd.DataFrame
        Dataframe with count of significant differences
    """
    DataFrameMacronutrients = {macronutrient : pd.DataFrame(np.zeros((5,5),dtype=float),columns=Diets,index=Diets) for macronutrient in Macronutrients}
    StatisticResults = deepcopy(DataFrameMacronutrients)
    PValueResults = deepcopy(DataFrameMacronutrients)

    for diet_1 , diet_2 in combinations(Diets,2):
        recipes_diet_1 = Dataset.query(f"{Diet} == '{diet_1}'")
        recipes_diet_2 = Dataset.query(f"{Diet} == '{diet_2}'")

        for macronutrient in Macronutrients:
            result_test = stats.ks_2samp(recipes_diet_1[macronutrient],recipes_diet_2[macronutrient])

            StatisticResults[macronutrient].loc[diet_1,diet_2] = result_test.statistic
            StatisticResults[macronutrient].loc[diet_2,diet_1] = result_test.statistic

            PValueResults[macronutrient].loc[diet_1,diet_2] = result_test.pvalue
            PValueResults[macronutrient].loc[diet_2,diet_1] = result_test.pvalue

            StatisticResults[macronutrient].loc[diet_1,diet_1] = 0
            PValueResults[macronutrient].loc[diet_1,diet_1] = 1
            StatisticResults[macronutrient].loc[diet_2,diet_2] = 0
            PValueResults[macronutrient].loc[diet_2,diet_2] = 1

    return sum(StatisticResults[macronutrient] for macronutrient in Macronutrients)/3 , sum(PValueResults[macronutrient] < 0.05 for macronutrient in Macronutrients)