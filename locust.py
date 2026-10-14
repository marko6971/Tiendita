

URL = "http://127.0.0.1:8001/http"


from locust import HttpUser, task, between


class UsuarioTiendita(HttpUser):

    # Tiempo de espera entre tareas de cada usuario
    wait_time = between(0.2, 1)

    @task
    def probar_endpoint(self):
        self.client.get(
            "/http",
            name="/http"
        )
