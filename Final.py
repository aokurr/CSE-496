import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLineEdit, QTextEdit, QComboBox,QLabel
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class NetworkxGraphApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.G = None
        self.initUI()

    def initUI(self):
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        
        self.graph_button = QPushButton("Create Graph", self)
        self.graph_button.clicked.connect(self.showEnterField1)
        self.layout.addWidget(self.graph_button)
        
        self.enter_button1 = QPushButton("Enter", self)
        self.enter_button1.clicked.connect(self.generateGraph)
        self.enter_button1.hide()
        
        self.k_entry1 = QLineEdit(self)
        placeholder = " " * 110 + "Enter Number Of Node" + " " * 10
        self.k_entry1.setPlaceholderText(placeholder)
        
        self.p_combobox = QComboBox(self)
        self.p_combobox.hide()
        self.p_combobox.addItem("0.2")
        self.p_combobox.addItem("0.4")
        self.p_combobox.addItem("0.6")
        self.p_combobox.addItem("0.8")
        self.p_combobox.setCurrentIndex(3)
        # Başlangıçta 0.2 seçili olsun
        self.layout.addWidget(self.p_combobox)

        self.k_entry1.hide()
        self.layout.addWidget(self.k_entry1)
        self.layout.addWidget(self.enter_button1)
        
        
        
        self.runAlgorithm_button = QPushButton("Run Algorithm", self)
        self.runAlgorithm_button.clicked.connect(self.showEnterField)
        self.layout.addWidget(self.runAlgorithm_button)

        

        self.enter_button = QPushButton("Enter", self)
        self.enter_button.clicked.connect(self.runAlgorithm)
        self.enter_button.hide()
        
        self.k_entry = QLineEdit(self)
        placeholder = " " * 110 + "Enter Number of K-pack" + " " * 10
        self.k_entry.setPlaceholderText(placeholder)


        self.k_entry.hide()
        self.layout.addWidget(self.k_entry)
        self.layout.addWidget(self.enter_button)
   
        self.figure = plt.figure(figsize=(10, 8))  # Figure boyutlarını ayarla
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)
        
        self.setWindowTitle("NetworkX ve PyQt5 Uygulaması")
        self.setGeometry(0, 0, 800, 600)
        
    
    
    def generateGraph(self):
        k_input = self.k_entry1.text()
        edge_input = float(self.p_combobox.currentText())
        self.k_entry1.hide()
        self.enter_button1.hide()
        self.p_combobox.hide()
        if not k_input:  # Eğer k_input boşsa
            k_input = int(-1)  # k_input'a -1 değerini ata
        else:
            k_input = int(k_input)
        düğüm_sayısı =int( k_input)  
        k = 3
        p = float(edge_input)
        
        if düğüm_sayısı!= -1:
            self.G = self.create_connected_watts_strogatz_graph(düğüm_sayısı,k,p)

        else:
            self.G = nx.Graph([
                    ('A', 'B'), ('A', 'C'), ('B', 'D'),
                    ('C', 'K'), ('D', 'E'), ('E', 'G'), ('E', 'F'), 
                    ('D', 'K'),('C','T')
                ])

        self.figure.clear()
        nx.draw(self.G, with_labels=True, font_weight='bold', node_color='skyblue', node_size=700, font_size=14)
        self.canvas.draw()

    def showEnterField(self):
        self.k_entry.show()
        self.enter_button.show()
        
    def showEnterField1(self):
        self.k_entry1.show()
        self.p_combobox.show()
        self.enter_button1.show()
        

    def runAlgorithm(self):
        k_input = self.k_entry.text()
        self.k_entry.hide()
        self.enter_button.hide()
        try:
            k = int(k_input)
            if k < 2:
                raise ValueError("k değeri en az 2 olmalıdır.")
            distance=k+1
            distance_sets = self.find_distance_networkx(self.G, distance)
            two_dimensional_list = [list(s) for s in distance_sets.values()]# Sonuçları yazdır
            i=0
            subSets = []
            for vertex, min_k_set in distance_sets.items():
                listVertex = list(min_k_set)
                x=self.find_incorrect_node(distance_sets, listVertex)
                subSets.append(x)
                subSets[i].append(vertex)
                i+=1
            self.find_largest_sublist(subSets,k)
        except ValueError as ve:
            print("error")
            
    def bfs_distance_networkx(self,G, start, k):
        distance = {start: 0}
        min_k_nodes = set()

        for u, v in nx.bfs_edges(G, start):
            if v not in distance:
                distance[v] = distance[u] + 1
                if distance[v] >= k:
                    min_k_nodes.add(v)
                        
        return min_k_nodes

    def find_distance_networkx(self,G, k):
        sets = {}
        for vertex in G:
            sets[vertex] = self.bfs_distance_networkx(G, vertex, k)
        return sets

    def search(self,Grap,element1,element2):
        values=Grap.get(element2)
        if element1 in values:
            return False
        else:
            return True

    def find_incorrect_node(self,Grap,vertex):
       i=0
       j=0
       while i<len(vertex)-1:
           j=i+1
           while j < len(vertex): 
               if self.search(Grap,vertex[i],vertex[j]):  
                   vertex.pop(j)
                   j=j-1
               j=j+1
           i=i+1
       return vertex
    def create_connected_watts_strogatz_graph(self,n, k, p, max_tries=100):
       for _ in range(max_tries):
            G = nx.watts_strogatz_graph(n, k, p)
            if nx.is_connected(G):
                return G
       raise Exception(f"Bağlı bir graf {max_tries} denemede oluşturulamadı.")
    def find_largest_sublist(self, two_dim_list,k):
        largest_sublist = None
        largest_length = 0
    
        for sublist in two_dim_list:
            if len(sublist) >= 2 and len(sublist) > largest_length:
                largest_sublist = sublist
                largest_length = len(sublist)
        self.generateGraph2(largest_sublist,k)
        return largest_sublist

    
    def generateGraph2(self, highlight_nodes=[],k=None):
        self.figure.clear()

        if not highlight_nodes:
            plt.text(0.5, 0.5, f" {k}-packing number could not be found", ha='center', va='center', fontsize=16, color='red')
            color_map = ['red' if not highlight_nodes or node in highlight_nodes else 'blue' for node in self.G.nodes()]
            color_map = ['red'] * len(color_map)
            nx.draw(self.G, with_labels=True, font_weight='bold', node_color=color_map, node_size=700, font_size=14)

        else:
            color_map = ['green' if node in highlight_nodes else 'blue' for node in self.G.nodes()]
            nx.draw(self.G, with_labels=True, font_weight='bold', node_color=color_map, node_size=700, font_size=14)

        self.canvas.draw()
    def closeEvent(self, event):
        self.figure.clear()
        event.accept()
def main():
    app = QApplication(sys.argv)
    ex = NetworkxGraphApp()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
