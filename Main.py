import sys,os,ast,socket
from _thread import start_new_thread,exit_thread
from PyQt4.QtGui import *
from PyQt4.QtCore import QFileInfo

a = QApplication(sys.argv)

appid = 0
def dtico():
    global appid, trgtl
    m, t, f, appid = 1, 0, 0, 0

    os.chdir(mypath+'icons\\')
    fu = 0
    for q in trgtl:
        if fu==0:
            fu = 1
            continue
        os.system('del /q /f {0}'.format('"'+q[2]+'.png'+'"'))
        if q[4] == 0:
            rm_fw_r(q[2])

    os.chdir(mypath+'links\\')
    fu = 0
    for q in trgtl:
        if fu==0:
            fu = 1
            continue
        os.system('del /q /f {0}'.format('"'+q[2]+'.lnk'+'"'))

    os.chdir(mypath)
    trgtl = [['C:\WINDOWS\system32\svchost.exe', appid, 'Windows Services', mypath + 'win.png', 1, 0]]

    un = rlc(''.join(list(os.popen("echo %username%"))))
    os.system('copy C:\\Users\%s\Desktop\*.lnk "'%un +mypath+'links"')
    os.system('copy C:\\Users\Public\Desktop\*.lnk "'+mypath+'links"')
    print('copy C:\\Users\Public\Desktop\*.lnk "'+mypath+'links"')
    appsList = list(os.popen('dir "'+mypath+'links\*.lnk" /s /b'))
    print('AppList = ',appsList)

    for lnk in appsList:
        if QFileInfo(lnk.replace('\n','')).symLinkTarget().endswith('.exe'):
            ico = exico(lnk.replace('\n',''))
            if ico:
                bn = os.path.basename(rlc(lnk)).replace('.lnk', '')
                trgtl.append([QFileInfo(rlc(lnk)).symLinkTarget(), m, bn, mypath+"icons\\"+bn+'.png', 1, 0])
                t += 1
                m += 1
            else:
                f += 1

    print("trgtl=", trgtl)
    print(len(appsList), t, f, sep="  ")

    trgtrfrsh(mypath + 'sf.ngd', 1, str(trgtl))
    trgtrfrsh(mypath+'sf.ngd',4,str(t))



def exico(lnkpath):
    if lnkpath.endswith('.lnk'):
        ipl = QFileInfo(lnkpath).symLinkTarget()
    elif lnkpath.endswith('.exe'):
        ipl = lnkpath
    else:
        return False

    ip = QFileInfo(ipl)
    i = QFileIconProvider().icon(ip)
    px = i.pixmap(32, 32)
    b = px.save(mypath+'icons\\'+os.path.basename(lnkpath).replace('.lnk','.png').replace('.exe','.png'))
    print(mypath+'icons\\'+os.path.basename(lnkpath).replace('.lnk','.png').replace('.exe','.png'),b)
    return b



