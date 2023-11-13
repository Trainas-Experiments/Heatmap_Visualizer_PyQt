import sys
import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QCheckBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

cmap = plt.cm.get_cmap('Greens')
colors = cmap(np.linspace(0.3, 0.8, cmap.N))
custom_colormap = mcolors.LinearSegmentedColormap.from_list('Chopped_Reds', colors)



class HeatMapWindow(QMainWindow):
    def __init__(self, data, mode=3, output='heatmap'):
        super().__init__()
        self.data = data
        self.mode = mode
        self.output = output
        self.initUI()
        if self.mode in [2, 3]:
            self.saveHeatmapImage(self.output)
        if self.mode in [1, 3]:
            self.show()

    def initUI(self):
        self.setWindowTitle('3D Array Heatmap Viewer')
        self.setGeometry(100, 100, 800, 600)
        
        # Main widget and layout
        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)
        layout = QVBoxLayout(self.main_widget)

        # Matplotlib Figure
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        # Checkboxes for layers
        self.checkboxes = []
        names = ['-1', '0', '1', '2', '3']
        for i in range(self.data.shape[2]):
            if i < len(names):
                checkbox = QCheckBox(f'Layer {i+1}: {names[i]}', self)
            else:
                checkbox = QCheckBox(f'Layer {i+1}', self)
            checkbox.setChecked(True) # May need to change this to what Dan wants or expose an algo for this to the constructor
            checkbox.stateChanged.connect(self.updatePlot)
            self.checkboxes.append(checkbox)
            layout.addWidget(checkbox)
         # Initial empty heatmap
        self.initial_heatmap = self.ax.imshow(np.zeros((self.data.shape[0], self.data.shape[1])), cmap=custom_colormap)
        self.colorbar = self.figure.colorbar(self.initial_heatmap, ax=self.ax, orientation='vertical')

        self.updatePlot()

    def updatePlot(self):
        # Aggregate selected layers
        selected_layers = [self.data[:,:,i] for i, cb in enumerate(self.checkboxes) if cb.isChecked()]
        
        # If no layers are selected, display a zero array
        if not selected_layers:
            layer_sum = np.zeros((self.data.shape[0], self.data.shape[1]))
        else:
            layer_sum = np.sum(selected_layers, axis=0)

        # Update the heatmap data
        self.initial_heatmap.set_data(layer_sum)
        
        # Update color limits if necessary
        self.initial_heatmap.set_clim(vmin=np.min(layer_sum), vmax=np.max(layer_sum))

        # Redraw the canvas
        self.canvas.draw()

    def saveHeatmapImage(self, base_filename):
        # Get current date and time
        now = datetime.datetime.now()
        date_time_tag = now.strftime("%Y%m%d_%H%M%S")

        # Construct the filename with the date-time tag
        filename = f"{base_filename}_{date_time_tag}.jpeg"

        layer_sum = self.aggregateLayers()
        fig, ax = plt.subplots()
        heatmap = ax.imshow(layer_sum, cmap=custom_colormap)
        plt.colorbar(heatmap, ax=ax, orientation='vertical')
        plt.savefig(filename, format='jpeg')
        plt.close(fig)

    def aggregateLayers(self):
        # Aggregate selected layers
        selected_layers = [self.data[:,:,i] for i, cb in enumerate(self.checkboxes) if cb.isChecked()]
        
        # If no layers are selected, return a zero array
        if not selected_layers:
            return np.zeros((self.data.shape[0], self.data.shape[1]))
        else:
            return np.sum(selected_layers, axis=0)
        

def generate_random_data(N, M):
    return np.random.randint(low=0, high=6, size=(N, N, M))


def main():
    app = QApplication(sys.argv)
    N, M = 8, 10  # Dimensions of the array
    data = generate_random_data(N, M)
    mainWindow = HeatMapWindow(data)
    mainWindow.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
