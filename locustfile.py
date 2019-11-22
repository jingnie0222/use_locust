from locust import HttpLocust, TaskSet, task
from locust.web import set_time_distribution

class UserBehavior(TaskSet):
    @task(1)
    def index(self):
        response = self.client.get("/gcov/")
        #print "Response status code:", response.status_code
        #print "Response content:", response.content

class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 500
    max_wait = 900
