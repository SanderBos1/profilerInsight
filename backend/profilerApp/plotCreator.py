import numpy as np
import base64
import io
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

class plotCreator:
    """
    A class for creating plots. it can create serveral kinds of plots.
    """
    def __init__(self, data:np.ndarray, columnName:str):
        """
        Initializes the plotCreator with the given parameters.

        Parameters:
        - columnName (str): The name of the column corresponding to the data.
        - data (np.ndarray): The data to be plotted.
        """
        self.data = data
        self.image = None
        self.columnName = columnName

    def getImage(self, plotType:str):
        """
        creates a plot of the data and returns it as a base64 encoded string.
        
        Parameters:
         - plotType (str): The type of plot to create. Can be either "histogram" or "boxplot".

        """
        if plotType == "histogram":
            self.createHistogram()
        elif plotType == "boxplot":
            self.createBoxplot()
        else:
            return "Not implemented Yet"
        
        return self.image

    def createBoxplot(self):
        """
        creates a boxplot of the data and sets self.data as the base64 encoded string of the plot.
    
        """
        boxplotData = self.data[~np.isnan(self.data)]

        plt.figure(figsize=(4, 3))
        plt.boxplot(boxplotData, patch_artist=True, medianprops=dict(color='#5b5d62'), boxprops=dict(facecolor='#fe5000', color='orange'))

        img_stream = io.BytesIO()
        plt.title(f'Boxplot of {self.columnName}')

        plt.savefig(img_stream, format='png')
        plt.close()  
        img_bytes = img_stream.getvalue()
      
        img_base64 = base64.b64encode(img_bytes).decode('utf-8')
        self.image = img_base64

    def createHistogram(self):
        """
        creates a Histogram of the data and sets self.data as the base64 encoded string of the plot.
    
        """
        plt.figure(figsize=(4, 3))
        plt.hist(self.data, bins=20, edgecolor='#5b5d62', color='#fe5000')
        plt.title(f'Histogram of {self.columnName}')
        plt.xlabel('Value')
        plt.ylabel('Frequency')

        img_stream = io.BytesIO()
        plt.savefig(img_stream, format='png')
        plt.close()  
        img_bytes = img_stream.getvalue()
      
        img_base64 = base64.b64encode(img_bytes).decode('utf-8')
        self.image = img_base64
        
