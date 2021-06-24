import urllib3
import time
import json
import os
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, HTTPServer
from multiprocessing import Process


AVERAGE_INTERVAL = 10
HOST_NAME = ""
SERVER_PORT = 8080
READY_PERIOD = 10
READY_FILENAME = "/var/bitcoin/ready"


def print_bitcoin_rate():
    while True:
        total = 0
        for i in range(AVERAGE_INTERVAL):
            data = urllib3.PoolManager().request("GET", "https://api.coindesk.com/v1/bpi/currentprice.json").data
            current_rate = json.loads(data)['bpi']['USD']['rate_float']
            print("Current rate: %.2f" % current_rate)
            total += current_rate
            time.sleep(60)
        print("Average rate of last %d minutes: %.2f" % (AVERAGE_INTERVAL, total/AVERAGE_INTERVAL))


def change_to_ready():
    os.mkdir(os.path.dirname(READY_FILENAME))
    time.sleep(READY_PERIOD)
    open(READY_FILENAME, "w")
    print("Service is ready")


class MyServer(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == "/healthz":
            self.send_response(HTTPStatus.OK)
        elif self.path == "/ready":
            if os.path.exists(READY_FILENAME):
                self.send_response(HTTPStatus.OK)
            else:
                self.send_response(HTTPStatus.CONFLICT)
        else:
            self.send_response(HTTPStatus.NOT_FOUND)
        # self.send_header("Content-type", "text/plain")
        self.end_headers()


def main():
    Process(target=print_bitcoin_rate).start()
    Process(target=change_to_ready).start()

    webServer = HTTPServer((HOST_NAME, SERVER_PORT), MyServer)
    print("Server started http://%s:%s" % (HOST_NAME, SERVER_PORT))
    webServer.serve_forever()


if __name__ == "__main__":
    main()
