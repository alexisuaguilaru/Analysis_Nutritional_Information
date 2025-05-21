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

def Plot_DistributionMacronutrientsByCuisine(Dataset:pd.DataFrame,Diet:str=None):
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

def Plot_RegressionMacronutrients(Dataset:pd.DataFrame,Diet:str=None):
    """
    Función para gráficar las líneas de regresión
    entre los macronutrientes

    Parameters
    ----------
        Dataset : pd.DataFrame
        Diet : str
    """
    fig , axes , ConfigPlot = CreateMosaicPlot()
    for macronutrient , display , _ in ConfigPlot:
        macronutrient_1 , macronutrient_2 = [macro for macro in Macronutrients if macro != macronutrient]
        sns.regplot(Dataset,x=macronutrient_1,y=macronutrient_2,ax=axes[display],
                    scatter_kws={'alpha':0.1,'linewidths':0,'color':'#337BF5'},
                    line_kws={'color':'black'})

        x_label = MapTranslate[macronutrient_1]
        y_label = MapTranslate[macronutrient_2]
        rho = Dataset[[macronutrient_1,macronutrient_2]].corr().iloc[0,1]
        SetLabelsPlot(axes[display],f'{x_label} contra {y_label}\n'+rf'$\rho$={rho:.4f}',x_label,y_label)

    SetTitleFig(fig,f'Correlación entre Macronutrientes' + (f'\nen {Diet}' if Diet else ''))

    return fig

def Plot_CorrelationMacronutrients(Dataset:pd.DataFrame):
    """
    Función para gráficar las correlaciones
    entre los macronutrientes

    Parameters
    ----------
        Dataset : pd.DataFrame
    """
    Display = "0011\n2233\n.44."
    fig , axes = plt.subplot_mosaic(Display,figsize=(12,20),layout='tight')
    
    for index_diet , diet in enumerate(Diets):
        corr_matrix = Dataset.query("Diet_type == @diet")[Macronutrients].corr()
        sns.heatmap(corr_matrix,vmin=-1,vmax=1,annot=True,cmap=Color_Map,ax=axes[str(index_diet)],annot_kws={'size':15},linecolor='white',linewidths=4,cbar=False)
        
        case_str = str.capitalize if diet != 'dash' else str.upper
        SetLabelsPlot(axes[str(index_diet)],case_str(diet),'Macronutrientes','Macronutrientes')
    
    SetTitleFig(fig,'Correlograma de los Macronutrientes\nEn las Diferentes Dietas')

    return fig