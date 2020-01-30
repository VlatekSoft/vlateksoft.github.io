#!/usr/bin/env python
# coding: utf-8

# python -m PyQt5.uic.pyuic interface.ui -o  interface.py -x перевод ui в py
from PyQt5 import QtWidgets, QtCore, QtGui 
from interface import Ui_MainWindow

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
import datetime
import time
import logging
import re #регулярки
from clickhouse_driver import Client
def clickconnect():
    ### тут лежит параметры авторизации к базе данныех
clickconnect()
logging.basicConfig(filename='logs.log', filemode='a', level=logging.INFO, format='%(message)s;%(funcName)s;%(lineno)d;%(name)s;%(created)f;%(levelname)s;%(msecs)d;')

start_time = datetime.datetime.now()
start_time.strftime("%Y-%m-%d %H:%M:%S")

import sys
sys.setrecursionlimit(100000)
print(sys.getrecursionlimit())
def now ():
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")

###### параметры точности 
SpecTrParam = 0.5
ReadGrzParam =0.7
BadQualityParam = 0.6
VidoizmGrzParam = 0.8


driver = webdriver.Chrome(executable_path='C:\MVSautoclick\chromedriver.exe') #запускаем эмулятор браузера
driver.set_window_size(1700, 1000)
url = #some url

driver.get(url)
numtabs = 1 #сколько вкладок открыть дополнительно

for i in range(numtabs):
    driver.execute_script("var url = arguments[0]; window.open(url)", url) #октрываем вкладки
    #driver.execute_script("window.open()") #октрываем пустые вкладки


indextab = 0
focus = driver.window_handles
driver.switch_to.window(focus[indextab])
def tabchanger(indextab): #принимает индекс текущей владки и назначает следующий
    alltabs = driver.window_handles #смотрим какие вкладки открыты
    if indextab < len(alltabs)-1:   indextab += 1
    else: indextab = 0
    driver.switch_to.window(alltabs[indextab])
    return indextab	

def comebacker(indextab): #принимает индекс текущей владки и назначает предыдущий
    alltabs = driver.window_handles #смотрим какие вкладки открыты
    if indextab > 0:   indextab -= 1
    else: indextab = len(alltabs)-1
    driver.switch_to.window(alltabs[indextab])
    return indextab	

countclick = 0 #счетчик кликов
def countclicker(countclick):
    countclick +=1
    #if countclick%100 == 0: print("Скорость средняя: ",  countclick/(int((now() - start_time).total_seconds())/3600) , " кликов в час")  
    print("Кликов сделано: ", countclick)
    return countclick
sqlstat = False



class ExampleApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.NoAdress)
	#далее куча подобных кнопок которые связанных сигналами-слотами

    def parsing(self): 
        global idevent, GRZtext, KladrColor, checknesoversh, checknodate, Arhivcheck, marka
        #GRZtext, TextKladr, TextCamera, KladrColor, TimeEvent, checknesoversh, checknodate = None
        try: 
            GRZtext = driver.find_element_by_css_selector("input[class=' x-form-field x-form-text road-numbers ']").get_property("value")
            print(GRZtext)
        except:
            GRZtext = driver.find_element_by_css_selector("input[class=' x-form-field x-form-text road-numbers']").get_property("value")
            print(GRZtext) ###################### получаем номер ГРЗ 
            #logging.error(now())

        try: 
            idevent = driver.find_elements_by_xpath("//*[contains(text(), 'ДАННЫЕ НАРУШЕНИЯ')]")
            idevent = idevent[0].text[-10:-2]

            print('idevent ', idevent)
        except:
            print('ошибка парсинга ID нарушения')
  
        try: 
            KladrColor = driver.find_elements_by_css_selector("textarea[class=' x-form-field x-form-textarea']")
            KladrColor = KladrColor[(len(KladrColor)-1)].value_of_css_property("background-color") #получаем цвет фона элемента
            print(KladrColor)
            if KladrColor == 'rgba(255, 127, 127, 1)': KladrColor = 1
            elif KladrColor == 'rgba(255, 255, 255, 1)': KladrColor = 2  
            else: KladrColor = 0
            print('Kladr', KladrColor)
        except:
            print('Ошибка поиска кладр')
            KladrColor = 0
            logging.info(now())
        try:
            Arhivcheck = driver.find_elements_by_css_selector("img[title='Карточка регистрации архивная!']")
            print(Arhivcheck[0])
            Arhivcheck = len(Arhivcheck)
            print('arhiv len', Arhivcheck)
        except: 
            Arhivcheck = 0
            print('arhiv', Arhivcheck)
            logging.info(now())
        
        try:   
            marka = driver.find_elements_by_xpath("//*[contains(text(), 'Марка')]")[1] #поиск элемента по тексту
            marka = marka.find_element_by_xpath('..') #поиск родителя элемента
            marka = marka.find_element_by_css_selector("input").get_property("value") #вытаскиваем текст поля
            marka = marka.split()[0]
            print('markapars', marka)
        except:
            print('Марка не читается')
            marka = 0
        try:
            checknodate = driver.find_element_by_xpath("//*[contains(text(), 'Нет даты рождения')]").get_property("value") #поиск элемента по тексту
        except:
            checknodate = 'nobirthday' #print(checknodate)
            print('Дата рождения есть')
            #logging.error(now())
        try: 
            checknesoversh = driver.find_element_by_xpath("//*[contains(text(), 'Несовершеннолетний собственник')]").get_property("value")
        except:
            checknesoversh = 'sovershen'
            print('Несовершеннолетний не найден')
            #logging.info(now())
        print('\nparsing result: ', checknesoversh, checknodate, GRZtext, KladrColor) ###################### парсер время
       
    def sqlrequest(self):
            global idevent, client, sqlresult, sqlresult2, grzcafap, grzml, sptranspml, badqualityml, vidoizmgrzml, readgrzac, sqlstat
            try:
                sqlresult = client.execute(f"SELECT v_regno,  quality,  contour_quality, recognize,  spec_transport, brands_brand FROM inference_viols WHERE tr_viol_id={idevent} ")
                sqlresult = str(sqlresult)
                print(sqlresult, '\n', len(sqlresult))
                if len(sqlresult)>2: 
                    sqlstat = True
                    sqlresult2 = client.execute(f"SELECT probability FROM inference_viols WHERE tr_viol_id={idevent} ")

                    sqlresult2 = str(sqlresult2)
                    print(sqlresult2, '\n', len(sqlresult2))
                
                    reg = re.compile('[^a-zA-Z0-9а-яА-я.,]') 
                    sqlresult =(reg.sub("", sqlresult)).split(',')  #фильтруем от мусора и разделяем
                
                    sqlresult2 =(reg.sub("", sqlresult2)).split(',')
                
                #    print(sqlresult, '\n фильтрованный 1', len(sqlresult),'\n')
                
                #    print(sqlresult2, '\n фильтрованный 2', len(sqlresult))
                else: sqlstat = False
                print('sqlstat', sqlstat)
            except:
                print('Ошибка SQL запроса')
                logging.error(now())
                sqlstat = False


    def sqlparsing(self):
            global markaml, markaml2, sqlresult, sqlresult2, grzcafap, grzml, sptranspml, badqualityml, vidoizmgrzml, readgrzac, sqlstat
            if sqlstat:    
            #try:
                grzcafap = str(sqlresult[0:1]).lower() #грз с цафап
                grzml = str(sqlresult[3:4]).lower() #распознанный сеткой грз
                sptranspml = sqlresult[4:5] #спецтранспорт
                sptranspml = float(sptranspml[0])
                readinggrz = sqlresult2 #нечитаемый грз, точность распознавания
                #print('\n',  readinggrz, '\n')
                
                badqualityml = sqlresult[2:3] #неудовлетворительное качество фото
                badqualityml = float(badqualityml[0])
                #lprtype= sqlresult[-13:-12] # вид траспорта? узнать
                vidoizmgrzml = sqlresult[1:2] #видоизмененый грз
                vidoizmgrzml = float(vidoizmgrzml[0]) #минимальная точность распознавания всех символов грз нейросетью
                markaml = str(sqlresult[5:6]).strip('[]\'')
                markaml2 = str(sqlresult[6:7]).strip('[]\'')
                 print(markaml)
                
                readgrzac = 1.0
                for i in range (len(readinggrz)):
                    if readinggrz[i] != '':
                        if float(readinggrz[i]) < readgrzac: 
                            readgrzac = float(readinggrz[i])
                print('\n sql request:', '\n marka', markaml, '\n grzcaf', grzcafap, '\n grzml \n', grzml, '\n -1 sptranspml \n', sptranspml, '\n badqual \n', badqualityml,  '\nnvidoizm\n ',vidoizmgrzml, '\nreadgrz\n ', readgrzac)
            #except:
                #print('Ошибка SQL парсера')
                #sqlstat = False
            else: sqlstat = False
