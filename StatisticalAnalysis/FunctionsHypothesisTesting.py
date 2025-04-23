import pandas as pd
from scipy import stats
import statsmodels.stats.weightstats as sm

Macronutrients = ['Carbs(g)','Protein(g)','Fat(g)']


def DashBalanceMacronutrients(DailyMacronutrients:pd.DataFrame,Significance:float=0.05) -> list[float]:
    """
        Function to test whether following the 
        DASH diet provides a balance in the 
        daily macronutrient intake.

        -- DailyMacronutrients : pd.DataFrame :: Sampling of daily macronutrient proportions

        -- Significance : float :: Significance of hypothesis testing

        Returns the p-values obtained from the Z test.
    """
    pvalues_z_test = []
    for macronutrient in Macronutrients:
        data_daily_macronutrient = DailyMacronutrients[macronutrient]

        fit_args_cdf = stats.norm.fit(data_daily_macronutrient)
        normality_result = stats.kstest(data_daily_macronutrient,'norm',method='two-sided',args=fit_args_cdf).pvalue
        if Significance < normality_result:
            print(f'{macronutrient[:-3]} does follow a normal distribution')
        else:
            print(f'{macronutrient[:-3]} does not follow a normal distribution')
        
        z_test_result = sm.ztest(data_daily_macronutrient,value=1/3,alternative='two-sided')[1]
        if Significance < z_test_result:
            print(f'{macronutrient[:-3]} is balanced')
        else:
            print(f'{macronutrient[:-3]} is not balanced')
        print()

        pvalues_z_test.append(z_test_result)

    return pvalues_z_test


def KetoHomocedasticity(DataMacronutrients:list[pd.Series],Significance:float=0.05) -> float:
    """
        Function to test if the 
        recipes have the same composition 
        in the Keto diet.

        -- DataMacronutrients : list[pd.Series] :: Macronutrient values

        -- Significance : float :: Significance of hypothesis testing

    """
    homocedasticity_result = stats.levene(*DataMacronutrients).pvalue

    if Significance < homocedasticity_result:
        print('There is a same composition')
    else:
        print('There is not same composition')

    return homocedasticity_result