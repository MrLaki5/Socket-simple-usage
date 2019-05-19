import socket
import io
import sys
from time import sleep
from PIL import Image
from PIL import ImageFile

def int_to_bytes(x):
    return x.to_bytes((x.bit_length() + 7) // 8, 'big')

def int_from_bytes(xbytes):
    return int.from_bytes(xbytes, 'big')

ImageFile.LOAD_TRUNCATED_IMAGES = True

HOST = '192.168.1.107'
PORT = 8082

print(HOST)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        k = 1;

        imgByte = io.BytesIO()

        while (k==1):
            fileSize = s.recv(4)
            print('Receiving file size: ', fileSize)
            fileSize = int_from_bytes(fileSize)
            print('Receiving file size: ', fileSize)

            if (fileSize != 0):
                safetyBelt = 0;
                while (fileSize>0):
                    dataPart = s.recv(fileSize)
                    print('File size received: ', len(dataPart))
                    fileSize -= len(dataPart)
                    if (len(dataPart) == 0):
                        safetyBelt +=1;
                        print('File finished receiving!')
                        k = 0;
                        break;
                    #print('Data received: ', dataPart)
                    imgByte.write(dataPart)

            else:

                print('File finished receiving!')
                k = 0;

    
        imgByte.seek(0)
        print('Imgage size: ', sys.getsizeof(imgByte.read()))

        imgByte.seek(0)
        imgFin = Image.open(imgByte)
        imgFin.save('temp.jpeg')

        s.close()



