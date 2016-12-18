import sys

import codecs
from locust import HttpLocust, TaskSet, task, events

headers = {'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-16LE'}
URL_source = "./tupu_resin_0919-small"
class UserBehavior(TaskSet):
    def on_start(self, client_id, num_clients):
        self.file = open(URL_source, "r")
        print("user %d, total count %d" % (client_id, num_clients))

    @task(1)
    def index(self):
        line = self.file.readline()
        if line:
            line = line.rstrip('\n')
        else:
            self.file.close()
            self.file = open(URL_source, "r")
            line = self.file.readline()
            line = line.rstrip('\n')

        response = self.client.post("/", headers=headers, data=line)
        if response.status_code != 200:
            print "Response status code:", response.status_code
            content = response.content
            decoder = codecs.getdecoder(response.encoding)
            (content,length) = decoder(content)
            content = content.replace(u'\u0a0d', '')
            #open("test.log", "w").write(content.encode("gbk"))
            #print "Response Content: %s" % content

class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 10
    max_wait = 20


