import os
from matplotlib.figure import Figure

def SaveFig(Fig:Figure,Path:str,NameTitle:str) -> None:
    """
        Función para guardar la figura del plot 
        en una ruta y nombre

        Parameters
        ----------
            Fig : Figure
            
            Path : str
            
            NameTitle : str
    """
    base_path = './Documentation/Resources/'+Path+'/'
    os.makedirs(base_path,exist_ok=True)
    Fig.savefig(base_path+NameTitle)