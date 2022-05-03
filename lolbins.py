#!/usr/bin/python3

#===============================================================================
#  Name        : lolbins.py
#  Author      : Hamza Megahed
#  Version     : v2.0
#  Copyright   : 
#  Description : list all Living Off The Land for Windows and Unix
#===============================================================================
import sys
import os
import git
import shutil
import glob
import sqlite3
from PyQt5 import QtCore, QtGui, QtWidgets, uic

category_dict = {
1 : "OSBinaries",
2 : "OSLibraries",
3 : "OSScripts",
4 : "OtherMSBinaries"
}
form_path = os.path.join(os.path.dirname(__file__), "lolbins.ui")
yaml_base = os.path.join(os.path.dirname(__file__), "source/")
git_dir = os.path.join(os.path.dirname(__file__), "source/", ".git/")
yaml_base_windows = os.path.join(os.path.dirname(__file__), "source/", "yml")
yaml_base_linux = os.path.join(os.path.dirname(__file__), "source/", "_gtfobins/")

Ui_MainWindow, QtBaseClass = uic.loadUiType(form_path)

class MyWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.listWidget.itemClicked.connect(self.GetItemName_windows)
        self.listWidget_3.itemClicked.connect(self.GetItemName_linux)
        self.comboBox.activated.connect(self.check_comboBox_index)
        self.pushButton.clicked.connect(self.force_update_windows)
        self.pushButton_3.clicked.connect(self.force_update_linux)
        self.pushButton_2.clicked.connect(self.search_content_windows)
        self.lineEdit_2.returnPressed.connect(self.search_content_windows)
        self.lineEdit_4.returnPressed.connect(self.search_content_linux)
        self.lineEdit.textChanged.connect(self.search_file_windows)
        self.lineEdit_3.textChanged.connect(self.search_file_linux)
        self.pushButton_4.clicked.connect(self.search_content_linux)
        self.tabWidget.currentChanged.connect(self.files_from_linux) # if tab changed
        try:
            self.connection = sqlite3.connect("lolbins.db")
            self.connection.row_factory = lambda cursor, row: row[0]
            self.cursor = self.connection.cursor()
        except:
            pass
        
    
    def check_comboBox_index(self):
        if self.comboBox.currentIndex() == 1:
            self.files_from_category_windows(category_dict[1])
        if self.comboBox.currentIndex() == 2:
            self.files_from_category_windows(category_dict[2])
        if self.comboBox.currentIndex() == 3:
            self.files_from_category_windows(category_dict[3])
        if self.comboBox.currentIndex() == 4:
            self.files_from_category_windows(category_dict[4])        
   
    def files_from_category_windows(self, category_type):
        try:
            self.listWidget.clear()
            self.arr = self.cursor.execute("SELECT file FROM windows WHERE category = ?",(category_type,),).fetchall()
            self.build_list_windows(self.arr)
        except:
            pass
            
            
    def build_list_windows(self,windows_file_list):
            for file in windows_file_list:
                self.listWidget.addItem(file)  
        
    
    def GetItemName_windows(self):
        try:
            self.textEdit.clear()
            self.item = self.listWidget.currentItem().text()
            rows = self.cursor.execute("SELECT content FROM windows WHERE file = ?",(self.item,),).fetchall()
            for row in rows:
                row += row
            self.textEdit.setPlainText(str(row))
            cursor = self.textEdit.textCursor()
            format = QtGui.QTextCharFormat()
            format.setBackground(QtGui.QBrush(QtGui.QColor("red")))
            pattern = self.lineEdit_2.text()
            re = QtCore.QRegularExpression(pattern, QtCore.QRegularExpression.CaseInsensitiveOption | QtCore.QRegularExpression.DotMatchesEverythingOption)
            i = re.globalMatch(self.textEdit.toPlainText())
            while i.hasNext():
                match = i.next() 
                cursor.setPosition(match.capturedStart(), QtGui.QTextCursor.MoveAnchor)
                cursor.setPosition(match.capturedEnd(), QtGui.QTextCursor.KeepAnchor)
                cursor.mergeCharFormat(format)
        except:
            pass

    
    def GetItemName_linux(self):
        self.item = self.listWidget_3.currentItem().text()
        rows = self.cursor.execute("SELECT content FROM linux WHERE file = ?",(self.item,),).fetchall()
        for row in rows:
                row += row
        self.textEdit_3.setPlainText(row)
        cursor = self.textEdit_3.textCursor()
        format = QtGui.QTextCharFormat()
        format.setBackground(QtGui.QBrush(QtGui.QColor("red")))
        pattern = self.lineEdit_4.text()
        re = QtCore.QRegularExpression(pattern, QtCore.QRegularExpression.CaseInsensitiveOption | QtCore.QRegularExpression.DotMatchesEverythingOption)
        i = re.globalMatch(self.textEdit_3.toPlainText())
        while i.hasNext():
            match = i.next() 
            cursor.setPosition(match.capturedStart(), QtGui.QTextCursor.MoveAnchor)
            cursor.setPosition(match.capturedEnd(), QtGui.QTextCursor.KeepAnchor)
            cursor.mergeCharFormat(format)
    

    def files_from_linux(self):
        if self.tabWidget.currentIndex() == 1:
            try:
                self.listWidget_3.clear()
                self.arr = self.cursor.execute("SELECT file FROM linux").fetchall()
                self.build_list_linux(self.arr) 
            except:
                pass
    

    def build_list_linux(self,linux_file_list):
        for linux_files in linux_file_list:
            self.listWidget_3.addItem(linux_files) 
        
    def force_update_windows(self):
        if not os.path.isdir(yaml_base):
            os.mkdir(yaml_base)
        if os.path.isdir(yaml_base_windows):
            shutil.rmtree(yaml_base_windows)
        if os.path.isdir(git_dir):
            shutil.rmtree(git_dir)

        try:
            sparse_checkout = git_dir+ "/info/sparse-checkout"
            self.repository = git.Repo.init(yaml_base)
            self.remote = self.repository.create_remote('origin', url='https://github.com/LOLBAS-Project/LOLBAS.git')
            self.repository.config_writer().set_value("core", "sparseCheckout", "true")
            with open(sparse_checkout, "a") as file_object:
                file_object.write("yml")
            self.repository.remotes.origin.pull("master")
            
        except:
            pass
        try:
            self.cursor.execute("DROP TABLE IF EXISTS windows")
            self.cursor = self.connection.cursor()
            self.cursor.execute("CREATE TABLE IF NOT EXISTS windows (category TEXT, file TEXT, content TEXT, UNIQUE (category, file, content) ON CONFLICT IGNORE)")
            for files in glob.glob(yaml_base_windows+"/**/*.yml", recursive=True):
                with open(files, "r") as file:
                    content = file.read()
                category = os.path.basename(os.path.dirname(files))
                file_name = os.path.basename(os.path.splitext(files)[0])
                self.cursor.execute("insert into windows values(?,?,?)",(category, file_name, content))
            self.connection.commit()
            self.show_msg("Please restart LOLBins!")
        except:
            self.show_msg("Something went wrong, can't update database")
    
    def show_msg(self,msg):
        self.msg = QtWidgets.QMessageBox()
        self.msg.setIcon(QtWidgets.QMessageBox.Warning)
        self.msg.setText(msg)
        self.msg.show()

    def search_file_windows(self):
        self.listWidget.clear()
        keyword = self.lineEdit.text()
        self.search_results = self.cursor.execute("SELECT file FROM windows WHERE file LIKE ?",('%'+keyword+'%',)).fetchall()
        self.build_list_windows(self.search_results)

    def search_file_linux(self):
        self.listWidget_3.clear()
        keyword = self.lineEdit_3.text()
        self.search_results = self.cursor.execute("SELECT file FROM linux WHERE file LIKE ?",('%'+keyword+'%',)).fetchall()
        self.build_list_linux(self.search_results)    

    def search_content_windows(self):
        self.listWidget.clear()
        keyword = self.lineEdit_2.text()
        self.search_results = self.cursor.execute("SELECT file FROM windows WHERE content LIKE ?",('%'+keyword+'%',)).fetchall()
        self.build_list_windows(self.search_results)

    def search_content_linux(self):
        self.listWidget_3.clear()
        keyword = self.lineEdit_4.text()
        self.search_results = self.cursor.execute("SELECT file FROM linux WHERE content LIKE ?",('%'+keyword+'%',)).fetchall()
        self.build_list_linux(self.search_results)
            
        
    
    def force_update_linux(self):
        if not os.path.isdir(yaml_base):
            os.mkdir(yaml_base)
        if os.path.isdir(yaml_base_linux):
            shutil.rmtree(yaml_base_linux)
        if os.path.isdir(git_dir):
            shutil.rmtree(git_dir)
            
        try:
            sparse_checkout = git_dir+ "/info/sparse-checkout"
            self.repository = git.Repo.init(yaml_base)
            self.remote = self.repository.create_remote('origin', url='https://github.com/GTFOBins/GTFOBins.github.io')
            self.repository.config_writer().set_value("core", "sparseCheckout", "true")
            with open(sparse_checkout, "a") as file_object:
                file_object.write("_gtfobins")
            
            self.repository.remotes.origin.pull("master")
        except:
            pass
        try:
            self.cursor.execute("DROP TABLE IF EXISTS linux")
            self.cursor = self.connection.cursor()
            self.cursor.execute("CREATE TABLE IF NOT EXISTS linux (file TEXT, content TEXT, UNIQUE (file, content) ON CONFLICT IGNORE)")
            for files in glob.glob(yaml_base_linux+"*.md", recursive=True):
                with open(files, "r") as file:
                    content = file.read()
                file_name = os.path.basename(os.path.splitext(files)[0])
                self.cursor.execute("insert into linux values(?,?)",(file_name, content))
            self.connection.commit()
            self.show_msg("Please restart LOLBins!")
        except:
            self.show_msg("Something went wrong, can't update database")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
