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
import os
import csv
from datetime import datetime
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
ARCHIVO_PRODUCTOS = BASE_DIR / "productos.csv"



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
inventario_inicial = [
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
        return cargar_inventario_csv()

    except Exception as error:
        print("ERROR:", repr(error))
        raise HTTPException(status_code=500, detail=str(error))




#POST Agrega producto a mi inventario
@app.post("/productos", response_model=respuestaProducto, status_code=status.HTTP_201_CREATED)
def addProducto(producto: crearProducto):
    try:
        inventario = cargar_inventario_csv()
        nuevo_id = max((p["id"] for p in inventario), default=0) + 1
        nuevo_producto = {
            "id": nuevo_id,    
            "nombre": producto.nombre,
            "precio": producto.precio,
            "cantidad": producto.cantidad
        }

        inventario.append(nuevo_producto)
        guardar_inventario_csv(inventario)
        return nuevo_producto
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al agregar el producto: {str(error)}"
        )

    
#DELETE Borra producto de mi inventario
@app.delete("/productos/{producto_id}")
def delete_producto(producto_id: int):
    try:
        inventario = cargar_inventario_csv()
        inventario_actualizado = [p for p in inventario if p["id"] != producto_id]

        if len(inventario_actualizado) == len(inventario):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No fue encontrado el producto",
            )

        guardar_inventario_csv(inventario_actualizado)  # importante: persistir el cambio
        return {"Message": "El producto fue eliminado"}
    except HTTPException:
        raise
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar el producto: {str(error)}",
        )


#POST  comprar producto de inventario 

@app.post("/productos/{producto_id}")
async def comprar_producto(producto_id: int):
    try:
        async with lock:
            inventario = cargar_inventario_csv()

            producto_encontrado = next(
                (p for p in inventario if p["id"] == producto_id),
                None,
            )

            if producto_encontrado is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="No existe el ID de ese producto",
                )

            if producto_encontrado["cantidad"] <= 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="No hay stock de ese producto",
                )

            await asyncio.sleep(0.05)
            producto_encontrado["cantidad"] -= 1
            guardar_inventario_csv(inventario)
            registrar_venta_csv(
                producto_nombre=producto_encontrado["nombre"],
                precio=producto_encontrado["precio"],
                cantidad=1,
            )

            return {"Message": "Producto comprado"}

    except HTTPException:
        raise
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al comprar producto: {str(error)}",
        )


def cargar_inventario_csv():

    print("Buscando archivo:", ARCHIVO_PRODUCTOS)
    print("¿Existe?:", ARCHIVO_PRODUCTOS.exists())

    productos = []

    with open(ARCHIVO_PRODUCTOS, mode="r",
              encoding="utf-8-sig", newline="") as f:

        reader = csv.DictReader(f)

        print("Columnas encontradas:", reader.fieldnames)

        for row in reader:
            productos.append({
                "id": int(row["id"]),
                "nombre": row["nombre"],
                "precio": float(row["precio"]),
                "cantidad": int(row["cantidad"])
            })

    print("Total productos:", len(productos))

    return productos


def guardar_inventario_csv(productos):
    with open("productos.csv", mode="w", newline="", encoding="utf-8") as f:
        fieldnames = ["id", "nombre", "precio", "cantidad"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(productos)


def registrar_venta_csv(producto_nombre: str, precio: float, cantidad: int = 0):
    file_exists = os.path.isfile("ventas.csv")

    with open("ventas.csv", mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow(["id_venta", "fecha", "producto", "precio", "cantidad", "monto_total"])
            nuevo_id = 1
        else:
            with open("ventas.csv", "r", encoding="utf-8") as f:
                nuevo_id = sum(1 for line in f)

        fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        monto_total = precio * cantidad
        writer.writerow([nuevo_id, fecha_actual, producto_nombre, precio, cantidad, monto_total])