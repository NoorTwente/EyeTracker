from signal import signal
import sys

from PyQt5 import QtCore

from PyQt5.QtCore import * 
from PyQt5.QtGui import * 
from PyQt5.QtWidgets import*


class MyWidget(QWidget):
    siganl = False
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Python")
  
        self.setWindowOpacity(0.5)
  
  
        # setting  the geometry of window
        self.setGeometry(0, 0, 1920, 1080)
  
        # creating a label widget
        self.label_1 = QLabel("transparent ", self)
        # moving position
        self.label_1.move(100, 100)
  
        self.label_1.adjustSize()



        self.b1 = QPushButton('Next Image')
        self.b2 = QPushButton('Crop')
        self.b3 = QPushButton('Clear')

        self.view = GraphicsView()
        h_box = QHBoxLayout()
        v_box = QVBoxLayout()
        v_box.addWidget(self.b1)
        v_box.addWidget(self.b2)
        v_box.addWidget(self.b3)
        h_box.addWidget(self.view)
        h_box.addLayout(v_box)
        self.setLayout(h_box)
        #self.resize(800, 800)
        self.setWindowTitle("Super Duper Cropper")

        self.show()



class GraphicsView(QGraphicsView):

    def __init__(self):
        super().__init__()
        self.setScene(QGraphicsScene())
        self.item = QGraphicsPixmapItem(QPixmap('test.jpg'))
        self.scene().addItem(self.item)
        self.rect_item = QGraphicsRectItem(QRectF(), self.item)
        self.rect_item.setPen(QPen(QColor(51, 153, 255), 2, Qt.SolidLine))
        self.rect_item.setBrush(QBrush(QColor(0, 255, 0, 40)))

    #def mousePressEvent(self, event):
        #self.pi = self.mapToScene(event.pos())
        #super().mousePressEvent(event)

    #def mouseMoveEvent(self, event):
        #pf = self.mapToScene(event.pos())
        #if (self.pi - pf).manhattanLength() > QApplication.startDragDistance():
            #self.pf = pf
            #self.draw_rect()
        #super().mouseMoveEvent(event)

    #def mouseReleaseEvent(self, event):
        #pf = self.mapToScene(event.pos())
        #if (self.pi - pf).manhattanLength() > QApplication.startDragDistance():
            #self.pf = pf
            #self.draw_rect()
        #super().mouseReleaseEvent(event)

    def givePoints(self, x, y):
        self.pi = self.mapToScene(QtCore.QPoint(x, y))
        pf = self.mapToScene(QtCore.QPoint(x, y))
        if (self.pi - pf).manhattanLength() > QApplication.startDragDistance():
            self.pf = pf
            self.draw_rect()

    def draw_rect(self):
        r = QRectF(self.pi, self.pf).normalized()
        r = self.rect_item.mapFromScene(r).boundingRect()
        self.rect_item.setRect(r)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWidget()
    window.view.givePoints(300, 400)
    app.aboutToQuit.connect(app.deleteLater)
    sys.exit(app.exec_())