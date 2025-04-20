import pandas as pd

Macronutrients = ['Carbs(g)','Protein(g)','Fat(g)']
EncodedMacronutrients = {macronutrient[0]:macronutrient for macronutrient in Macronutrients}

def DeleteOutliersDiet(Diets_Dataset:pd.DataFrame,Diet:str,RulesMacronutrients:list[tuple[str,str]]):
    """
        Function for deleting outliers
    """
    def GetOutlierRule(Rule:str):
        macronutrient = EncodedMacronutrients[Rule[0]]
        type_rule = Rule[1]
        return f"not (`{macronutrient}` {type_rule} {quantiles_macronutrients.loc[type_rule,macronutrient]})"

    quantiles_macronutrients = Diets_Dataset.query("Diet_type == @Diet")[Macronutrients].quantile([0.25,0.75])
    quantiles_macronutrients.loc['interquartile_range'] = quantiles_macronutrients.loc[0.75] - quantiles_macronutrients.loc[0.25]
    quantiles_macronutrients.loc['<'] = quantiles_macronutrients.loc[0.25]-1.5*quantiles_macronutrients.loc['interquartile_range']
    quantiles_macronutrients.loc['>'] = quantiles_macronutrients.loc[0.75]+1.5*quantiles_macronutrients.loc['interquartile_range']

    outliers_rule = ' & '.join([f"Diet_type == '{Diet}'"]+list(map(GetOutlierRule,RulesMacronutrients)))
    return Diets_Dataset.query(outliers_rule)