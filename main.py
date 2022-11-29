import PluggedIrc
import sys

if __name__ == '__main__':
    server = PluggedIrc.Server()
    server.Forever()
    