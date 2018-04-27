import time


def get_timestamp():
    return int(round(time.time() * 1000))


def runtest():
    start = time.time()

    with open('logs/battery-test-' + str(get_timestamp()), 'a') as logfile:
        while True:
            logfile.write(str(get_timestamp()))
            logfile.write("\n")
            logfile.flush()
            time.sleep(5)



if __name__ == "__main__":
    runtest()
