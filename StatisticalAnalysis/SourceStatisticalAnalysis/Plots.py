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
    
    components_values = PCA(random_state=RANDOM_STATE).fit_transform(Dataset[Macronutrients])
    sns.scatterplot(
        x=components_values[:,0],
        y=components_values[:,1],
        ax=axes[1],
        alpha=0.25,
        linewidth=0,
        color=ColorBase,
    )
    SetLabels(axes[1],XLabel='PC1',YLabel='PC2')

    title = 'Correlations and PCA of\nMacronutrients' + (f' in {Diet} Diet' if Diet else '')
    fig.suptitle(title,fontsize=20)

    return fig

def CreateMosaicPlot(
    ) -> tuple[Figure, dict[str,Axes], Iterator[tuple[str,str,str]]]:
    """
    Function for creating the fig
    for plots
    """
    display = "PPCC;.FF."

    fig , axes = plt.subplot_mosaic(
        display,
        figsize=(8,6),
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