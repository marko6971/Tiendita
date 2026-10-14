
import asyncio
import httpx
import time

URL = "http://127.0.0.1:8001/http"


async def enviar_peticion(cliente, numero):
    inicio = time.perf_counter()

    respuesta = await cliente.get(URL)

    duracion = time.perf_counter() - inicio

    print(
        f"Petición {numero}: "
        f"HTTP {respuesta.status_code} | "
        f"{duracion:.3f} segundos | "
        f"{respuesta.text}"
    )

    return respuesta.status_code


async def main():
    async with httpx.AsyncClient() as cliente:

        print("Enviando 10 peticiones simultáneas...\n")

        resultados = await asyncio.gather(
            *[
                enviar_peticion(cliente, i)
                for i in range(1, 11)
            ]
        )

        print("\n--- RESUMEN ---")
        print("Aceptadas (2xx):", sum(200 <= c < 300 for c in resultados))
        print("Rechazadas (429):", resultados.count(429))


asyncio.run(main())
