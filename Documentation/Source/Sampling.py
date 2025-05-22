import pandas as pd
import numpy as np
import seaborn as sns
from scipy import stats

from .BasePlot import *

def Sample_FrequencyTable(SampleData:pd.DataFrame,Bins:int) -> pd.DataFrame:
    """
    Función para generar la tabla de frecuencias 
    en base a un muestreo junto con sus z-score

    Parameters
    ----------
        SampleData : pd.DataFrame
        Bins : int
    """
    frequency_absolute , bins_classes = np.histogram(SampleData,bins=Bins)

    table_frequency = []
    table_frequency.append(frequency_absolute)
    table_frequency.append(frequency_absolute/50)
    table_frequency.append(np.cumulative_sum(frequency_absolute)/50)

    class_marks = (bins_classes[:-1]+bins_classes[1:])/2
    
    sampling_mean = SampleData.mean()
    sampling_std = SampleData.std()
    table_frequency.append((class_marks-sampling_mean)/sampling_std)

    table_frequency = pd.DataFrame(table_frequency,index=['Frequency_absolute','Frequency_relative','Frequency_cumulative','z-score'],columns=class_marks).T
    table_frequency.rename_axis(index='Class_mark',columns='Frequencies',inplace=True)

    return table_frequency

def Plot_Sampling(SampleData:pd.DataFrame,Macronutrient:str):
    fig , axes = SimplePlot()
    sns.boxplot(SampleData,x=Macronutrient,ax=axes,color=Color_Palette[InverseMacronutrient[Macronutrient]])

    SetLabelsPlot(axes,f'Distribución Muestral de {MapTranslate[Macronutrient]}',MapTranslate[Macronutrient])

    return fig

def Sample_ConfidenceInterval(SampleData:pd.DataFrame,ConfidenceLevels:list[float]):
    """
        Función para obtener el intervalo de confianza 
        para la media poblacional a partir de una confianza 
        dada y un muestreo.

        Parameters
        ----------
            SampleData : pd.DataFrame
            ConfidenceLevels : list[float]
    """
    size_sample = SampleData.size
    mean_sample = np.mean(SampleData)
    std_sample = np.std(SampleData,ddof=1)

    confidence_intervals = []
    for confidence in ConfidenceLevels:
        interval_confidence = stats.norm.interval(confidence,mean_sample,std_sample/np.sqrt(size_sample))
        confidence_intervals.append([confidence,*interval_confidence])
    
    return pd.DataFrame(confidence_intervals,columns=['Confidence_level','Lower_interval','Upper_interval'])