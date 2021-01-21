from http.server import BaseHTTPRequestHandler, HTTPServer
from functions import slaves_assign, parse_url, available_slaves, update_duration_slaves, come_back, send_response_, cmd_args
import time, json, threading, sys, math

slaves_dictionary = slaves_assign()
callback_collection = []
# run from begin program
def lifecycle():
    global slaves_dictionary
    while True:
        time.sleep(1.5)
        for slave in slaves_dictionary:
            if slave["duration"] != 0:
                # sub = math.floor(time.time() - slave["unit-test"])
                # print(slave["ip"], sub)
                slave["duration"] -= 1

t = threading.Thread(target=lifecycle)
t.start()

class MyHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        global slaves_dictionary
        try:
            (path, params) = parse_url(self)
            if path == '/get_slaves':
                amount = int(params['amount'][0])
                duration = int(params['duration'][0])
                if amount > 10:
                    msg = '[!] Error: You must insert amount less or equal to 10\n'
                    print(msg)
                    send_response_(self, 400, 'text/plain', msg)
                available, slaves = available_slaves(amount, slaves_dictionary)
                if not available:
                    new_amount = amount - len(slaves)
                    slaves_come_back = come_back(slaves_dictionary, new_amount, duration)
                    if slaves_come_back is None:
                        msg = '[!] Error'
                        print(msg)
                        send_response_(self, 400, 'text/plain', msg)
                    else:
                        msg = json.dumps({"slaves": [], "come_back": slaves_come_back })
                        send_response_(self, 200, 'application/json', msg)
                    return
                else:
                    slaves_dictionary, slaves = update_duration_slaves(slaves_dictionary, amount, duration)
                    msg = json.dumps({"slaves": slaves})
                    send_response_(self, 200, 'application/json', msg)
                    return
        except Exception as error:
            msg = '[!] Error: {0}\n You must check your request'.format(error)
            print(msg)
            send_response_(self, 400, 'text/plain', msg)

if __name__ == '__main__':
    args_list = sys.argv
    port = cmd_args(args_list)
    print('starting server on port {0}...'.format(port))

    server_address = ('localhost', port)
    httpd = HTTPServer(server_address, MyHandler)

    httpd.serve_forever()