######29-01
    def changecolor(self):
        if nobirthdaystat: self.pushButton_17.setStyleSheet('QPushButton {background-color: red; color: white; font: bold}') #нет даты рождения
        if not18stat: self.pushButton_16.setStyleSheet('QPushButton {background-color: red; color: white; font: bold}') #не совершеннолетний собвственник
        if noadresstat: self.pushButton.setStyleSheet('QPushButton {background-color: red; color: white; font: bold}') #нет адреса кладр
        if datanotstat: self.pushButton_19.setStyleSheet('QPushButton {background-color: red; color: white; font: bold}') #данных не найдено
        if arhivstat: self.pushButton_18.setStyleSheet('QPushButton {background-color: red; color: white; font: bold}') #архивная
    
 ############### 29-01
    def checkconditions(self): #проверяем данные по нейросетям, если условия совпадают, в дальнейшем подкрашываем кнопки и автокликаем
        global unknownstat, brakevents, grzstat, sptranstat, unreadgrzstat, badqualitystat, vidoizmgrzstat, markastat, nobirthdaystat, not18stat, noadresstat, datanotstat, arhivstat
        unknownstat=brakevents=grzstat=sptranstat=unreadgrzstat=badqualitystat=vidoizmgrzstat=markastat=nobirthdaystat=not18stat=noadresstat=datanotstat=arhivstat=None
        if checknodate != 'nobirthday': 
            brakevents = nobirthdaystat = True
        if checknesoversh != 'sovershen': 
            brakevents = not18stat = True
        if KladrColor == 1: 
            brakevents = noadresstat = True
        if KladrColor == 2: 
            brakevents = datanotstat = True
        if Arhivcheck > 0: 
            brakevents = arhivstat = True

        if sqlstat:
            if grzcafap != grzml: brakevents = grzstat = True
            if (1 > sptranspml > SpecTrParam) and (100 > sptranspml >(SpecTrParam*100)): brakevents = sptranstat = True
            if not (ReadGrzParam < readgrzac < 1): brakevents = unreadgrzstat = True
            if not (BadQualityParam < badqualityml < 1): brakevents = badqualitystat = True
            if not (VidoizmGrzParam < vidoizmgrzml < 1) and not ((VidoizmGrzParam*100) < vidoizmgrzml < 100): brakevents = vidoizmgrzstat = True
            if not (marka == markaml) and not (marka == markaml2) : brakevents = markastat = True #если марка с фронта не совпадает с нейросеткой
        if not sqlstat and not brakevents: unknownstat = True #если не пришел sql и не было красных парсеров


