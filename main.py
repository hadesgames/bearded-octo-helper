
#--------------------
# do this once at program startup
#--------------------
import socket
origGetAddrInfo = socket.getaddrinfo

def getAddrInfoWrapper(host, port, family=0, socktype=0, proto=0, flags=0):
    return origGetAddrInfo(host, port, socket.AF_INET, socktype, proto, flags)

# replace the original socket.getaddrinfo by our version
socket.getaddrinfo = getAddrInfoWrapper

import recorder
import processor


def main():
    rec = recorder.Recorder()
    processorThread = processor.run(rec)

    rec.start()
    rec.record(3)
    rec.stop()


if __name__ == "__main__":
    main()
