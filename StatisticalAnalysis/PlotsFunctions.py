import pandas as pd
import numpy as np
from scipy import stats 

import matplotlib.pyplot as plt
import seaborn as sns

Macronutrients = ['Carbs(g)','Protein(g)','Fat(g)']
Diets = ['dash', 'keto', 'mediterranean', 'paleo', 'vegan']

Color_Palette = ['green','red','gold']
Color_Map = 'seismic'

def PlotMacronutientsByDiet(Diets_Dataset:pd.DataFrame,Diet:str):
    """
        Function for plotting of macronutrients by diet on Histogram
    """
    fig , axes , ConfigPlot = __CreateMosaicPlot()
    
    diet_type_dataset = Diets_Dataset.query("Diet_type == @Diet")
    for macronutrient , display , color in ConfigPlot:
        sns.histplot(data=diet_type_dataset,x=macronutrient,ax=axes[display],stat='proportion',bins=50,color=color)
        axes[display].set_title(macronutrient[:-3])
        axes[display].set_xlabel('Grams')

    fig.suptitle(f'Diet: {Diet}',size=25)

def PlotMacronutrients(Diets_Dataset:pd.DataFrame):
    """
        Function for plotting macronutrients by diet on Boxplot
    """
    fig , axes , ConfigPlot = __CreateMosaicPlot()

    for macronutrient , display , color in ConfigPlot:
        sns.boxplot(data=Diets_Dataset,x=macronutrient,y='Diet_type',ax=axes[display],color=color)
        axes[display].set_title(macronutrient[:-3])
        axes[display].set_xlabel('Grams')
    
    fig.suptitle('Distribution of Macronutrients by Diet',size=25)

def PlotCorrelogramsMacronutrients(Diets_Dataset:pd.DataFrame,Diet:str):
    """
        Function for plotting correlation matrix by macronutrients
    """
    fig , axes = plt.subplots(figsize=(6,5))

    sns.heatmap(Diets_Dataset.query("Diet_type == @Diet")[Macronutrients].corr(),annot=True,vmin=-1,vmax=1,ax=axes,cmap=Color_Map)
    axes.set_title(f"Diet: {Diet}")

def PlotMacronutrients2D(Diets_Dataset:pd.DataFrame,Diet:str):
    """
        Function for plotting Macronutrients on a plane 
    """
    fig , axes = plt.subplots(figsize=(7,5.5),layout='tight')
    
    data_macronutrients = Diets_Dataset.query("Diet_type == @Diet")[Macronutrients].to_numpy().T
    matrix_transformation = np.linalg.inv(np.array([[-1,-np.sqrt(3)/3,1],[1,-np.sqrt(3)/3,0],[0,2*np.sqrt(3)/3,0]]))
    data_transformed = (matrix_transformation@data_macronutrients).T

    sns.scatterplot(x=data_transformed[:,0],y=data_transformed[:,1],ax=axes,alpha=0.5)

    delta = 0.01
    axes.set_xlim(0-delta,1+delta)
    axes.set_ylim(0-delta,np.sqrt(3)/2+delta)

    fig.suptitle(f'Diet: {Diet}',size=25)

def PlotQQByDiet(Diets_Dataset:pd.DataFrame,Diet:str):
    """
        Function for plotting q-q plots by macronutrient
    """
    dataset_diet = Diets_Dataset.query("Diet_type == @Diet")[Macronutrients]

    fig , axes , ConfigPlot = __CreateMosaicPlot()
    for macronutrient , display , color in ConfigPlot:
        filtered_dataset = dataset_diet[macronutrient]
        filtered_dataset = filtered_dataset[(filtered_dataset < 1) & (filtered_dataset > 0)]

        fitted_dist_args = stats.beta.fit(filtered_dataset,floc=0,fscale=1)
        (theoretical_quantiles , sample_quantiles) , _ = stats.probplot(filtered_dataset,dist=stats.beta,sparams=fitted_dist_args)
        
        axes[display].scatter(theoretical_quantiles,sample_quantiles,s=5,c=color)
        axes[display].plot(theoretical_quantiles,theoretical_quantiles,color='black',alpha=0.5,linestyle='--',lw=3)
        
        axes[display].set_title(rf'{macronutrient[:-3]} fitted to $\alpha$={fitted_dist_args[0]:.4f} and $\beta$={fitted_dist_args[1]:.4f}')
        axes[display].set_xlabel('Theoretical Quantiles')
        axes[display].set_ylabel('Sample Quantiles')
    
    fig.suptitle(f'Q-Q Plots by Macronutrient in {Diet}',size=23)

def __CreateMosaicPlot():
    """
        Function for creating the fig
        for plots
    """
    Display = "PPCC\n.FF."

    fig , axes = plt.subplot_mosaic(Display,figsize=(12,8),layout='tight')
    ConfigPlot = zip(Macronutrients,['C','P','F'],Color_Palette)

    return fig , axes , ConfigPlot