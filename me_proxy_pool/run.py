from me_proxy_pool.proxypool.scheduler import *
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def main():
    try:
        s = Scheduler()
        s.run()
    except:
        main()

if __name__ == '__main__':
    main()
