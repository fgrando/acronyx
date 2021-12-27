import sys
import re
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QPushButton, QWidget, QLabel, QLineEdit, QAction, QTextEdit, QPlainTextEdit, QTabWidget,QVBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot, QSettings


class Core:
    def __init__(self):
        self.dic = {}
        self.excluded = []

    def loadDefinitions(self, path):
        with open(path, 'r') as fd:
            for line in fd.readlines():
                items = line.strip().split(',')
                if len(items) > 1:
                    self.dic[items[0]] = '\n'.join(items[1:])

    def getDefinition(self, word):
        try:
            definition = self.dic[word]
        except:
            definition = '?'
        return definition

    def getAbbrevs(self, text):
        return re.findall(r'[A-Z][A-Z]+', text, re.DOTALL)

    def setExcludedTerms(self, text):
        self.excluded = text.split(',')

    def getHtmlTable(self, text):
        abbreviations = self.getAbbrevs(text)
        table = ''
        for abbrev in abbreviations:
            if abbrev in self.excluded:
                continue
            definition = self.getDefinition(abbrev)
            row = f'<tr><td>{abbrev}</td><td>{definition}</td></tr>'
            row = row.replace('\n','<br>') # replace new lines by html new lines
            table = table + row + '\n'
        return f'<table border="1">{table}</table>'




class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.core = Core()
        self.title = 'Acronyx'
        self.left = 0
        self.top = 0
        self.width = 400
        self.height = 300
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        self.settings = QSettings("history.ini", QSettings.IniFormat)
        self.table_widget = MyTableWidget(self)
        self.setCentralWidget(self.table_widget)
        self.show()




class MyTableWidget(QWidget):

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.core = parent.core
        self.settings = parent.settings
        self.layout = QVBoxLayout(self)
        self.EXCLUDED = 'excluded'
        
        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()

        self.tabs.currentChanged.connect(self.buildTable)
        
        # Add tabs
        self.tabs.addTab(self.tab1,"1. Paste text here")
        self.tabs.addTab(self.tab2,"2. Edit acronyms")
        self.tabs.addTab(self.tab3,"3. Copy the result table")
        
        # Create first tab
        self.tab1.layout = QVBoxLayout(self)
        self.textAreaIn = QPlainTextEdit("""
        Lorem Ipsum is simply dummy text of the printing and typesetting industry.
        Lorem BBL has been the industry's standard dummy AFK ever since the 1500s,
        when an unknown printer took a galley BBS type and scrambled it to make a YOUR specimen book.
        It has survived not only BTW centuries,
        but also the leap into electronic typesetting, remaining essentially unchanged.
        It was popularised in BBIAB 1960s with the release of Letraset EG containing
        Lorem Ipsum passages, and more recently with desktop publishing software like Aldus
        PageMaker including versions BRB Lorem Ipsum.
        """)
        self.tab1.layout.addWidget(self.textAreaIn)
        self.tab1.setLayout(self.tab1.layout)

        # Create second tab
        self.tab2.layout = QVBoxLayout(self)
        self.lineEditPath = QLineEdit()
        self.pushButtonDic = QPushButton ("Choose dictionary file")
        self.pushButtonDic.clicked.connect(self.selectDic)
        self.tab2.layout.addWidget(self.pushButtonDic)
        self.tab2.layout.addWidget(self.lineEditPath)
        self.labelExcluded = QLabel('Comma separated excluded terms:')
        excluded = self.settings.value(self.EXCLUDED)
        self.lineEditExcluded = QLineEdit(excluded)
        self.tab2.layout.addWidget(self.labelExcluded)
        self.tab2.layout.addWidget(self.lineEditExcluded)
        self.tab2.setLayout(self.tab2.layout)

        # Create last tab
        self.tab3.layout = QVBoxLayout(self)
        self.textAreaOut = QTextEdit ()
        #self.textAreaOut.setReadOnly(True)
        self.tab3.layout.addWidget(self.textAreaOut)
        self.tab3.setLayout(self.tab3.layout)

        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    def loadDictionary(self, path):
        self.lineEditPath.setText(path)
        self.core.loadDefinitions(path)

    def buildTable(self, i):
        if i == 2:
            txt = self.textAreaIn.toPlainText()
            excludedCsv = self.lineEditExcluded.text()
            self.settings.setValue(self.EXCLUDED, excludedCsv)
            self.core.setExcludedTerms(excludedCsv)
            self.textAreaOut.setHtml(self.core.getHtmlTable(txt))

    def selectDic(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            self.loadDictionary(fileName)
        


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
