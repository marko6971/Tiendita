#Mi tiendita
#autor: Marco Preciado
#Fecha: 05/oct/2026
#una api para mostrar via html productos de tiendita podemos borrar agregar consultar


from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from pydantic import BaseModel, Field
from typing import List

app = FastAPI(title="Api Proyecto Tiendita", version="1.0.0")


#prueba 10 sec
@app.get("/prueba-asyncio10")
async def consultar_bd():
    #cede el conttrol al event loop
    await asyncio.sleep(10)
    print("prueba")
    return {"status":"ok"}
    
#prueba 5 sec
@app.get("/prueba-asyncio5")
async def consultar_bd():
    #cede el conttrol al event loop
    await asyncio.sleep(5)
    print("prueba")
    return {"status":"ok"}
    
#prueba 3 sec
@app.get("/prueba-asyncio3")
async def consultar_bd():
    #cede el conttrol al event loop
    await asyncio.sleep(3)
    print("prueba")
    return {"status":"ok"}
    
#prueba 1 sec
@app.get("/prueba-asyncio1")
async def consultar_bd():
    #cede el conttrol al event loop
    await asyncio.sleep(1)
    print("prueba")
    return {"status":"ok"}
    

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


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

#Modelos Pydantic Pedir al cliente que su peticion debe tener esta estructura

class crearProducto(BaseModel):
    nombre: str = Field(..., min_length=1, description="nombre de producto")
    precio: float = Field(..., gt=0, description="Precio del producto")
    cantidad: int = Field(..., ge=0, description="Stock del producto")

#Modelo Pydantic  Salida Api con esta estructura

class respuestaProducto(BaseModel):
    id: int
    nombre: str
    precio: float
    cantidad: int



@app.get("/")
def home():
    return {"Message": "Hola bienvenido"}

@app.get("/productos")
def getProductos():
    return inventario

@app.post("/productos", response_model=List[crearProducto], status_code=status.HTTP_201_CREATED)
def addProducto(producto: crearProducto):
    try:

        nuevo_id = len(inventario) + 1
        nuevo_producto = {
            "id": nuevo_id,    
            "nombre": producto.nombre,
            "precio": producto.precio,
            "cantidad": producto.cantidad
        }

        inventario.append(nuevo_producto)

        return inventario
    
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"ocurrio un error:{str(error)}")

#DELETE borra productos del inventario 

@app.delete("/productos/{producto_id}")
def deleteProducto(producto_id: int):
    try:
        for producto in inventario:
            if producto["id"] == producto_id:
                inventario.remove(producto)
                return {"Message": "El producto fue eliminado"}
        return {"Message": "No fue encontrado el producto"}
    except HTTPException as errorHTTP:
        return{str(errorHTTP)}
    except Exception as error:
        return {str(error)}
