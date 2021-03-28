from ftplib import FTP
import os
import random

def auth(ftp):
    while True:
        hst = str(input('//Server connection. <Enter> will try to conncet to default 127.0.0.1 '))
        if hst == '':
            hst = '127.0.0.1'
        try:
            ftp.connect(hst)
        except ConnectionRefusedError as err:
            print('//Connection not established, check data validity')
        ftpusr = str(input('//Enter login. <Enter> will log you defaulty as anon '))
        if ftpusr != '':
            ftppass = str(input('//Enter password'))
            try:
                ftp.login(ftpusr, ftppass)
                break
            except Exception as err:
                code_err = int(str(err.args[0]).split(' ')[0])
                if code_err == 530:
                    print('//Can`t log. Check username or password ')
                else:
                    print(err.args[0])
        else:
            ftp.login()
            break
    while True:
        mode = str(input('//Mode: A is for active mode, P is for passive. <Enter> will defaultly choose P '))
        if mode == 'A':
            try:
                p1 = random.randint(1, 256)
                p2 = random.randint(1, 256)
                prm = '127,0,0,1,' + str(p1) + ',' + str(p2)
                prt = int(prm.split(',')[-1]) + int(prm.split(',')[-2]) * 256
                rsp = ftp.sendcmd('PORT ' + prm)
                print('//Active connection established at port ' + str(prt))
            except Exception as err:
                print('//Not established')
            break
        elif mode == 'P' or mode == '':
            try:
                rsp = ftp.sendcmd('PASV')
                prt = int(rsp.split(',')[-1][:-1]) + int(rsp.split(',')[-2]) * 256
                print('//Passive connection established at port ' + str(prt))
            except Exception as err:
                print(err)
            break
        else:
            print('//Wrong Input. Mode is <A> or <P> or <> (same as P')
    if ftpusr == '':
        ftpusr = 'anon'
    return ftp, ftpusr

def getHelp():
    msg = ' //This is a help message. \n //changedir <> -- change working directory \n //deletefile <filename> -- delete file with name <filename> \n //gethelp -- this command, returns list of commands. \n //listdir -- lists contents of directory. \n //makedir -- creates new direfctory, \n //shortlist -- return contents of directory (shorter). \n //currdir -- current directory name \n //exit -- stop connection \n //dwnld -- download file(s) dnwld <file1> <file2> <wheretosave> \n //removedir -- remove directory \n // storefile -- upload file(s) storefile <file1> <file2> <wheretosave> '
    print(msg)

def getlistdir(ftp):
    try:
        strngs = []
        rspns = ftp.retrlines('LIST', strngs.append)
        if int(rspns.split(' ')[0]) == 226:
            if len(strngs) == 0:
                print("//Directory is empty")
            else:
                for strng in strngs:
                    print(strng)
    except Exception as err:
        cderr = int(str(rspns[1].args[0]).split(' ')[0])
        print(rspns[1].args[0])

def getchangedir(ftp, args):
    if len(args) == 0:
        print('//use of changedir is changedir <dir>')
        return 0
    elif len(args) > 1:
        print('//use of changedir is changedir <dir>')
        return 0
    try:
        rspns = ftp.cwd(args[0])
        cd = int(str(rspns).split(' ')[0])
        if cd == 250:
            dir = rspns.split(' ')[3]
            print('//Succesfully moved to ' + dir)
    except Exception as err:
        cderr = int(str(err.args[0]).split(' ')[0])
        if cderr == 550:
            dir = err.args[0].split(' ')[3]
            print('//Eror, no directory named ' + dir + ' was found')
        else:
            print(err.args[0])

def getmakedir(ftp, args):
    if len(args) == 0:
        print('//use of makedir is ')
        return 0
    elif len(args) > 1:
        print('//use of makedir is ')
        return 0
    try:
        rspns = ftp.mkd(args[0])
        if rspns != "":
            print('//Succesfully made directory ' + rspns)
    except Exception as err:
        cderr = int(str(err.args[0]).split(' ')[0])
        if cderr == 550:
            if err.args[0].find('Permission denied') > 0:
                print('//Permition to makedir here is denied')
            elif err.args[0].find('already exists') > 0:
                dir = err.args[0].split(' ')[3]
                print('//Directory already exists')
            else:
                print(err.args[0])
        else:
            print(err.args[0])

def getcurrdir(ftp):
    try:
        rspsn = ftp.pwd()
        print('//Currently in dir ' + rspsn)
    except Exception as err:
        print(err)

def getshortlist(ftp):
    try:
        strngs = []
        rspns = ftp.nlst()
        strngs = rspns
        if len(strngs) == 0:
            print('//No files in this directory')
        else:
            for strng in strngs:
                print(strng)
    except Exception as err:
        print(err)

def getexit(ftp):
    try:
        rspns = ftp.quit().split(' ')[1]
        print('//Server response to quit attempt ' + rspns)
    except Exception as err:
        print(err)

def getdwnld(ftp, args):
    if len(args) < 2:
        print('//dwnld usage dwnld <file1> <place>')
    fls = args[:-1]
    outbs = args[-1]
    if outbs[-1] != '/' and outbs[-1] != '\\':
        outbs = outbs + '/'

    for fl in fls:
        out = outbs + fl.split('/')[-1]
        try:
            with open(out, 'wb') as f:
                ftp.retrbinary('RETR ' + fl, f.write)
            print('//File ' + fl.split('/')[-1] + ' succesfully downloaded and saved to ' + os.path.realpath(out))
        except Exception as err:
            code_err = int(str(err.args[0]).split(' ')[0])
            if code_err == 550:
                if err.args[0].find('Permission denied') > 0:
                    print('//Permission to download denied')
                elif err.args[0].find('not found') > 0:
                    print('///No file <' + fl + '> was found')
                elif err.args[0].find('Permission denied') >= 0:
                    print('//Permission denied to download in this directory')
                else:
                    print(err)
            elif code_err == 22:
                print('//Wrong path')
            elif code_err == 13:
                if err.args[1].find('Permission denied') >= 0:
                    print('//Denied permission to download')


