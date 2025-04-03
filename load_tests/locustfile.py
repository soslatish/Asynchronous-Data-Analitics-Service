from locust import HttpUser, task, between
import random
import json

class DeviceUser(HttpUser):
    wait_time = between(1, 3)
    
    def on_start(self):
        # Create a test device
        response = self.client.post(
            "/api/devices/",
            json={"name": f"Test Device {random.randint(1, 1000)}"}
        )
        self.device_id = response.json()["id"]
        
        # Create a test user (optional)
        response = self.client.post(
            "/api/users/",
            json={
                "username": f"testuser_{random.randint(1, 10000)}",
                "email": f"user{random.randint(1, 10000)}@example.com"
            }
        )
        self.user_id = response.json()["id"]

    @task(10)
    def add_device_data(self):
        data = {
            "x": random.uniform(-100, 100),
            "y": random.uniform(-100, 100),
            "z": random.uniform(-100, 100)
        }
        self.client.post(f"/api/devices/{self.device_id}/data", json=data)
    
    @task(2)
    def get_device_analytics(self):
        self.client.get(f"/api/analytics/devices/{self.device_id}")
    
    @task(1)
    def get_user_analytics(self):
        self.client.get(f"/api/analytics/users/{self.user_id}")