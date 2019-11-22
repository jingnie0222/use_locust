import sys

import codecs
from locust import HttpLocust, TaskSet, task
from locust.web import set_time_distribution
from locust.xml_parse import parsexml

# The List of time intervial for response time distribution
TIME_DISTRIBUTION = [(0, 20), (20, 50), (50, 80), (80, 100), (100, 200),(200, 1000)]
set_time_distribution(TIME_DISTRIBUTION)

headers = {'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-16LE'}
#URL_source = "./tupu_resin_0919-small"
URL_source = "./tupu_resin_0919"
class UserBehavior(TaskSet):
    def on_start(self, client_id, num_clients):
        self.line_count = 0
        self.file = open(URL_source, "r")
        self.client_id = client_id
        self.num_clients = num_clients
        print("user %d, total count %d" % (client_id, num_clients))


    @task(1)
    def index(self):
        while True:
            line = self.file.readline()
            if not line:
                # Read URL_sources again
                self.file.close()
                self.line_count = 0
                self.file = open(URL_source, "r")
                line = self.file.readline()

            line = line.rstrip('\n')
            self.line_count += 1

            # Each client/user only use its own, not conflict with others
            if (self.line_count % self.num_clients == self.client_id % self.num_clients):
                break

        response = self.client.post("/", headers=headers, data=line)
        if response.status_code == 0:
            #print("Get Nothing: %s" % line)
            return
        elif response.content and response.encoding:
            content = response.content
            decoder = codecs.getdecoder(response.encoding)
            (content,length) = decoder(content)
            content = content.replace(u'\u0a0d', '')
            if response.status_code != 200:
                print "URL:", response.url
                print "Response status code:", response.status_code
                print "Response encoding:", response.encoding
                print "Response Content: %s" % content
            elif response.status_code == 200:
                #parsexml('post', line, content)
                pass

class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 30
    max_wait = 50


