#Mi tiendita
#autor: Marco Preciado
#Fecha: 05/oct/2026
#una api para mostrar via html productos de tiendita podemos borrar agregar consultar

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from pydantic import BaseModel, Field
from typing import List
from collections import deque
import time

app = FastAPI(title="API Proyecto Tiendita", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

#Inicializamos variable lock (Condición de carrera)
lock = asyncio.Lock()


#Modelos de Pydantic
#Pedir al cliente que su petición debe estructurarse de esta manera.
class crearProducto(BaseModel):
    nombre: str = Field(..., min_length=1, description="Nombre del producto")
    precio: float = Field(..., gt=0, description="Precio del producto")
    cantidad: int = Field(..., ge=0, description="stock del producto")


#La salida de datos de la API debe de estructurarse de esta manera.
class respuestaProducto(BaseModel):
    id: int
    nombre: str
    precio: float
    cantidad: int


#Datos cargados (Simulación)
inventario = [
    {"id": 1, "nombre": "iPhone 15", "precio": 14999, "cantidad": 87},
    {"id": 2, "nombre": "Samsung Galaxy S24", "precio": 16999, "cantidad": 142},
    {"id": 3, "nombre": "Xiaomi Redmi Note 13", "precio": 4999, "cantidad": 56},
    {"id": 4, "nombre": "Motorola Edge 50", "precio": 8999, "cantidad": 173},
    {"id": 5, "nombre": "Google Pixel 8", "precio": 11999, "cantidad": 34},
    {"id": 6, "nombre": "OnePlus 12", "precio": 13999, "cantidad": 91},
    {"id": 7, "nombre": "Huawei Nova 12", "precio": 7999, "cantidad": 128},
    {"id": 8, "nombre": "Honor 200", "precio": 9499, "cantidad": 67},
    {"id": 9, "nombre": "OPPO Reno 12", "precio": 8499, "cantidad": 195},
    {"id": 10, "nombre": "Realme 12 Pro", "precio": 6999, "cantidad": 43},
    {"id": 11, "nombre": "Sony Xperia 10 VI", "precio": 10999, "cantidad": 116}
]


#Prueba asyncio 5 segundos
@app.get("/prueba-asyncio")
async def pruebaAsyncio():
    try:
        print("empiezan los 5 segundos")
        await asyncio.sleep(5)
        print("Se acaba de terminar los 5 segundos")
        return {"Message": "Respuesta después de 5 segundos"}
    except Exception as error:
        print(f"Hubo un error: {error}")

#Prueba asyncio 3 segundos
@app.get("/prueba-asyncio-3segundos")
async def pruebaAsyncio():
    print("empiezan los 3 segundos")
    await asyncio.sleep(3)
    print("Se acaba de terminar los 3 segundos")
    return {"Message": "Respuesta después de 3 segundos"}

#Prueba asyncio 1 segundos
@app.get("/prueba-asyncio-1segundo")
async def pruebaAsyncio():
    print("empiezan los 1 segundos")
    await asyncio.sleep(1)
    print("Se acaba de terminar los 1 segundos")
    return {"Message": "Respuesta después de 1 segundos"}


#Ejemplo de API - GET para obtener mensaje inicial
@app.get("/")
def home():
    try:
        print("hola1") 
        resultado = "1"  +  1,
        print("hola2")
        return {"Message": "Hola bienvenido"}
    except Exception as error:
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al hacer la operación: {str(error)}"
        )
       
   


#GET Obtiene lista de productos de mi inventario
@app.get("/productos")
def getProductos():
    try:
        return inventario
    except Exception as error:
        return  {str(error)} 

#POST Agrega producto a mi inventario
@app.post("/productos", response_model=respuestaProducto, status_code=status.HTTP_201_CREATED)
def addProducto(producto: crearProducto):
    try:

        nuevo_id = max((p["id"] for p in inventario), default=0) + 1
        nuevo_producto = {
            "id": nuevo_id,    
            "nombre": producto.nombre,
            "precio": producto.precio,
            "cantidad": producto.cantidad
        }

        inventario.append(nuevo_producto)

        return nuevo_producto
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al agregar el producto: {str(error)}"
        )

    
#DELETE Borra producto de mi inventario
@app.delete("/productos/{producto_id}")
def deleteProducto(producto_id: int):
    try:
        for producto in inventario:
            if producto["id"] == producto_id:
                inventario.remove(producto) #Elimina el producto del inventario ya que encontró el id correspondiente
                return {"Message": "El producto fue eliminado"}
        return {"Message": "No fue encontrado el producto"}
    except HTTPException as errorHTTP:
        return {str(errorHTTP)}

    except Exception as error:
        return  {str(error)} 


@app.post("/productos/{producto_id}")
async def comprarProducto(producto_id: int):
    try:
        async with lock:
            for objeto in inventario:
                if objeto["id"] == producto_id:
                    if objeto["cantidad"] > 0:
                        await asyncio.sleep(0.05)
                        objeto["cantidad"] = objeto["cantidad"]-1
                        return {"Mensaje":"Producto comprado"}
                    else:
                        raise HTTPException(
                            status_code = status.HTTP_400_BAD_REQUEST,
                            detail = "No hay stock de ese producto"
                        )

            raise HTTPException(
                status_code = status.HTTP_400_BAD_REQUEST,
                detail = "No existe el ID de ese producto"
            )

    except Exception as error:
        raise HTTPException (
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = f"Error al comprar producto: {str(error)}"
        )