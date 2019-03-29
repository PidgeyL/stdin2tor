import sys
import requests

if len(sys.argv) > 2:
    print("Usage: %s [tor proxy]"%sys.argv[0])

if len(sys.argv) == 2:
    proxy = sys.argv
    if not proxy.lower().startswith('socks5://'):
        proxy = 'socks5://' + proxy
else:
    proxy = 'socks5://localhost:9050'

for line in sys.stdin.readlines():
    line = line.strip()
    resp = requests.get('http://httpbin.org/ip', proxies={'http':proxy})
    if not resp:
        print(resp.content)
        sys.exit("Check settings")
    ip   = resp.content.decode().split('"')[3].split(',')[0]
    print('[%s] %s'%(ip, line))
