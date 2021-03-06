import time
from machine import I2C
import sensor, image, lcd

clock = time.clock()
lcd.init()
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)
sensor.set_vflip(1)
sensor.set_hmirror(1)

atual = []
Dado = []
Enviado = []
pergunta = 0
entrada = 2
vl = 0

def separa(v):
    tam = len(v)
    S = []
    check = 0
    for i in range(tam):
        S.append(v[i])
        check = check + ord(v[i])
    S.append(',')
    tam = len(str(check))
    a = str(check)
    for i in range(tam):
        S.append(a[i])
    return S

def i2c_on_receive(data):
    global pergunta, entrada
    pergunta = data
    if(pergunta != 0 or pergunta != 1):
        entrada = pergunta
    else:
        entrada = 2

def i2c_on_transmit():
    if(pergunta == 0): #pergutando se tem dado
        if(Enviado == [] and len(Dado)>0): #se o tamanho do vetor de Dados for > 0
            return len(Dado) #sim ha dados
        else:
            return 0 #nao tenho dado
    else:
        if(pergunta == 1): #enviando o dado
            global vl
            caracter = ord(Dado[vl])
            vl = vl + 1
            if vl == len(Dado):
                vl = 0
                for item in Dado:
                    Enviado.append(item)
            return caracter

def i2c_on_event (event):
    print("on_event:", event)

try:
    i2c = I2C(I2C.I2C2, mode = I2C.MODE_SLAVE, scl=34, sda=35, freq=400000, addr = 0x42,
            addr_size = 7,
            on_receive = i2c_on_receive,
            on_transmit = i2c_on_transmit,
            on_event = i2c_on_event)
except Exeption as e:
    sys.print_exception(e)

while True:
    clock.tick()
    if(len(Dado)>0 and entrada == 2):
        Dado.clear()
        Enviado.clear()
        atual.clear()

    img = sensor.snapshot()
    res = img.find_qrcodes()
    if len(res) > 0:
        img.draw_string(2,2, res[0].payload(), color=(0,128,0), scale=2)
        v = res[0].payload()
        atual = separa(v)

    if(atual != Dado):
        if(len(Dado) > 0):
            Dado.clear()
            Enviado.clear()
        for cp in atual:
            Dado.append(cp)
    lcd.display(img)
