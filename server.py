from http.server import BaseHTTPRequestHandler, HTTPServer
from functions import slaves_assign, parse_url, available_slaves, update_duration_slaves, come_back
import time, json, threading, sys

slaves_dictionary = slaves_assign()
callback_collection = []
# run from begin program
def lifecycle():
    global slaves_dictionary
    while True:
        time.sleep(1)
        for slave in slaves_dictionary:
            if slave["duration"] != 0:
                slave["duration"] -= 1

t = threading.Thread(target=lifecycle)
t.start()

class MyHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        global slaves_dictionary
        (path, params) = parse_url(self)
        if path == '/get_slaves':
            try:
                amount = int(params['amount'][0])
                duration = int(params['duration'][0])
                if amount > 10:
                    msg = '[!] Error: You must insert amount less or equal to 10\n'
                    print(msg)
                    self.send_response(400)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(bytes(msg, "utf8"))
                available, slaves = available_slaves(amount, slaves_dictionary)

                if not available:
    #               count duration
                    new_amount = amount - len(slaves)
                    slaves_come_back = come_back(slaves_dictionary, new_amount, duration)
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(bytes(json.dumps({"slaves": slaves, "come_back": slaves_come_back }), "utf8"))
                    return
                else:
                    slaves_dictionary, slaves = update_duration_slaves(slaves_dictionary, duration, amount)
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(bytes(json.dumps({"slaves": slaves}), "utf8"))
                    return
            except Exception as error:
                msg = '[!] Error: {0}\n You must check your request'.format(error)
                print(msg)
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(bytes(msg, "utf8"))

if __name__ == '__main__':
    port = 8080
    args_list = sys.argv
    if args_list:
        try:
            port = int(args_list[2])
        except:
            print('[!] Incorrect command, we use an default port')
            print('[!] Error: Example run command: python server.py --port 8080')
    print('starting server on port {0}...'.format(port))

    server_address = ('localhost', port)
    httpd = HTTPServer(server_address, MyHandler)

    httpd.serve_forever()