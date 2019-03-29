
import stem
import stem.control
import subprocess
import sys
import time

def renew_ip(port = 9051, passwd = None):
    passwd = passwd or 'password'
    with stem.control.Controller.from_port(port = port) as control:
        control.authenticate(password = passwd)
        control.signal(stem.Signal.NEWNYM)
    time.sleep(5)


def chunks(data, n):
    for i in range(0, len(data), n):
        yield data[i:i+n]


if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser(description="Break stdin into chunks and change the TOR route before executing each chunk")
    ap.add_argument('cmd', type=str, help='Command to run, between quotes')
    ap.add_argument('-p',  type=str, help='Password to authenticate to TOR control port')
    ap.add_argument('-c',  type=str, help='Control server:port')
    ap.add_argument('-n',  type=int, help='Chunks of stdin before IP change')
    args = ap.parse_args()

    try:
        pwd          = args.p or 'password'
        control      = args.c or 'localhost:9051'
        server, port = control.split(':')
        port         = int(port)
        chunk_size   = args.n or 1
    except:
        sys.exit("Invalid arguments")


    for lines in chunks(sys.stdin.readlines(), chunk_size):
        renew_ip()
        process = subprocess.Popen(args.cmd.split(), stdin =subprocess.PIPE,
                                                stdout=subprocess.PIPE,
                                                stderr=subprocess.PIPE)
        data = ''.join(lines)
        output, error = process.communicate(input=data.encode())
        if error:
            sys.exit(error.decode())
        if output.endswith(b'\n'):
            output = output[:-1]
        print(output.decode())

