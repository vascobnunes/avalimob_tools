import sys
import os
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication,QDialog
from PyQt5.uic import loadUi
from PyQt5.QtCore import QRegExp, QEvent, QObject
from PyQt5.QtGui import QRegExpValidator
from PIL import Image
from resizeimage import resizeimage


def resize_image(path, image, basewidth, qual):
    image_full_path = os.path.join(path, image)
    img = Image.open(image_full_path)
    if int(basewidth)>0:
        resizeimage.resize_width(img, int(basewidth))
    new_name = os.path.join(path, "resize" + image)
    if int(qual) > 0:
        img.save(new_name, quality=int(qual), optimize=True)
    else:
        img.save(new_name)

class avalimob(QDialog):
    def __init__(self):
        super(avalimob,self).__init__()
        loadUi('avalimob_tools.ui',self)
        self.setWindowTitle('Ferramentas de apoio a avaliacao imobiliaria')
        self.lineEdit.setText(os.getcwd())
        reg_ex = QRegExp("[0-9][0-9][0-9]")
        input_validator = QRegExpValidator(reg_ex, self.lineEdit_2)
        self.lineEdit_2.setValidator(input_validator)
        reg_ex = QRegExp("[0-9][0-9]")
        input_validator = QRegExpValidator(reg_ex, self.lineEdit_3)
        self.lineEdit_3.setValidator(input_validator)
        reg_ex = QRegExp("([a-zA-Z]:)?(\\\\[a-zA-Z0-9_.-]+)+\\\\?")
        input_validator = QRegExpValidator(reg_ex, self.lineEdit)
        self.lineEdit.setValidator(input_validator)
        self.pushButton.clicked.connect(self.on_pushButton_clicked)
        # self._filter = Filter()
        self.lineEdit.installEventFilter(self)

    def eventFilter(self, widget, event):
        # FocusOut event
        if event.type() == QEvent.FocusOut:
            files_in_path = os.listdir(self.lineEdit.text())
            self.listWidget.clear()
            self.listWidget.addItems(files_in_path)
            count_files = len(files_in_path)
            self.label_4.setText(str(count_files) + " file(s)")
            # return False so that the widget will also handle the event
            # otherwise it won't focus out
            return False
        else:
            # we don't care about other events
            return False

    def on_pushButton_clicked(self):
        filespath = self.lineEdit.text()
        resize_perc = self.lineEdit_3.text()
        rescale_perc = self.lineEdit_2.text()
        for f in os.listdir(filespath):
            if f.endswith(".jpg") or f.endswith(".png"):
                resize_image(filespath, f, resize_perc, rescale_perc)

def main():
    app=QApplication(sys.argv)
    widget=avalimob()
    widget.show()
    sys.exit(app.exec_())

if __name__ == '__main__':

    main()