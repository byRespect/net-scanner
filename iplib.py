from socket import *
import nmap #Nmap kütüphanesini çağırıyoruz
def networkScan(list_widget, label):
    ip_count = 0
    network = '192.168.1.1/24' #Yapılacak taramanın ip aralığı
    nm = nmap.PortScanner() #Nmap tool'unu projemize enjekte edioyurz
    nm.scan(hosts=network, arguments='-sn')  #Nmap toolunun içinde -sn komutunu çalışırıyoruz
    hosts_list = [(x, nm[x]['status']['state']) for x in nm.all_hosts()]
    for host, status in hosts_list:  #For döngüsü ile kaç tane ip adresi bulunduğunu kaydediyoruz
        list_widget.addItem(host) #Gelen hostları listWidget'ın içerisine atıyoruz
        ip_count+=1;
    if(ip_count):
        label.setText(str(ip_count) +" ADET IP ADRESİ BULUNDU.") #Kaydedtiğimiz ip adreslerini yazdırıyoruz
        label.setStyleSheet("color:green") #Yazı rengi
    else:
        label.setText("IP ADRESİ BULUNAMADI.") #Eğer bulunamazsa
        label.setStyleSheet("color:red") #Yazı rengi

def portScan(ip):
    ports = [] # Port taramak için liste oluşturuyoruz
    try:
        t_IP = gethostbyname(ip)
        for i in range(0, 500): #Aralığımızı 0 10 olarak belirliyoruz
            s = socket(AF_INET, SOCK_STREAM) #Socket oluşturup portları tarıyoruz ve çıkan sonuçları conn değişkenine atıyoruz
            conn = s.connect_ex((t_IP, i))
            if (conn == 0): #bulunan sonuçları listemize ekliyoruz
                ports.append(i)
            s.close()
    except Exception:
        pass
    finally:
        pass
    return ports