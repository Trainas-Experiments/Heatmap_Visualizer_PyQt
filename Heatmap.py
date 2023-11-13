import sys
import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QCheckBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class HeatMapWindow(QMainWindow):
    def __init__(self, data):
        super().__init__()
        self.data = data
        self.initUI()

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
        for i in range(self.data.shape[2]):
            checkbox = QCheckBox(f'Layer {i+1}', self)
            checkbox.stateChanged.connect(self.updatePlot)
            self.checkboxes.append(checkbox)
            layout.addWidget(checkbox)
         # Initial empty heatmap
        self.initial_heatmap = self.ax.imshow(np.zeros((self.data.shape[0], self.data.shape[1])), cmap='viridis')
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

def generate_random_data(N, M):
    return np.random.rand(N, N, M)


def main():
    app = QApplication(sys.argv)
    N, M = 10, 4  # Dimensions of the array
    data = generate_random_data(N, M)
    mainWindow = HeatMapWindow(data)
    mainWindow.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