winapp = []
class SWidget(QWidget):

    widget = QWidget()
    grid = QGridLayout(widget)


    def __init__(self,parent=None):
        QWidget.__init__(self,parent)

        l = QGridLayout(self)
        l.setContentsMargins(0,30,0,0)
        # l.setSpacing(0)

        s = QScrollArea()
        l.addWidget(s)



        f = QFont("Times", 13)

        cn1 = QLabel('Icon')
        cn2 = QLabel('Name')
        cn3 = QLabel('Internet Access')
        cn1.setFont(f)
        cn2.setFont(f)
        cn3.setFont(f)
        self.grid.addWidget(cn1,0,0)
        self.grid.addWidget(cn2,0,1)
        self.grid.addWidget(cn3,0,2)

        print("Here Trgt lst = ",trgtl)
        self.addDtApps()
        self.addUserApps() #======================#####==========================#
        self.addWS()

        print('winapp=', winapp)
        print(len(winapp))

        s.setWidget(self.widget)

        self.setGeometry(50,50,self.widget.width()+30, 650)
        self.setFixedSize(self.widget.width()+20, 650)
        self.setWindowTitle("Simba")


        slotlist = []
        i = 0
        while i < len(winapp):
            slotlist.append("winapp[{0}][0].clicked.connect(lambda: allow_prev(winapp[{1}][1], winapp[{2}][2],winapp[{3}][0],winapp[{4}][3],winapp[{5}][4]))\n".format(i, i, i, i, i,i))
            i += 1

        exec(''.join(slotlist))



    def addApp(self, lst, bsn, iconpath, fwf, abf):
        global appid
        lab = QLabel(self)
        lab.setPixmap(QPixmap(iconpath))
        self.grid.addWidget(lab, appid+1, 0)
        appn = QLabel(bsn, self)
        appn.setFont(QFont("Times", 13))
        self.grid.addWidget(appn, appid+1, 1)
        lst.append([QPushButton, int, str, int, int])
        lst[appid][0] = QPushButton(self)
        lst[appid][0].setCheckable(True)
        lst[appid][0].setFont(QFont("Times", 11))
        if abf:
            lst[appid][0].setChecked(1)
            lst[appid][0].setText('Blocked')
        else:
            lst[appid][0].setChecked(0)
            lst[appid][0].setText('Allowed')
        self.grid.addWidget(winapp[appid][0], appid+1, 2)
        lst[appid][1] = appid
        lst[appid][2] = bsn
        lst[appid][3] = fwf
        lst[appid][4] = 0
        appid += 1

    def addDtApps(self):
        for x in trgtl:
            self.addApp(winapp, x[2], x[3], x[4], x[5])

    def addUserApps(self):
        for x in ual:
            self.addApp(winapp,x[2],x[3],x[4],x[5])

    def addWS(self):
        for x in wsl:
            self.addApp(winapp,x[2],x[3],x[4],x[5])

    def clear(self):
        if self.grid != None :
            while self.grid.count():
                child = self.grid.takeAt(0)
                if child.widget() is not None:
                    child.widget().deleteLater()
                elif child.layout() is not None:
                    self.clear(child.layout())




def allow_prev(id, name, btn,fwf,abf):
    start_new_thread(allow_prev_th,(id, name, btn, fwf, abf))

def allow_prev_th(id, name, btn,fwf, abf):
    if btn.isChecked():
        btn.setText('Blocking..')
    else:
        btn.setText('Allowing..')

    if fwf:
        fwf = new_fw_r(trgtl[id][0],name)
    else:
        pass

    trgtl[id][4],winapp[id][3] = fwf,fwf
    print("ID =", id, '|| Name =', name, '|| Path =', trgtl[id][0], '|| Is Checked =', btn.isChecked())
    if btn.isChecked():
        os.system("netsh advfirewall firewall set rule name=\"{0}_in\" new dir=in profile=any action=block".format(name))
        os.system("netsh advfirewall firewall set rule name=\"{0}_out\" new dir=out profile=any action=block".format(name))
        btn.setText('Blocked')
        trgtl[id][5], winapp[id][4] = 1, 1
    else:
        os.system("netsh advfirewall firewall set rule name=\"{0}_in\" new dir=in profile=any action=allow".format(name))
        os.system("netsh advfirewall firewall set rule name=\"{0}_out\" new dir=out profile=any action=allow".format(name))
        btn.setText('Allowed')
        trgtl[id][5], winapp[id][4] = 0, 0

    trgtrfrsh(mypath+'sf.ngd',1,str(trgtl))
    exit_thread()


def rlc(string):
    lst = list(string)
    lst[len(lst) - 1] = ''
    string = ''.join(lst)
    return string

def trgtrfrsh(file,ln,newstr):
    f = open(file,"r")
    oldstr = f.readlines()
    f.close()

    print(oldstr)
    oldstr[ln] = newstr+'\n'
    # oldstr[ln + 1] = str(int(oldstr[ln + 1].replace('/n', '')) + 1) + '\n'
    print(oldstr)

    f = open(file,'w')
    f.writelines(oldstr)
    f.close()


def new_fw_r(exepath,name):

    if '.exe' in exepath:
        fw1 = os.system("netsh advfirewall firewall add rule name=\"{0}_in\" dir=in action=allow program=\"{1}\" profile=any enable=yes".format(name, exepath.replace('/','\\')))
        fw2 = os.system("netsh advfirewall firewall add rule name=\"{0}_out\" dir=out action=allow program=\"{1}\" profile=any enable=yes".format(name, exepath.replace('/','\\')))
    else:
        fw1 = os.system("netsh advfirewall firewall add rule name=\"{0}_in\" dir=in interface=any action=allow remoteip={1} enable=yes".format(name,exepath))
        fw2 = os.system("netsh advfirewall firewall add rule name=\"{0}_out\" dir=out interface=any action=allow remoteip={1} enable=yes".format(name,exepath))

    if fw1 == fw2:
        return fw1
    else:
        return 1

