import sys, logging, os.path, subprocess, time, getopt
from random import randint, choice
from datetime import datetime
from colorama import Fore, Style
from operator import add, sub, mul, truediv

def played(x=0):
    fname = logpath + datetime.now().strftime("%Y%m%d")
    if (x == 0):
        if os.path.isfile(fname):
            f=open(fname)
            p=f.read()
            f.close()
            try :
                return int(p)
            except ValueError:
                return 0
        else:
            return 0
    else:
        f=open(fname, "w")
        f.write(str(x))
        f.close()

def check_op(ans, z, msg):
    try :
        if float(ans) == z :
            log.debug(msg + ans)
            return 1
        else:
            log.info(Fore.RED + msg + f"{ans} is wrong" + Style.RESET_ALL)
            return 0
    except ValueError:
        log.info(Fore.RED + msg + f"{ans} is wrong, don't be naughty" + Style.RESET_ALL)
        return 0

def question_op(n, qtype=0):
    if qtype == 0:
        ops, opt = (add, sub), ('+', '-')
        op = choice(ops)
        i = ops.index(op)
        if uat: x, y = randint(1, 5), randint(1, 5)
        else: x, y = randint(9, 49), randint(9, 49)
        if x < y: x,y = y,x
        z = op(x, y)
        msg = f"Question {n}: {x} {opt[i]} {y} = "
        while True:
            ans = input(msg)
            if check_op(ans, z, msg) == 1: break
    else:
        ops, opt = (mul, truediv), ('*', '/')
        op = choice(ops)
        i = ops.index(op)
        if uat: x, y = randint(1, 5), randint(1, 5)
        else: x, y = randint(9, 49), randint(9, 49)
        z = round(op(x, y), 2)
        msg = f"Question {n}: {x} {opt[i]} {y} = "
        while True:
            ans = input(msg)
            if check_op(ans, z, msg) == 1: break

def play(T):
    cmd="/opt/retropie/supplementary/emulationstation/emulationstation.sh &"
    subprocess.run(cmd, shell=True, check=True, executable='/bin/bash')
    time.sleep(T * 60)
    killcmd="pgrep retro |xargs kill"
    try :
        subprocess.run(killcmd, shell=True, check=True, executable='/bin/bash')
    except subprocess.CalledProcessError:
        pass
    time.sleep(2)
    killcmd="pgrep emulat |xargs kill"
    try :
        subprocess.run(killcmd, shell=True, check=True, executable='/bin/bash')
    except subprocess.CalledProcessError:
        pass

# Main
def main():
    global uat, logpath, log
    uat = False
    logpath = '/tmp/'
    self = os.path.basename(__file__)
    usage = 'Usage: ' + self + ' m=<uat> l=<logpath>'
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hm:l:",["help", "mode=", "logpath="])
    except getopt.GetoptError as err:
        print(err)
        print(usage)
        sys.exit(1)
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print(usage)
            sys.exit(1)
        elif opt in ('-m', '--mode'):
            if arg == 'uat': uat = True
        elif opt in ('-l', '--logpath'):
            if (os.path.exists(arg)): logpath=arg
            else: print(f"path {arg} not found, use default path /tmp/")

    # logging with both file and stdout
    log = logging.getLogger(__name__)
    log.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(message)s')

    fh = logging.FileHandler(logpath + self + '.log')
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    log.addHandler(fh)

    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)
    ch.setFormatter(formatter)
    log.addHandler(ch)

    Q=5 if uat else 15
    X = played() + 1
    Q = Q * (X)
    log.debug( "===== " + datetime.now().strftime("%Y%m%d %H:%M:%S") + " ===== play " + str(X))
    log.info(f"You may play for 25 min, if both Lian & Luca answer {Q} questions correctly")
    log.info(f"{Q} Add & Sub questions for Lian:")
    for i in range(Q, 0, -1): question_op(i)
    log.info(f"{Q} Multi & Div questions for Luca (Round to 2 decimals where applicable):")
    for i in range(Q, 0, -1): question_op(i, 1)

    log.info("Well done, enjoy the game.")
    if not uat:
        play(25)
        played(X)
        log.info(datetime.now().strftime("%Y%m%d %H:%M:%S") + " - Game time is up")

# close logger
    lh = list(log.handlers)
    for i in lh:
        log.removeHandler(i)
        i.flush()
        i.close()

if __name__ == "__main__":
    main()

