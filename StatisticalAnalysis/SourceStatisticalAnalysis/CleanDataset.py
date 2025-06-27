from scipy.special import gamma
from scipy.optimize import minimize
from scipy.stats import dirichlet
import numpy as np

from .Base import *

import pandas as pd

def DataCleaningFunction(
    Dataset:pd.DataFrame,
    Threshold:int=10,
) -> pd.DataFrame:
    """
    Function for applying data cleaning in a dataset 
    using its Dirichlet distribution fitted to its observations. 
    The outliers values are determined based on their distribution 
    and a threshold of 10

    Parameters
    ----------
    Dataset : pd.DataFrame
        Dataset in which data cleaning operation is applied
    Threshold : int
        Threshold or quantile for determining when a value is a outlier
    
    Return
    ------
    CleanDataset : pd.DataFrame
        Dataset without outliers based on its Dirichlet distribution
    """
    QueryValues = ' & '.join(f'0 < {macronutrient} < 1' for macronutrient in Macronutrients)
    DataObservations = Dataset.query(QueryValues)

    AlphaParameters = GetAlphaParameters(DataObservations[Macronutrients])
    PDFValues = dirichlet.pdf(DataObservations[Macronutrients].T,AlphaParameters)

    CalculatedThreshold = np.percentile(PDFValues,Threshold)
    OutliersData = PDFValues < CalculatedThreshold
    return DataObservations[~OutliersData].copy()

def GetAlphaParameters(
    DataObservations:np.ndarray,
) -> np.ndarray:
    """
    Function for fitting the alpha parameters 
    of a Dirichlet distribution given a 
    set of observations using MLE method

    Parameter
    ---------
    DataObservations : np.ndarray
        Set of observatios or data which is fitted to a Direchlet distribution

    Return
    ------
    AlphaParameters : np.ndarray
        Set of alpha parameters which are best fitted for a Direchlet distribution of a set of observations
    """
    InitialAlpha = np.ones((3,))*1/3
    Result = minimize(
        LogLikelihood_Dirichlet,
        InitialAlpha,
        args=(DataObservations,),
        method='L-BFGS-B',
        bounds=[(1e-10, None)]*3
    )  
    return Result.x

def LogLikelihood_Dirichlet(
    Alpha:np.ndarray,
    DataObservations:np.ndarray,
) -> float:
    """
    Function for evaluating likelihood 
    of a set of alpha parameters in a 
    Dirichlet distribution given a 
    set of observations

    Parameters
    ----------
    Alpha : np.ndarray
        Trial or estimation of alpha parameters
    DataObservations : np.ndarray
        Set of observations which are drawn from a Dirichlet distribution

    Return
    ------
    LogLikelihood : float
        Negative log likelihood for a set of alpha parameters
    """
    Alpha_0 = np.sum(Alpha)
    Term_1 = np.sum(np.log(DataObservations)*(Alpha-1),axis=1)
    Term_2 = np.log(np.prod(gamma(Alpha))/gamma(Alpha_0))
    return -np.sum(Term_1-Term_2)