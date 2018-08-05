try:
    from PyQt5.QtGui import *
    from PyQt5.QtCore import *
    from PyQt5.QtWidgets import *
except ImportError:
    from PyQt4.QtGui import *
    from PyQt4.QtCore import *

from libs.lib import newIcon, labelValidator

BB = QDialogButtonBox


class LabelDialog(QDialog):

    def __init__(self, text="Enter object label", trackid=0, parent=None, listItem=None):
        super(LabelDialog, self).__init__(parent)

        self.label1 = QLabel()
        self.label1.setText('Category: ')

        self.edit = QLineEdit()
        # self.edit.move(30, -20)
        self.edit.setText(text)
        self.edit.setFixedWidth(200)
        self.edit.setValidator(labelValidator())
        self.edit.editingFinished.connect(self.postProcess)

        # self.label2 = QLabel()
        # self.label2.setText('TrackID: ')
        # self.trackedit = QLineEdit()
        # self.trackedit.setText(str(trackid))
        # self.trackedit.setFixedWidth(40)
        # self.trackedit.setValidator(QIntValidator())
        # self.trackedit.editingFinished.connect(self.postProcess1)

        model = QStringListModel()
        model.setStringList(listItem)
        completer = QCompleter()
        completer.setModel(model)
        self.edit.setCompleter(completer)

        layout = QVBoxLayout()
        layout.addWidget(self.label1)
        layout.addWidget(self.edit)
        # layout.addWidget(self.label2)
        # layout.addWidget(self.trackedit)
        self.buttonBox = bb = BB(BB.Ok | BB.Cancel, Qt.Horizontal, self)
        bb.button(BB.Ok).setIcon(newIcon('done'))
        bb.button(BB.Cancel).setIcon(newIcon('undo'))
        bb.accepted.connect(self.validate)
        bb.rejected.connect(self.reject)
        layout.addWidget(bb)

        if listItem is not None and len(listItem) > 0:
            self.listWidget = QListWidget(self)
            for item in listItem:
                self.listWidget.addItem(item)
            self.listWidget.itemClicked.connect(self.listItemClick)
            self.listWidget.itemDoubleClicked.connect(self.listItemDoubleClick)
            layout.addWidget(self.listWidget)

        self.setLayout(layout)

    def validate(self):
        try:
            if self.edit.text().trimmed():
                self.accept()
        except AttributeError:
            # PyQt5: AttributeError: 'str' object has no attribute 'trimmed'
            if self.edit.text().strip():
                self.accept()

    def postProcess(self):
        try:
            self.edit.setText(self.edit.text().trimmed())
        except AttributeError:
            # PyQt5: AttributeError: 'str' object has no attribute 'trimmed'
            self.edit.setText(self.edit.text())

    # def postProcess1(self):
    #     try:
    #         self.trackedit.setText(self.trackedit.text().trimmed())
    #     except AttributeError:
    #         # PyQt5: AttributeError: 'str' object has no attribute 'trimmed'
    #         self.trackedit.setText(self.trackedit.text())

    def popUp(self, text='', move=True):
        self.edit.setText(text)
        self.edit.setSelection(0, len(text))
        self.edit.setFocus(Qt.PopupFocusReason)
        # trackid = int(self.trackedit.text())
        if move:
            self.move(QCursor.pos())
        return self.edit.text() if self.exec_() else None

    def listItemClick(self, tQListWidgetItem):
        try:
            text = tQListWidgetItem.text().trimmed()
        except AttributeError:
            # PyQt5: AttributeError: 'str' object has no attribute 'trimmed'
            text = tQListWidgetItem.text().strip()
        self.edit.setText(text)
        
    def listItemDoubleClick(self, tQListWidgetItem):
        self.listItemClick(tQListWidgetItem)
        self.validate()
