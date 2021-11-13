import sys
import os
import yaml
import git
import shutil
from PyQt5 import QtCore, QtGui, QtWidgets, uic


form_path = os.path.join(os.path.dirname(__file__), "lolbins.ui")
yaml_base = os.path.join(os.path.dirname(__file__), "source/")
git_dir = os.path.join(os.path.dirname(__file__), "source/", ".git/")
yaml_base_windows = os.path.join(os.path.dirname(__file__), "source/", "yml")
yaml_base_linux = os.path.join(os.path.dirname(__file__), "source/", "_gtfobins")
yaml_exe =  os.path.join(os.path.dirname(__file__), yaml_base,"yml", "OSBinaries")
yaml_lib = os.path.join(os.path.dirname(__file__), yaml_base,"yml", "OSLibraries")
yaml_script = os.path.join(os.path.dirname(__file__), yaml_base, "yml", "OSScripts")
yaml_other_ms = os.path.join(os.path.dirname(__file__), yaml_base, "yml", "OtherMSBinaries")
qtCreatorFile = "lolbins.ui" # Enter file here.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

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
        self.tabWidget.currentChanged.connect(self.build_list_linux) # if tab changed
    
    def check_comboBox_index(self):
        if self.comboBox.currentIndex() == 1:
            self.build_list_windows(yaml_exe)
        if self.comboBox.currentIndex() == 2:
            self.build_list_windows(yaml_lib)
        if self.comboBox.currentIndex() == 3:
            self.build_list_windows(yaml_script)
        if self.comboBox.currentIndex() == 4:
            self.build_list_windows(yaml_other_ms)        
   
    def build_list_windows(self, yml_loc):
        try:
            self.listWidget.clear()
            self.arr = sorted(os.listdir(yml_loc))
            for files in self.arr:
                if os.path.splitext(files)[1] == ".yml":
                    self.listWidget.addItem(os.path.splitext(files)[0])  
        except:
            pass
    
    
    def GetItemName_windows(self):
        if self.comboBox.currentIndex() == 1:
            self.yaml_file = yaml_exe
        elif self.comboBox.currentIndex() == 2:  
            self.yaml_file = yaml_lib
        elif self.comboBox.currentIndex() == 3:
            self.yaml_file = yaml_script
        elif self.comboBox.currentIndex() == 4:  
            self.yaml_file = yaml_other_ms
        self.item = self.listWidget.currentItem().text()
        yaml_file = self.item + ".yml"
        yaml_file = os.path.join(os.path.dirname(__file__), self.yaml_file,yaml_file)
        with open(yaml_file) as f_yaml:
            for doc in yaml.safe_load_all(f_yaml):
                break
        file_output = yaml.dump(doc, allow_unicode=True, sort_keys=False, default_flow_style=False, width=300, indent = 3)
        self.textEdit.setPlainText(file_output)
    
    
    def GetItemName_linux(self):
        self.item = self.listWidget_3.currentItem().text()
        self.yaml_file = yaml_base_linux
        yaml_file = self.item + ".md"
        yaml_file = os.path.join(os.path.dirname(__file__), self.yaml_file,yaml_file)
        with open(yaml_file) as f_yaml:
            for doc in yaml.safe_load_all(f_yaml):
                break
        file_output = yaml.dump(doc, allow_unicode=True, sort_keys=False, default_flow_style=False, width=300, indent = 3)
        self.textEdit_3.setPlainText(file_output)
    
    def build_list_linux(self):
        if self.tabWidget.currentIndex() == 1:
            try:
                self.listWidget_3.clear()
                self.arr = sorted(os.listdir(yaml_base_linux))
                for files in self.arr:
                        if os.path.splitext(files)[1] == ".md":
                            self.listWidget_3.addItem(os.path.splitext(files)[0])  
            except:
                pass
        
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
            #print(remote)
            self.repository.config_writer().set_value("core", "sparseCheckout", "true")
            with open(sparse_checkout, "a") as file_object:
                file_object.write("yml")
            
            self.repository.remotes.origin.pull("master")
        except:
            pass

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
            #print(remote)
            self.repository.config_writer().set_value("core", "sparseCheckout", "true")
            with open(sparse_checkout, "a") as file_object:
                file_object.write("_gtfobins")
            
            self.repository.remotes.origin.pull("master")
        except:
            pass

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
