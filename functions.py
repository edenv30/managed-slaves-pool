import urllib.parse as urlparse

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
    url = self.path
    path = urlparse.urlparse(url).path
    params = urlparse.parse_qs(urlparse.urlparse(url).query)
    return path, params
#check if have enough slaves available and return the availables slaves
def available_slaves(amount, slaves):
    cnt = 0
    a_slaves = []
    for slave in slaves:
        if slave["duration"] == 0:
            cnt += 1
            a_slaves.append(slave["ip"])
        if cnt == amount:
            return True, a_slaves
    return False, []
#assign slaves
def update_duration_slaves(slaves_dictionary, duration, amount):
    slaves = []
    for slave in slaves_dictionary:
        if slave["duration"] == 0:
            slave["duration"] = duration
            slaves.append(slave["ip"])
        if len(slaves) == amount: return slaves_dictionary, slaves
#retuan the duration time that the client needs to come back again
def come_back(slaves_dictionary, amount, duration):
    slaves = []
    my_list = sorted(slaves_dictionary, key=lambda k: k['duration'])

    for slave in my_list:
        if slave["duration"] <= duration and slave["duration"] != 0:
            slaves.append(slave)
        if len(slaves) == amount:
            break
#   check if slaves empty
    return slaves[amount-1]['duration']