def getdeletefile(ftp, args):
    if len(args) < 1:
        print('//deletefile usage is deletefile <file1>')
    fls = args
    for fl in fls:
        try:
            ftp.delete(fl)
            print('//Succesfully deleted file ' + fl)
        except Exception as err:
            code_err = int(str(err.args[0]).split(' ')[0])
            if code_err == 550:
                if err.args[0].find('Permission denied') > 0:
                    print('//Permission to delete denied')
                elif err.args[0].find('not found') > 0:
                    print('///No file <' + fl + '> was found')
                elif err.args[0].find('Permission denied') >= 0:
                    print('//Permission denied to access in this directory')
                else:
                    print(err)
            elif code_err == 22:
                print('//Wrong path')
            elif code_err == 13:
                if err.args[1].find('Permission denied') >= 0:
                    print('//Denied permission to delete')

def getremovedir(ftp, args):
    if len(args) == 0:
        print('//removedir usage is removedir <dir>')
    elif len(args) >1:
        print('//removedir usage is removedir <dir>')
    try:
        rspns = ftp.rmd(args[0])
        if rspns != "":
            print('//Succesfully removed directory')
    except Exception as err:
        code_err = int(str(err.args[0]).split(' ')[0])
        if code_err == 550:
            if err.args[0].find('Permission denied') > 0:
                print('//Can`t remove this dir')
            elif err.args[0].find('not found') > 0:
                dir = err.args[0].split(' ')[3]
                print('//No such directory found')
            elif err.args[0].find('not empty') > 0:
                dir = err.args[0].split(' ')[3]
                print('//Can only remove empty directory')
            else:
                print(err.args[0])
        else:
            print(err.args[0])

def getstorefile(ftp, args):
    if len(args) < 2:
        print('storefile usage storefile <file1> <where>')
        return 0
    fls = args[:-1]
    pathbase = args[-1]
    if pathbase[-1] != '/' and pathbase[-1] != '\\':
        pathbase = pathbase + '/'
    
    for fl in fls:
        path = pathbase + os.path.normpath(fl).split('\\')[-1]
        ftype = fl.split('.')[-1].upper()
        if not os.path.isfile(fl):
            print('//No such file')
            continue

        try:
            if ftype == 'TXT':
                with open(fl, 'rb') as fobj:
                    ftp.storlines('STOR ' + path, fobj)
            else:
                with open(fl, 'rb') as fobj:
                    ftp.storbinary('STOR ' + path, fobj, 1024)
            print('//File loaded')
        except Exception as err:
            code_err = int(str(err.args[0]).split(' ')[0])
            if code_err == 550:
                if err.args[0].find('Permission denied') > 0:
                    print('//No permission to load file here')
                elif err.args[0].find('Filename invalid') > 0:
                    print('//Wrong file on server')
                else:
                    print(err)
            else:
                print(err)

    msg = '//This is a help message. \n\
         //changedir <> -- change working directory \n\
             //deletefile <filename> -- delete file with name <filename> \n\
                  //gethelp -- this command, returns list of commands. \n\
                       //listdir -- lists contents of directory. \n\
                            //makedir -- creates new direfctory, \n\
                                 //shortlist -- return contents of directory (shorter). \n\
                                       //currdir -- current directory name \n\
                                            //exit -- stop connection \n\
                                                 //dwnld -- download file(s) dnwld <file1> <file2> <wheretosave> \n\
                                                      //removedir -- remove directory \n\
                                                           // storefile -- upload file(s) storefile <file1> <file2> <wheretosave> '
def commandproccesing(func, ftp):
    func_spl = func.split(' ')
    func_, args = func_spl[0], func_spl[1:]
    if func_ == 'changedir':
        getchangedir(ftp, args)
    elif func_ == 'deletefile':
        getdeletefile(ftp, args)
    elif func_ == 'gethelp':
        getHelp()
    elif func_ == 'listdir':
        getlistdir(ftp)
    elif func_ == 'makedir':
        getmakedir(ftp, args)
    elif func_ == 'shortlist':
        getshortlist(ftp)
    elif func_ ==  'currdir':
        getcurrdir(ftp)
    elif func_ == 'exit':
        getexit(ftp)
    elif func_ == 'dwnld':
        getdwnld(ftp, args)
    elif func_ == 'removedir':
        getremovedir(ftp, args)
    elif func_ == 'storefile':
        getstorefile(ftp, args)
    else:
        print('//No such function')
        getHelp()
    return 0

ftp = FTP()

ftp, log = auth(ftp)
print('///////////////////////////////////////////')
print('//Loaded')
print('//Your adress is ' + str(ftp.sock.getsockname()))
print('//You are logged as ' + log)
ftp.cwd('./')
print('//' + ftp.welcome)
print('//Hosted at ' + ftp.host)
print('///////////////////////////////////////////')

while True:
    func = str(input('>'))
    cd = commandproccesing(func, ftp)
    if cd < 0:
        break
    if func == 'close':
        break
    print('//New command?')

print('/////////////////////////////server shutdown/////////////////////////////////')

