from lossy_udp_socket import lossy_udp_socket
import threading
import time


WINDOWSIZE = 1000
NUMEROFPACKEGES = 256
counter = 0
TIMEOUT = 2
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
            print('s: '+str(s))
            print('counter: ' + str(counter))
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
for i in range(NUMEROFPACKEGES):
    strMa = "HI," +str(i)
    msg = str.encode(strMa)
    obj.append(package(msg, TIMEOUT))

#start first window
sendOb(obj)


lossy.stop()