##### 29-01
    def changecolorml(self):
        global sqlstat, brakevents
        print('unknownstat, brakevents, grzstat, sptranstat, unreadgrzstat, badqualitystat, vidoizmgrzstat, markastat, nobirthdaystat, not18stat, noadresstat, datanotstat, arhivstat\n', 
        unknownstat, brakevents, grzstat, sptranstat, unreadgrzstat, badqualitystat, vidoizmgrzstat, markastat, nobirthdaystat, not18stat, noadresstat, datanotstat, arhivstat)
        if sqlstat:
            if grzstat: self.pushButton_11.setStyleSheet('QPushButton {background-color: red; color: white; font: bold}') #на перепроверку при не совпадении номеров
            if sptranstat: self.pushButton_2.setStyleSheet('QPushButton {background-color: red; color: white; font: bold}') #спецтранспорт
            if unreadgrzstat: self.pushButton_9.setStyleSheet('QPushButton {background-color: red; color: white; font: bold}') #нечитаемый грз
            if badqualitystat: self.pushButton_10.setStyleSheet('QPushButton {background-color: red; color: white; font: bold}') #неудовл. качество фото
            if vidoizmgrzstat: self.pushButton_14.setStyleSheet('QPushButton {background-color: red; color: white; font: bold}') #видоизм
            if markastat: self.pushButton_5.setStyleSheet('QPushButton {background-color: red; color: white; font: bold}') #данные тс не достоверны
        if not sqlstat:
            print('Не запускаем обновление подсветки т.к.  sql false') 
            brakevents = True   
        if not brakevents:  self.pushButton_15.setStyleSheet('QPushButton {background-color: green; color: white; font: bold}') #подсветка проверено
    
    def autoclick(self): #зацикленный автоклик по материалам
        time.sleep(0.5)
        if countclick > 30000: print("Обработано материалов", countclick)
        elif not brakevents:  #если зеленая кнопка
            self.Provereno()
        elif noadresstat: #нет адреса кладр 1
            self.NoAdress()
        elif datanotstat:  #данных не найдено 2
            self.DataNot()
        elif arhivstat:  #архивная 3
            self.Arhiv()
            #print('Архив условие')            
        elif nobirthdaystat: #нет даты рождения 4
            self.NoBirthday()
        elif not18stat:  #не совершеннолетний собвственник 5
            self.Not18()
        elif sqlstat:
            if grzstat: self.Recheck() #несовпадение грз - перепроверка
            elif sptranstat: self.SpecTransp()
            elif unreadgrzstat: self.UnreadGRZ()
            elif badqualitystat: self.BadQuality()
            elif vidoizmgrzstat: self.VidoizmGRZ()
            elif markastat: self.DataTSWrong()
        elif unknownstat: self.Recheck() #если ничего не подсвечивали - перепроверка
        else: print('Ошибка автокликера')
  
    def cleancolor(self): #очищаем кнопки от подсветки
        self.pushButton.setStyleSheet('font: bold')
        self.pushButton_2.setStyleSheet('font: bold')
        self.pushButton_3.setStyleSheet('font: bold')
        self.pushButton_4.setStyleSheet('font: bold')
        self.pushButton_5.setStyleSheet('font: bold')
        self.pushButton_7.setStyleSheet('font: bold')
        self.pushButton_8.setStyleSheet('font: bold')
        self.pushButton_9.setStyleSheet('font: bold')
        self.pushButton_10.setStyleSheet('font: bold')
        self.pushButton_11.setStyleSheet('font: bold')
        self.pushButton_12.setStyleSheet('font: bold')
        self.pushButton_13.setStyleSheet('font: bold')
        self.pushButton_14.setStyleSheet('font: bold')
        self.pushButton_15.setStyleSheet('font: bold')
        self.pushButton_16.setStyleSheet('font: bold')
        self.pushButton_17.setStyleSheet('font: bold')
        self.pushButton_18.setStyleSheet('font: bold')
        self.pushButton_19.setStyleSheet('font: bold')



    def fasttab(self): #переключение вкладок вперед
        global indextab
        indextab = tabchanger(indextab)
        self.cleancolor()
        self.parsing()
        self.changecolor()
        self.sqlrequest()
        self.sqlparsing()
        self.changecolorml()
    def comebacktab(self): #переключение вкладок назад
        global indextab
        indextab = comebacker(indextab)
    def stop(self):
        print('stopped')

    def keyPressEvent(self , e): #считываем клавиши
        key = e.key()
        if key == QtCore.Qt.Key_F:
            self.Provereno()
        elif key == QtCore.Qt.Key_9:
            self.stop()
        elif key == 1040:
            self.Provereno()
        elif key == QtCore.Qt.Key_C:
            self.Provereno()
        elif key == 1057:
            self.Provereno()
        elif key == QtCore.Qt.Key_X:
            self.Provereno()
        elif key == QtCore.Qt.Key_1:
            self.NoAdress()
        elif key == QtCore.Qt.Key_2:
            self.SpecTransp()
        elif key == QtCore.Qt.Key_3:
            self.NoSvetofor()      
        elif key == QtCore.Qt.Key_Q:
            self.fasttab() 
        elif key == 1049:
            self.fasttab() 
        elif key == QtCore.Qt.Key_Z:
            self.comebacktab()
        elif key == 1071:
            self.fasttab() 
        elif key == QtCore.Qt.Key_V:
            self.Provereno()
        elif key == 1052:
            self.Provereno()
        elif key == 16777220: #enter
            self.Provereno()
        elif key == QtCore.Qt.Key_O:
            self.changeadress()
        elif key == QtCore.Qt.Key_Escape:
            self.close()   
        elif key == QtCore.Qt.Key_L:
            self.testchangeml()  

    def testchangeml(self):
        global TimeEvent, TextCamera, GRZtext
        TimeEvent = '2019-12-30 20:20:00'
        TextCamera = 'AS5000334'
        GRZtext = 'а530от199'
        self.sqlrequest()
        self.sqlparsing()
        self.changecolorml()

    def changeadress(self):  #это для теста R
        print('смена')
        driver.execute_script('''setTimeout(function() {  let link = document.querySelectorAll('button');   link = Array.from( link ).filter( e => (/.../i).test( e.textContent ) );  link[1].click(); });''')
        driver.execute_script('''setTimeout(function() {  let link = document.querySelectorAll('button');   link = Array.from( link ).filter( e => (/Проверить/i).test( e.textContent ) );  link[0].click(); });''')
        driver.execute_script('''setTimeout(function() {  let link = document.querySelectorAll('button');   link = Array.from( link ).filter( e => (/ОК/i).test( e.textContent ) );  link[0].click(); });''')
        logging.info(now(), countclick)

##### 29-01 добавил новые функции
    def buttonsend(self):
        global indextab, countclick
        indextab = tabchanger(indextab)
        countclick = countclicker(countclick)
        logging.info(now())
        #self.cleancolor()
        self.parsing()
        self.sqlrequest()
        self.sqlparsing()
        self.checkconditions()
        self.changecolor()
        self.changecolorml()
        self.autoclick()

    def NoAdress(self):          
        driver.execute_script(''' JS ''')# тут лежат вызываетс JS скрипт которые работает на вебстранице
          self.buttonsend()
        #print('Нет адреса')
   #### далее куча других 
    
    def error(self):
        logging.exception(now())
        raise Exception('Страница не успела загрузиться \n или вы открыли посторонний сайт. \n Переключитесь на другую вкладку (клавиши Q или Z)')

def my_excepthook(type, value, tback):
    QtWidgets.QMessageBox.critical(
        window, "ERROR", str(value),
        #QtWidgets.QMessageBox.Cancel
        QtWidgets.QMessageBox.Ok
    )
        
    sys.__excepthook__(type, value, tback)
sys.excepthook = my_excepthook

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = ExampleApp()
    window.show()
    app.exec_()
