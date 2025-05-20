import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from .Base import *

def CreateMosaicPlot():
    Display = "PPCC\n.FF."

    fig , axes = plt.subplot_mosaic(Display,figsize=(12,8),layout='constrained',subplot_kw={'xlim':(0-1e-2,1+1e-2)})
    ConfigPlot = zip(Macronutrients,['C','P','F'],Color_Palette)

    return fig , axes , ConfigPlot

def OrderDiets(Dataset:pd.DataFrame,Macronutrient:str) -> np.ndarray:
    return Dataset[Macronutrient].quantile(0.25).sort_values().index

def SetLabelsPlot(ax,Title:str,XLabel:str=None,YLabel:str=None) -> None:
    if Title : ax.set_title(Title,size=18)
    if XLabel : ax.set_xlabel(XLabel,size=14)
    if YLabel : ax.set_ylabel(YLabel,size=14)
    ax.tick_params(labelsize=12)

def SetTitleFig(fig,Title:str) -> None:
    fig.suptitle(Title,size=30)