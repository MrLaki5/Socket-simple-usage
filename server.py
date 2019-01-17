import socket
import io
import sys
from PIL import Image

def int_to_bytes(x):
    return x.to_bytes(4, 'big')

def int_from_bytes(xbytes):
    return int.from_bytes(xbytes, 'big')

HOST = socket.gethostbyname(socket.gethostname())
PORT = 8082

package_size = 2048;

print(HOST)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))

        img = Image.open("img.jpg")
        imgByte = io.BytesIO()
        img.save(imgByte, "JPEG")
        imgByte.seek(0)
        print('Img size in bytes: ', sys.getsizeof(imgByte.read()))
        imgByte.seek(0)

        try:
            while True:
                s.listen(0)
                s.setblocking(1)
                conn, addr = s.accept()
                with conn:
                    print('Connected by ', addr)

                    toBeSend ='a'
                    sentNum = 0;

                    while (toBeSend != b''):
                        tempNum = int_to_bytes(package_size)
                        print('Sent bytes: ', sentNum)
                        print('Number to send: ', tempNum)

                        conn.send(tempNum)


                        toBeSend = imgByte.read(package_size)
                        #print('Data to be send: ', toBeSend)

                        bytesSent =conn.send(toBeSend)
                        sentNum = sentNum + bytesSent


                    tempB = int_to_bytes(0)
                    print('Sending done')
                    conn.sendall(tempB)
                    imgByte.seek(0)
                    #imgByte.close()
                    conn.close()
        finally:
            s.close()




