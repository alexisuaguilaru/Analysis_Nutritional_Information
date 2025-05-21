import pandas as pd
import seaborn as sns

from .Base import Macronutrients
from .BasePlot import *

def SummaryMeasures(Dataset:pd.DataFrame) -> pd.DataFrame:
    """
    Función para calcular la media, Q1, Q2, Q3, desviación 
    estándar, mínimo, máximo y asimetría de Fisher de un 
    conjunto de datos sobre ciertos atributos

    Parameters
    ----------
        Dataset : pd.DataFrame

    Returns
    -------
        summary : pd.DataFrame
    """
    measures = ['mean','25%','50%','75%','std','min','max']
    
    summary_measures = Dataset[Macronutrients].describe().loc[measures]
    summary_measures.loc['skewness'] = Dataset[Macronutrients].skew()

    return summary_measures

def Plot_DistributionMacronutrients(Dataset:pd.DataFrame,Diet:str=None):
    """
    Función para gráficar los gráficos de tipo cajas y bigotes 
    por cada macronutriente.

    Parameters
    ----------
        Dataset : pd.DataFrame
        Diet : str
    """
    fig , axes , ConfigPlot = CreateMosaicPlot()
    for macronutrient , display , color in ConfigPlot:
        sns.boxplot(data=Dataset,x=macronutrient,ax=axes[display],color=color)
        SetLabelsPlot(axes[display],MapTranslate[macronutrient],'Porcentaje de Gramos')

    SetTitleFig(fig,'Distribución de Macronutrientes' + (f'\n en {Diet}' if Diet else ''))

    return fig

def Plot_DistributionMacronutientsByCuisine(Dataset:pd.DataFrame,Diet:str=None):
    """
    Función para gráficar la distribución de los 
    macronutrientes por estilo de cocina

    Parameters
    ----------
        Dataset : pd.DataFrame
        Diet : str
    """
    fig , axes , ConfigPlot = CreateMosaicPlot()
    for macronutrient , display , color in ConfigPlot:
        sns.boxplot(data=Dataset,x=macronutrient,y=Cuisine,ax=axes[display],color=color)
        SetLabelsPlot(axes[display],MapTranslate[macronutrient],'Porcentaje de Gramos','Tipo de Cocina')

    SetTitleFig(fig,'Distribución de Macronutrientes\nPor Cocina' + (f' en {Diet}' if Diet else ''))

    return fig