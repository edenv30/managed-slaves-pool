import urllib.parse as urlparse
import logging, time

# initial slaves in list of dictionaries
def slaves_assign():
    slaves = []
    for i in range(101, 111):
        slaves.append(
            {
                "ip": "192.168.0." + str(i),
                "duration": 0,
            }
        )
    return slaves
#extract the path(get_slaves) and the params (amount & duration)
def parse_url(self):
    if self: # edge case
        url = self.path
        path = urlparse.urlparse(url).path
        params = urlparse.parse_qs(urlparse.urlparse(url).query)
        return path, params
    return
#check if have enough slaves available and return the available slaves
def available_slaves(amount, slaves):
    if 0 < amount <= 10 and len(slaves) > 0: # edge cases
        cnt = 0
        a_slaves = []
        for slave in slaves:
            if slave["duration"] == 0:
                cnt += 1
                a_slaves.append(slave["ip"])
            if cnt == amount and len(a_slaves)>0: # edge cases if len(a_slaves) > 0:
                return True, a_slaves
    return False, a_slaves
#assign slaves
def update_duration_slaves(slaves_dictionary, amount, duration):
    if check_variables(slaves_dictionary, amount, duration):
        slaves = []
        for slave in slaves_dictionary:
            if slave["duration"] == 0:
                slave["duration"] = duration
                # slave["unit-test"] = time.time() # unit test
                slaves.append(slave["ip"])
            if len(slaves) == amount: return slaves_dictionary, slaves
    return
#return the duration time that the client needs to come back again
def come_back(slaves_dictionary, amount, duration):
    if check_variables(slaves_dictionary, amount, duration):
        slaves = []
        my_list = sorted(slaves_dictionary, key=lambda k: k['duration'])
        for slave in my_list:
            if 0 < slave["duration"] <= duration:
                slaves.append(slave)
            if len(slaves) == amount:
                return slave["duration"]
    return
# send response to the client
def send_response_(self, status_code, content_type, msg):
    self.send_response(status_code)
    self.send_header('Content-Type', content_type)
    self.end_headers()
    self.wfile.write(bytes(msg, "utf8"))
# check cmd
def cmd_args(args_list):
    port = 8080
    len_args = len(args_list)
    if args_list:
        try:
            if len_args == 3:
                if args_list[1] == "--port" and args_list[2].isnumeric():
                    port = int(args_list[2])
            return port
        except Exception as e:
            logging.exception(e)
# edge cases - dictionary , amount , duration
def check_variables(slaves_dictionary, amount, duration):
    if len(slaves_dictionary) > 0 and 0 < amount <= 10 and duration >= 0:
        return True
    return False
# checking list if empty
def is_empty(list_check):
    return True if len(list_check) == 0 else False