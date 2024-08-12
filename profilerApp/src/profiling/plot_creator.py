import base64
import io
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

matplotlib.use('Agg')

class PlotCreator:
    """
    A class for creating plots. it can create serveral kinds of plots.
    """
    def __init__(self, data:np.ndarray, column_name:str):
        """
        Initializes the plotCreator with the given parameters.

        Parameters:
        - columnName (str): The name of the column corresponding to the data.
        - data (np.ndarray): The data to be plotted.
        """
        self.data = data
        self.image = None
        self.column_name = column_name

    def get_image(self, plot_type:str):
        """
        creates a plot of the data and returns it as a base64 encoded string.
        
        Parameters:
         - plotType (str): The type of plot to create. Can be either "histogram" or "boxplot".

        """
        if plot_type == "histogram":
            self.create_histogram()
        elif plot_type == "boxplot":
            self.create_boxplot()
        else:
            return "Not implemented Yet"
        
        return self.image

    def create_boxplot(self):
        """
        creates a boxplot of the data and sets self.data as the base64 encoded string of the plot.
    
        """
        boxplot_data = self.data[~np.isnan(self.data)]

        plt.figure(figsize=(4, 3))
        plt.boxplot(boxplot_data, patch_artist=True, medianprops=dict(color='#5b5d62'), \
                    boxprops=dict(facecolor='#fe5000', color='orange'))

        img_stream = io.BytesIO()
        plt.title(f'Boxplot of {self.column_name}')

        plt.savefig(img_stream, format='png')
        plt.close()  
        img_bytes = img_stream.getvalue()
      
        img_base64 = base64.b64encode(img_bytes).decode('utf-8')
        self.image = img_base64

    def create_histogram(self):
        """
        creates a Histogram of the data and sets self.data as the base64 encoded string of the plot.
    
        """
        plt.figure(figsize=(4, 3))
        plt.hist(self.data, bins=20, edgecolor='#5b5d62', color='#fe5000')
        plt.title(f'Histogram of {self.column_name}')
        plt.xlabel('Value')
        plt.ylabel('Frequency')

        img_stream = io.BytesIO()
        plt.savefig(img_stream, format='png')
        plt.close()  
        img_bytes = img_stream.getvalue()
      
        img_base64 = base64.b64encode(img_bytes).decode('utf-8')
        self.image = img_base64
        
