from lossy_udp_socket import lossy_udp_socket
import threading
import time
import base64

WINDOWSIZE = 5
NUMEROFPACKEGES = 256
counter = 0
TIMEOUT = 0.1
class GoBackN():
    def send(self,package):
        package.timer()
        lossy.send(package.msg)

    def receive(self,msg):
        message = msg.decode('utf-8')
        m =message.split(',')
        obj[int(m[1])].arrived = True

class  package():
    def __init__(self,msg,time):
        self.msg = msg
        self.time = time
        self.timeout = False
        self.arrived = False

    def timer(self):
        thread = threading.Thread(target=self.startTimer)
        thread.start()


    def startTimer(self):
        currentTime = 0
        while currentTime < self.time and self.arrived == False:
            time.sleep(1)
            currentTime = currentTime +1
        if not self.arrived == True:
            self.timeout = True


def sendOb(obj):

    if(counter <= len(obj)):
        s= 0
        while s< WINDOWSIZE and s+counter< len(obj):
            #print('s: '+str(s))
            #print('counter: ' + str(counter))
            obj[counter+s].arrived = False
            obj[counter + s].timeout = False
            GoBackNobj.send(obj[counter+s])
            #time.sleep(3)
            s = s+1
        reciveOb(obj)
    else:
        return
def reciveOb(obj):
    global counter
    for ob in obj[counter:]:
        while ob.arrived == False:
            if ob.timeout == True:
                break
        if ob.timeout == False:
            counter= counter +1
            print('package arrived successfully' + str(ob.msg) + '\n')
            if len(obj)>= counter+WINDOWSIZE:
                GoBackNobj.send(obj[counter+WINDOWSIZE-1])

        else:
            print('package timeout'+ str(ob.msg))
            sendOb(obj)
            return



GoBackNobj = GoBackN()
lossy = lossy_udp_socket(GoBackNobj,50,('127.0.0.1',50),0.1)
revievcedOb = list()

#create n packages
obj = list()
f = open('newfile',"wb")
f.seek(1000-1)
f.write(b"\0")
f.close

with open('newfile', 'r') as file:
    data = file.read().replace('\n', '')

for i in range(NUMEROFPACKEGES):
    #strMa = "HI," +str(i)
    #
    #msg = base64.b64encode(f)
    msg = data + ',' +str(i)
    mssg = str.encode(msg)
    obj.append(package(mssg, TIMEOUT))

#start first window
summe = 0
start = time.time()
sendOb(obj)
ende = time.time()
print('{:5.3f}'.format(ende-start))

lossy.stop()
# windowsize 10 = 28.156
# WINDOWSIZE 5 = 22.282
# WINDOWSIZE 3 = 24.282










