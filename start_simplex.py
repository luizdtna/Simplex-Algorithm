import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout
from PyQt5.QtWidgets import QPushButton, QLineEdit, QSizePolicy, QLabel, QTextEdit
from simplex import search_better
from simplex_face import Ui_Dialog


class tela_principal(QMainWindow):
    def __init__(self, num_variables, num_restrictions, is_max, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Minha calculadora')
        #self.setFixedSize(400,400) #400x400 a tela

        self.cw = QWidget() #central Widget
        self.grid = QGridLayout(self.cw)
        self.setCentralWidget(self.cw)

        self.row_FO = []
        self.restrictions = []
        self.variables = 'abcdefghijklmnopqrstuvwxyz'
        self.real_num_variables = num_variables

        self.labelFunObj = QLabel()
        self.labelFunObj.setText('Função Objetivo:')
        self.grid.addWidget(self.labelFunObj, 0, 0, 1, 1)
        self.labelFunObj.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)



        """self.display = QLineEdit() #cria um imput
        self.grid.addWidget(self.display,0,1,1,1) # adiciona na grid
        self.display.setStyleSheet(
            '* {background: #FFF; color: #000; font-size: 10px}'
        )"""



        self.loop_func_obj(num_variables,1,0,1,1,self.variables)

        self.label_restrictions = QLabel()
        self.label_restrictions.setText('Restrições:')
        self.grid.addWidget(self.label_restrictions, 2, 0, 1, 1)
        self.label_restrictions.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)

        self.loop_variables(num_variables,num_restrictions,3,0,1,1,self.variables,arrayrow = [])

        #self.do_matrix(num_variables, num_restrictions)

        #print(self.restrictions[2][3])


        #for i in self.row_FO:
        #    print(i.text())

        self.btnSend = QPushButton()
        self.btnSend.setText('Enviar')
        self.grid.addWidget(self.btnSend,10,0,1,1,)
        self.btnSend.clicked.connect(
            lambda : self.display.setText((search_better(self.do_matrix(num_variables,num_restrictions), is_max)))
        )
        #self.line_result = QLineEdit

        self.display = QTextEdit()  # cria um imput
        self.grid.addWidget(self.display, 11, 0, 1, 8)  # adiciona na grid
        self.display.setDisabled(True)
        self.display.setStyleSheet(
            '* {background: #FFF; color: #000; font-size: 10px}'
        )
        self.display.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)

    def insert_in_view(self):
        pass

    def loop_func_obj(self,num_variables, row,col, rowspan, colspan, var):

        if num_variables != 0:
            label_var = self.real_num_variables - num_variables
            self.row_FO.append(self.func_obj(QLineEdit(''), row, col, rowspan, colspan, QLabel(var[label_var]+' +'),num_variables))
            self.loop_func_obj(num_variables-1,row,col+2,rowspan, colspan, var)


    def func_obj(self, lineEdit_FO,row,col, rowspan, colspan, varLabel, num_variables):
        self.grid.addWidget(lineEdit_FO,row,col, rowspan, colspan)
        #self.grid.addWidget(varLabel,row,col+1, rowspan, colspan)

        if num_variables != 1:
            self.grid.addWidget(varLabel, row, col + 1, rowspan, colspan)
        else:
            varLabel.setText(varLabel.text()[:-2])
            self.grid.addWidget(varLabel, row, col + 1, rowspan, colspan)

        return lineEdit_FO

    def loop_variables(self,num_variables,num_restrictions, row,col, rowspan, colspan, var,arrayrow):

        if num_variables != 0:
            label_var = self.real_num_variables - num_variables
            arrayrow.append(self.set_variables(QLineEdit(''), row, col, rowspan, colspan, QLabel(var[label_var]+' +'),num_variables))
            self.loop_variables(num_variables-1,num_restrictions,row,col+2,rowspan, colspan, var, arrayrow)

        elif num_restrictions != 0:
            arrayrow.append(self.set_variables(QLineEdit(''), row, col, rowspan, colspan, QLabel(var[num_variables]),num_variables,last_variable=True))
            self.restrictions.append(arrayrow)
            if num_restrictions != 1:


                arrayrow = []
                num_variables = self.real_num_variables
                #arrayrow.append(self.set_variables(QLineEdit(''), row+1, col, rowspan, colspan, QLabel(var[num_variables])))
                self.loop_variables(num_variables,num_restrictions-1, row+1, 0, rowspan, colspan, var, arrayrow)

        #print(arrayrow)

    def set_variables(self,lineEdit_Variables,row,col, rowspan, colspan, varLabel,num_variables, last_variable = False):
        if not last_variable:
            self.grid.addWidget(lineEdit_Variables,row,col, rowspan, colspan)

            if num_variables != 1:
                self.grid.addWidget(varLabel,row,col+1, rowspan, colspan)
            else:
                varLabel.setText(varLabel.text()[:-2])
                self.grid.addWidget(varLabel, row, col + 1, rowspan, colspan)

            #    self.grid.addWidget(QLabel('+'), row, col + 2, rowspan, colspan)


            return lineEdit_Variables
        else:

            self.grid.addWidget(QLabel('<='), row, col + 1, rowspan, colspan)
            self.grid.addWidget(lineEdit_Variables, row, col+2, rowspan, colspan)
            #self.grid.addWidget(self.label_less_or_equal, row, col + 1, rowspan, colspan)
            return lineEdit_Variables
    def do_matrix(self, num_variables, num_restrictions):

        matrix = []

        cont = 0
        array_restrictions_test = []
        for i in range(num_restrictions):
            for j in range(num_variables + 1):
                if cont == num_variables:
                    #print(self.restrictions[i][j].text())
                    array_restrictions_test.append(self.restrictions[i][j].text())
                    matrix.append(array_restrictions_test)
                    array_restrictions_test = []
                    cont = 0
                else:
                    #print(self.restrictions[i][j].text(), end=' ')
                    array_restrictions_test.append(self.restrictions[i][j].text())
                    cont += 1
        array_FO_teste = []
        for i in range(num_variables):
            array_FO_teste.append(self.row_FO[i].text())
        array_FO_teste.append(0)
        matrix.append(array_FO_teste)

        return matrix

    def show_resul(self):
        pass

class StartApp(QMainWindow, Ui_Dialog):
    def __init__(self, parent=None):
        self.novo3 = 0
        super().__init__(parent)
        super().setupUi(self)
        self.pushButton.clicked.connect(self.isNumeric)

    def isNumeric(self):
        try:
            num_variables = float(self.lineEdit.text())
            num_restrictions = float(self.lineEdit_2.text())
            self.redirect_app(num_variables,num_restrictions)
        except Exception as e:
            self.label_warning.setStyleSheet('color: red')
            self.label_warning.setText('Formato errado')


    def redirect_app(self, num_variables, num_restrictions):
        #novo3 = RedimensionarImg()
        is_max = self.radioButton_2.isChecked()
        aux = tela_principal(int(num_variables),int(num_restrictions), is_max)
        aux.show()
        #self.novo3 = tela_principal(num_variables,num_restrictions)
        #self.novo3.show()
        self.close()








if __name__ == '__main__':
    qt = QApplication(sys.argv)
    novo2 = StartApp()
    novo2.show()

    qt.exec_()

"""if __name__ ==  '__main__':
    qt = QApplication(sys.argv)
    calc = tela_principal(3, 3)
    calc.show()
    qt.exec()"""