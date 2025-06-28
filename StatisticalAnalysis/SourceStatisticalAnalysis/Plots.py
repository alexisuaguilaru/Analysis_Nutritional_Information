import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA

from .Base import *

import pandas as pd
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from typing import Iterator
import numpy as np
from scipy import stats 


def PlotMacronutrients(
        Dataset:pd.DataFrame,
        Diet:str=None,
    ) -> Figure:
    """
    Function for plotting distribution 
    of macronutrients
    """
    fig , axes , config_plot = CreateMosaicPlot()
    for macronutrient , mosaic_position , color in config_plot:
        axes[mosaic_position].grid(True,axis='x',color='gray',lw=1.5,ls=':')
        
        sns.violinplot(
            Dataset,
            x=macronutrient,
            ax=axes[mosaic_position],
            color=color,
            bw_adjust=2,
            fill=False,
            linewidth=2,
            inner_kws={'box_width':15},
        )

        SetLabels(axes[mosaic_position],XLabel=macronutrient)

    title = 'Distribution of Macronutrients' + (f'\nin {Diet} Diet' if Diet else '')
    fig.suptitle(title,fontsize=20)

    fig.savefig(f'./Resources/{Diet}Diet.png')
    return fig

def PlotRegressions(
        Dataset:pd.DataFrame,
        Diet:str=None,
    ) -> Figure:
    """
    Function for plotting regressions 
    curves between macronutrients
    """
    fig , axes , config_plot = CreateMosaicPlot()
    for macronutrient , mosaic_position , _ in config_plot:
        macronutrient_1 , macronutrient_2 = SetMacronutrients.difference(set([macronutrient]))

        sns.regplot(
            Dataset,
            x=macronutrient_1,
            y=macronutrient_2,
            ax=axes[mosaic_position],
            color=ColorBase,
            scatter_kws={'alpha':0.1, 'linewidths':0}
        )

        SetLabels(axes[mosaic_position],XLabel=macronutrient_1,YLabel=macronutrient_2)
    
    title = 'Regression Curves of\nMacronutrients' + (f' in {Diet} Diet' if Diet else '')
    fig.suptitle(title,fontsize=20)

    return fig

def PlotCorrelationsPCA(
        Dataset:pd.DataFrame,
        Diet:str=None,
        Macronutrient:str=None,
    ) -> Figure:
    """
    Function for plotting correlation 
    values of macronutrients and PC1 
    vs. PC2
    """
    fig , axes = plt.subplots(
        ncols=2,
        figsize=(10,6),
        layout='tight',
        subplot_kw={'frame_on':False},
        )

    correlation_matrix = Dataset[Macronutrients].corr()
    sns.heatmap(
        correlation_matrix,
        vmin=-1,vmax=1,
        ax=axes[0],
        cbar=False,
        annot=True,
        annot_kws={'size':12},
        cmap=ColorMap,
    )
    SetLabels(axes[0])
    
    pca_model = PCA(random_state=RANDOM_STATE)
    components_values = pca_model.fit_transform(Dataset[Macronutrients])
    sns.scatterplot(
        x=components_values[:,0],
        y=components_values[:,1],
        ax=axes[1],
        alpha=0.25,
        linewidth=0,
        color=ColorBase,
        size=Dataset[Macronutrient],
    )
    SetLabels(axes[1],XLabel='PC1',YLabel='PC2')

    title = 'Correlations and PCA of\nMacronutrients' + (f' in {Diet} Diet' if Diet else '')
    fig.suptitle(title,fontsize=20)

    return fig

def PlotBetaDistributions(
        Dataset:pd.DataFrame,
        Diet:str=None,
    ) -> Figure:
    fig , axes , config_plot = CreateMosaicPlot((9,8))
    for macronutrient , mosaic_position , color in config_plot:
        axes[mosaic_position].grid(True,axis='both',color='gray',lw=0.5,ls=':')

        fit_beta_arguments = stats.beta.fit(Dataset[macronutrient],floc=0,fscale=1)
        (theoretical_quantiles , observed_quantiles) , _ = stats.probplot(Dataset[macronutrient],dist=stats.beta,sparams=fit_beta_arguments)

        axes[mosaic_position].scatter(theoretical_quantiles,observed_quantiles,s=5,c=color)
        axes[mosaic_position].plot(theoretical_quantiles,theoretical_quantiles,color='black',alpha=0.5,linestyle='--',lw=3)
        axes[mosaic_position].set_xlim((theoretical_quantiles[0]-5e-2,theoretical_quantiles[-1]+5e-2))
        axes[mosaic_position].set_ylim((theoretical_quantiles[0]-5e-2,theoretical_quantiles[-1]+5e-2))
        
        title_axes = f'{macronutrient.capitalize()}\n' + rf'$\alpha =$ {fit_beta_arguments[0]:.2f} $\beta = ${fit_beta_arguments[1]:.2f}'
        SetLabels(axes[mosaic_position],title_axes,'Theorical Quantiles','Observed Quantiles')
    
    title = 'Q-Q Plots of Macronutrients' + (f'\nin {Diet} Diet' if Diet else '')
    fig.suptitle(title,fontsize=20)
    
    fig.savefig(f'./Resources/{Diet}Diet_Beta.png')
    return fig

def CreateMosaicPlot(
        FigSize:tuple[float,float]=(8,6),
    ) -> tuple[Figure, dict[str,Axes], Iterator[tuple[str,str,str]]]:
    """
    Function for creating the fig
    for plots

    Parameters
    ----------
    FigSize : tuple[float,float]
        Value for Parameter figsize of plt.subplot_mosaic
    """
    display = "PPCC;.FF."

    fig , axes = plt.subplot_mosaic(
        display,
        figsize=FigSize,
        layout='tight',
        subplot_kw={'frame_on':False,'xlim':(0-5e-2,1+5e-2),'ylim':(0-5e-2,1+5e-2)}
    )
    config_plot = zip(Macronutrients,['C','P','F'],ColorPalette)

    return fig , axes , config_plot

def SetLabels(
        Axes:Axes,
        Title:str=None,
        XLabel:str=None,
        YLabel:str=None,
    ) -> None:
    """
    Function for setting labels and title 
    of a plot
    """
    if Title: Axes.set_title(Title,size=20)
    if XLabel: Axes.set_xlabel(XLabel,size=15)
    if YLabel: Axes.set_ylabel(YLabel,size=15)
    
    Axes.tick_params(axis='both',labelsize=13)