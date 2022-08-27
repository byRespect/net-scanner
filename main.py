import sys
from PyQt5 import QtWidgets # Python'un bizler için hazıladığı grafik tabanlı  PyQt5 kütüphanesini kullandık
from PyQt5.QtWidgets import *
import _thread
import iplib #İdlib dosyasını içeri import ediyoruz
select_item = ""
msgBox = None#main içinde tanımladık global'de None olarak tanımladık
# (yani null değere sahip olan değişkenimize veriyi main içinde tanımladık mainden sonra burası null kalmıyor.)

def listClick(item):#listWidget'e tıklandığında çalışacak function
    global select_item#global deki (yukarıda select_item)'i seçiyoz
    select_item = item.text()#listwidget'de tıklanmış olan item'in ismini select_item'e atıyoruz.
    #print(select_item)

def showPorts(ip):
    global msgBox#QMessageBox atadığımız global değişkinimizi alıyoruz
    text = "IP: -> " + str(ip) + "\n"#parametre olarak aldığımız ip'yi text'e arıyoruz
    # (bu text başarılı olursa mesaj kutusu içinde gösterilecek olan mesaj)
    ports = iplib.portScan(ip)#iplib'den portscan'ınımızı çalıştırıyoruz ip'ye göre ve dönen port dizililerini ports değişkenine atıyoruz
    if ports.__len__() > 0: #(ports.__len__() -> dizi uzunluğu (dizi içinde kaç tane eleman var))
        for x in ports:#ports içindeki port'ları x'e atıyoruz tek tek
            text += str(x) + "\n" # text = text + str(x) -> [burası port] + "\n" -> [burası bir alt satıra in diyoruz]
        msgBox.setWindowTitle("Portlar") # mesaj kutusunun başlığı
        msgBox.setText(text)#mesaj kutusunun içeriği
        return msgBox.exec()#mesaj kutusunu çağır
    else:
        msgBox.setWindowTitle("Hata")
        msgBox.setText("Acik Port Bulunamadi.")
        return msgBox.exec_()

def buttonClick():
    global select_item #select_item  global değişkinimizi alıyoruz
    global msgBox #QMessageBox atadığımız global değişkinimizi alıyoruz
    if(select_item):
        msgBox.setWindowTitle("Arama") #Başlık
        msgBox.setText(select_item + " üzerinden açık portlar aranıyor. Lütfen bekelyiniz.") #Seçilen Ip adresinde açık portları arıyoruz
        msgBox.exec() #MsgBox değerini göstermesini istiyoruz
        _thread.start_new_thread(showPorts, (select_item,)) #therad oluşturuyoruz
    else:
        msgBox.setWindowTitle("Hata") #eğer bulunamazsa
        msgBox.setText(select_item + "Lütfen listeden ip seçiniz.")
        msgBox.exec()

def buttonSettings(button):#burası thread'ımız. bu thread içinde sürekli bir döngü var
    while True:
        if(select_item):#eğer listeden birşey seçilmişse buton aktif olsun değilse aktif olmasın istendiği takdirde
            # port scan ettiği sürece boyuncada pasif bıraktırabiliriz
            button.setEnabled(True)
        else:
            button.setEnabled(False)

def window():
    app = QApplication(sys.argv)           #Burası Pyqt5 için gerekli settings ayarları
    formWidget = QWidget()                 # https://doc.qt.io/qtforpython/contents.html
    gridLayout = QGridLayout()
    status_label = QLabel()
    listWidget = QListWidget()
    find_port = QPushButton()
    global msgBox
    msgBox = QMessageBox()

    status_label.setText("IP ADRESLERİ BULUNUYOR...")
    status_label.setStyleSheet("color:blue")

    listWidget.resize(350, 120)
    listWidget.itemClicked.connect(listClick)

    find_port.resize(100,30)
    find_port.setText("PORT TARAMAYI BAŞLAT") #Port Tarama aralığı

    find_port.clicked.connect(buttonClick)

    gridLayout.addWidget(status_label)
    gridLayout.addWidget(listWidget)
    gridLayout.addWidget(find_port)

    formWidget.setLayout(gridLayout)
    formWidget.setWindowTitle("NETWORK SCANNER")
    formWidget.show()

    # aşağıda biz bir thread oluşturup programımıza ayrı çekirdek oluşturutup arayüzün kasmasını engelliyoruz.

    _thread.start_new_thread(iplib.networkScan , (listWidget,status_label))#thread başlatıyoruz
    _thread.start_new_thread(buttonSettings, (find_port,))
    sys.exit(app.exec())

window();