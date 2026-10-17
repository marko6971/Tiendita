

URL = "http://127.0.0.1:8001/http"


from locust import HttpUser, task, between
import random


class CompradorRelampago(HttpUser):
    # Tiempo de espera entre tareas de cada usuario
    wait_time = between(0.1, 0.3)

    @task
    def comprarProducto(self):
        payload = {
            "producto_id"= 3
        }

        self.client.post("/productos/3", json=payload)
