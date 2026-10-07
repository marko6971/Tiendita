from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()


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

@app.get("/")
def home():
    return {"Message": "Hola bienvenido"}

@app.get("/productos")
def getProductos():
    return inventario

@app.post("/productos")
def addProducto(producto: dict):

    nuevo_id = len(inventario) + 1
    nuevo_producto = {
        "id": nuevo_id,    
        "nombre": producto["nombre"],
        "precio": producto["precio"],
        "cantidad": producto["cantidad"]
    }

    inventario.append(nuevo_producto)

    return inventario

@app.delete("/productos/{producto_id}")
def deleteProducto(producto_id: int):
    for producto in inventario:
        if producto["id"] == producto_id:
            inventario.remove(producto)
            return {"Message": "El producto fue eliminado"}
    return {"Message": "No fue encontrado el producto"}


