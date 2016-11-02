#!/usr/bin/python

import sys, csv, site, os
from PyQt4 import QtCore, QtGui, uic, Qt

from srcdplayground import SrcdPlayground
from srcdrest import SrcdRest
from countries import *

VERSION_PATH = os.getcwd() + '/VERSION'
MAIN_UI_PATH = os.getcwd() + '/ui/mainwindow.ui'
HS_URL = 'https://secure.helpscout.net/conversation/'
form_class = uic.loadUiType(MAIN_UI_PATH)[0]
 
class MyWindowClass(QtGui.QMainWindow, form_class):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)

        # Read version number from a file
        with open(VERSION_PATH, 'r') as content_file:
            version = content_file.read()
        self.setWindowTitle("Resourcer-v" + version);
        
        self.bq = SrcdPlayground()
        self.rest = SrcdRest()

        # Set the list of similar components from the groupboxes
        self.languagesW = [self.languageCombo0,
                           self.languageCombo1,
                           self.languageCombo2,
                           self.languageCombo3]

        self.relevancesW = [self.relevant0,
                            self.relevant1,
                            self.relevant2,
                            self.relevant3]

        self.ecosystemsW = [self.ecosystemCombo0,
                            self.ecosystemCombo1,
                            self.ecosystemCombo2,
                            self.ecosystemCombo3]

        self.countriesW = [self.countryCombo0,
                           self.countryCombo1,
                           self.countryCombo2,
                           self.countryCombo3]


        langs = [{'language': ''}] + self.bq.getLanguages()
        ecos =  [{'ecosystem': ''}] + self.bq.getEcosystems()
        countries = [{'country': ''}] + [{'country': 'French Speaking'}] + [{'country': 'Schengen Area'}, {'country': 'Spanish Speaking'}] +  self.bq.getCountries()
        # fill the combobox with the information
        for lang  in langs:
            for i in range(len(self.languagesW)):
                self.languagesW[i].addItem(lang['language'])

        for eco in ecos:
            for i in range(len(self.ecosystemsW)):
                self.ecosystemsW[i].addItem(eco['ecosystem'])

        for i in range(len(self.countriesW)):
            for country in countries:
                self.countriesW[i].addItem(country['country'])
            self.countriesW[i].insertSeparator(4)
                
        # Table not editable
        self.resultTable.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        # Table without lines
        self.resultTable.setShowGrid(False)

        # Signals
        self.resultTable.itemClicked.connect(self.__followUrl)
        # self.openLinksButton.clicked.connect(self.__openLinks)
        self.csvButton.clicked.connect(self.__handleSave)
        self.searchButton.clicked.connect(self.__search)
        # self.resetButton.clicked.connect(self.__resetWigets)

        # self.statusBar.showMessage('Connected to BigQuery::srcd-playground')

    def __followUrl(self, item):
        if item.column() == 4:
            data = item.data(QtCore.Qt.UserRole).toPyObject()
            QtGui.QDesktopServices.openUrl(QtCore.QUrl(HS_URL + str(data)))
        elif item.column() == 5:
            email = self.resultTable.item(item.row(), 0).text()
            linkedin = self.rest.getLinkedin(str(email))
            QtGui.QDesktopServices.openUrl(QtCore.QUrl(linkedin))
        elif item.column() == 6:
            email = self.resultTable.item(item.row(), 0).text()
            github = self.rest.getGithub(str(email))
            QtGui.QDesktopServices.openUrl(QtCore.QUrl(github))

    # def __openLinks(self):
    #     start = int(self.comboRowCount.currentText()) - 1
    #     end = start + 10
    #     rows = self.resultTable.rowCount() - 1

    #     # recalculate end just in case overflows rows
    #     end = rows if end > rows else end

    #     for row in xrange(start, end + 1):
    #         link = self.resultTable.item(row, 3).text()
    #         QtGui.QDesktopServices.openUrl(QtCore.QUrl(link))

    def __handleSave(self):
        path = QtGui.QFileDialog.getSaveFileName(
                self, 'Save File', '', 'CSV(*.csv)')
        if not path.isEmpty():
            with open(unicode(path), 'wb') as stream:
                writer = csv.writer(stream)
                for row in range(self.resultTable.rowCount()):
                    rowdata = []
                    for column in range(self.resultTable.columnCount()):
                        item = self.resultTable.item(row, column)
                        if item is not None:
                            rowdata.append(
                                unicode(item.text()).encode('utf8'))
                        else:
                            rowdata.append('')
                    writer.writerow(rowdata)
                    
    def __search(self):
        # self.__queryTimerInit()
        langs = self.__createLangInfo()
        ecos = self.__createEcoInfo()
        countries = self.__createCountryInfo()
        report = True if self.withReportCheckbox.isChecked() else False
        ANDlangs = True if self.languageRadioAnd.isChecked() else False
        ANDecos =  True if self.ecosystemRadioAnd.isChecked() else False
        
        # print langs
        # print ecos
        # print countries

        self.__removeRows(self.resultTable)
        # self.comboRowCount.clear()
        
        if len(langs) >= 0:
            self.query = self.bq.getQuery(langs, ecos, countries, report, ANDlangs, ANDecos)
            
            # print query in the table
            self.resultTable.setSortingEnabled(False)
            for cand in self.query:
                self.__addRow(cand['email'], cand['country'], cand['report'], cand['PageRank'], cand['hs'])
            self.resultTable.setSortingEnabled(True)
            # self.__fillComboRows()
        
    # def __fillComboRows(self):
    #     allRows = self.resultTable.rowCount()
    #     self.comboRowCount.clear()
    #     for i in range(1, allRows, 10):
    #         self.comboRowCount.addItem(str(i))

    
    def __addRow(self, email, country, report, pagerank, link):
        # emailItem = QtGui.QTableWidgetItem("")
        # emailItem.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
        # emailItem.setCheckState(QtCore.Qt.Unchecked)
        emailItem = QtGui.QTableWidgetItem(unicode(email))
        countryItem = QtGui.QTableWidgetItem(unicode(country))
        reportItem = QtGui.QTableWidgetItem(unicode(report))
        reportColor = QtGui.QColor('red') if report == 'No' else QtGui.QColor('green')
        reportItem.setTextColor(QtGui.QColor(reportColor))
        pagerankItem = QtGui.QTableWidgetItem(unicode("{0:.2f}".format(float(pagerank))))
        linkFont = QtGui.QFont()
        linkFont.setUnderline(True)
        hsItem = QtGui.QTableWidgetItem(unicode('View'))
        hsItem.setData(QtCore.Qt.UserRole, link)
        hsItem.setTextColor(QtGui.QColor(QtGui.QColor('blue')))
        hsItem.setFont(linkFont)
        linkedinItem = QtGui.QTableWidgetItem(unicode('View'))
        linkedinItem.setTextColor(QtGui.QColor(QtGui.QColor('blue')))
        linkedinItem.setFont(linkFont)
        githubItem = QtGui.QTableWidgetItem(unicode('View'))
        githubItem.setTextColor(QtGui.QColor(QtGui.QColor('blue')))
        githubItem.setFont(linkFont)
        
        self.resultTable.insertRow(0)
        self.resultTable.setItem(0, 0, emailItem)
        self.resultTable.setItem(0, 1, countryItem)
        self.resultTable.setItem(0, 2, reportItem)
        self.resultTable.setItem(0, 3, pagerankItem)
        self.resultTable.setItem(0, 4, hsItem)
        self.resultTable.setItem(0, 5, linkedinItem)
        self.resultTable.setItem(0, 6, githubItem)
                
    def __removeRows(self, table):
        while table.rowCount():
            table.removeRow(0)
            
    def __createLangInfo(self):
        result = []
        for i in range(len(self.languagesW)):
            value = unicode(self.languagesW[i].currentText())
            relevant = True if self.relevancesW[i].isChecked() else False
            if value != '':
                result.append([value, relevant])
        return result

    def __createArrays(self, comboArray):
        result = []
        for i in range(len(comboArray)):
            value = unicode(comboArray[i].currentText())
            if value != '':
                result.append(value)
        return result
                       
    def __createEcoInfo(self):
        return self.__createArrays(self.ecosystemsW)

    def __createCountryInfo(self):
        result = []
        for i in range(len(self.countriesW)):
            value = unicode(self.countriesW[i].currentText())
            if value != '':
                if value == 'Schengen Area':
                    result += C_SCHENGEN
                elif value == 'French Speaking':
                    result += C_FRENCH
                elif value == 'Spanish Speaking':
                    result += C_SPANISH
                else:
                    result.append(value)
        return result

    # def __resetWigets(self):
    #     for i in range(len(self.languagesW)):
    #         self.languagesW[i].setCurrentIndex(0)

    #     for i in range(len(self.relevancesW)):
    #         self.relevancesW[i].setCheckState(QtGui.Unchecked)
            
    #     for i in range(len(self.ecosystemsW)):
    #         self.ecosystemsW[i].setCurrentIndex(0)

    #     for i in range(len(self.countriesW)):
    #         self.countriesW[i].setCurrentIndex(0)

if __name__ == '__main__':
    # sys.path.insert(0, os.path.abspath('.'))
    # Add system site-packages, otherwise it will fail
    sys.path = site.getsitepackages() + sys.path
    app = QtGui.QApplication(['Resourcer'])
    myWindow = MyWindowClass(None)
    myWindow.show()
    app.exec_()    
