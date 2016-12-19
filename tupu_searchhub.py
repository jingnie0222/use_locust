import sys

from urllib import unquote
import codecs
from locust import HttpLocust, TaskSet, task

URL_source = "./tupu_nginx_0919"

class UserBehavior(TaskSet):
    def on_start(self, client_id, num_clients):
        self.line_count = 0
        self.file = open(URL_source, "r")
        self.client_id = client_id
        self.num_clients = num_clients
        print("user %d, total count %d" % (client_id, num_clients))

    @task(1)
    def get(self):
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

        response = self.client.get(url = '/', name = "tupu_searchhub", params = line, timeout = 0.1)
        #response = self.client.get('/', name = "tupu_searchhub", params = line, stream=True)
        if response.status_code == 0:
            #print("Get Nothing: %s" % line)
            return
        elif response.status_code == 200:
            #content = response.content
            pass
        elif response.status_code != 200:
            print "URL:", response.url
            print "Response status code:", response.status_code
            print "Response encoding:", response.encoding
            if response.content and response.encoding:
                content = response.content
                decoder = codecs.getdecoder(response.encoding)
                (content,length) = decoder(content)
                content = content.replace(u'\u0a0d', '')
                #open("test.log", "w").write(content.encode("gbk"))
                print "Response Content: %s" % content

class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 10
    max_wait = 20