def rm_fw_r(name):
    os.system("netsh advfirewall firewall delete rule name=\"{0}_in\" dir=in profile=any".format(name))
    os.system("netsh advfirewall firewall delete rule name=\"{0}_out\" dir=out profile=any".format(name))


def addexefun():
    exepath = QFileDialog.getOpenFileName(w, "Open", 'C:/Program Files','*.exe').replace('/','\\')
    if not exepath:
        pass
    else:
        exico(exepath)
        bn = os.path.basename(exepath).replace('.exe','')
        ual.append([exepath, appid, bn, mypath+'icons\\'+bn+'.png', 1, 0])
        w.addApp(winapp, bn, mypath+'icons\\'+bn+'.png',1,0)
        trgtrfrsh(mypath+'sf.ngd',2,str(ual))
        trgtrfrsh(mypath + 'sf.ngd', 4, str(appid))
        print(bn)

def addsitefun():
    ws.show()

# Web Site Window

def siteab(site):
    print(site)

    if wg.isActiveWindow():
        wg.close()

    try:
        ipaddr = socket.gethostbyname(site)
    except:
        print("Must be connected to the internet")
        wg.show()
        return

    wsl.append([ipaddr, appid, site, mypath+'ws.png', 1, 0])
    w.addApp(winapp, site, mypath+'ws.png',1,0)
    trgtrfrsh(mypath+'sf.ngd',3,str(wsl))
    trgtrfrsh(mypath + 'sf.ngd', 4, str(appid))


ws = QWidget()
ws.setWindowTitle('Add Web Site')
ws.resize(260,40)

te = QLineEdit(ws)
te.resize(200,30)
te.move(5,5)
te.setText('www.example.com')

bs = QPushButton(ws)
bs.setText('Add')
bs.resize(50,30)
bs.move(207,5)
bs.setShortcut('Enter')

bs.clicked.connect(lambda:siteab(te.text()))


def wgclose():
    wg.close()

wg = QWidget()
wg.setWindowTitle("Warning")
wg.setFixedSize(280,70)
wl = QLabel(wg)
wl.move(20,10)
wl.setFont(QFont("Times",13))
wl.setText("Must be connected to the internet")
wb = QPushButton(wg)
wb.setText("OK")
wb.move(100,35)
wb.setShortcut('Enter')
wb.clicked.connect(wgclose)


def reffun():
    start_new_thread(reffunth,())

def reffunth():
    global appid
    w.clear()

    dtico()

    for v in ual:
        v[1] = appid
        appid+=1
    for v in wsl:
        v[1] = appid
        appid+=1

    trgtrfrsh(mypath+'sf.ngd',2,str(ual))
    trgtrfrsh(mypath + 'sf.ngd', 3, str(wsl))
    w.addDtApps()
    w.addUserApps()
    w.addWS()
    print("Refreshed")
    # exit_thread()

# ==========================Main=================================


if getattr(sys,'frozen',False):
    mypath = os.path.dirname(sys.executable).replace('/','\\') + '\\'
else:
    mypath = os.path.dirname(__file__).replace('/','\\') + '\\'
print("Here", mypath)


wsl = []
ual = []
trgtl = []
try:
    sf = open('sf.ngd','r')
    sfrs = sf.readlines()
    sf.close()
    trgtl = ast.literal_eval(sfrs[1])
    ual = ast.literal_eval(sfrs[2])
    wsl = ast.literal_eval(sfrs[3])
except:
    sf = open(mypath+'sf.ngd','w')
    sf.writelines('1\n'+str(trgtl) + '\n' + str(ual) + '\n' + str(wsl) + '\n%s\n' %0)
    sf.close()
    os.system('mkdir  "{0}icons" "{0}links"'.format(mypath))
    dtico()


print(trgtl)

os.chdir(mypath+'icons\\')
icoList = list(os.popen('dir *.png /s /b'))
print(os.path.curdir)

# #to remove all rules
# for rule in trgtl:
#     rm_fw_r(rule[2


w = SWidget()

addexe = QPushButton(w)
addexe.setText("Add exe")
addexe.resize(70,30)
addexe.clicked.connect(addexefun)

addsite = QPushButton(w)
addsite.setText("Add Web Site")
addsite.move(70,0)
addsite.clicked.connect(addsitefun)

refresh = QPushButton(w)
refresh.setText("Refresh")
refresh.move(170,0)
refresh.clicked.connect(reffunth)


w.show()
sys.exit(a.exec_())