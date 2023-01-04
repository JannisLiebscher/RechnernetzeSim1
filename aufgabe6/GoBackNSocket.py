from lossy_udp_socket import lossy_udp_socket
import threading
import time

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
    #nur die nächsten 3
    if(len(obj)>0):
        for ob in obj:
            GoBackNobj.send(ob)
            time.sleep(1)
        reciveOb(obj)
    else:
        return
def reciveOb(obj):
    for ob in obj:
        timeout = False
        while ob.arrived == False:
            if ob.timeout == True:
                timeout = True
                break
        if timeout == False:
            revievcedOb.append(obj)
            print('package arrived successfully'+ str(ob.msg))
        else:
            print('package timeout'+ str(ob.msg))
            sendOb(obj)
            return


GoBackNobj = GoBackN()
lossy = lossy_udp_socket(GoBackNobj,50,('127.0.0.1',50),0.5)
revievcedOb = list()

#create n packages
obj = list()
for i in range(3):
    strMa = "HI," +str(i)
    msg = str.encode(strMa)
    obj.append(package(msg, 5))

#start first window
sendOb(obj)


lossy.stop()


