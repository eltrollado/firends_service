import random
import time
from locust import HttpUser, task, between


class QuickstartUser(HttpUser):
    wait_time = between(1, 10)

    @task(10)
    def get_friends(self):
        id = random.randint(1, 10**7)
        self.client.get(f'/users/{id}/friends')
        self.wait()
        self.client.get(f'/users/{id}/friends')
        self.wait()
        self.client.get(f'/users/{id}/friends')

    @task
    def add_friend(self):
        user_id = random.randint(1, 10 ** 7)
        friend_id = random.randint(1, 10 ** 7)
        self.client.post(f'/users/{user_id}/friends/{friend_id}')


