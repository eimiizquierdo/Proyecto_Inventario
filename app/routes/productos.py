from fastapi import APIRouter, Path, Query
from uuid import UUID
from app.services.productos_service import list_products, get_products, create_product, update_product, delete_product
from app.models.producto import OneProduct, ProductCreate, ProductUpdate, ProductOut, ProductList

router = APIRouter(prefix="/products")

# http:localhost:8000/products?limit=20&offset=0
# http:localhost:8000/products?limit=-20&offset=-10
# http:localhost:8000/products?limit=abc&offset=abc
# Limit - Número de registros a mostrar
# Offset - En qué reistro empezar a mostrar los resultados


@router.get("/", response_model = ProductList, name = "listar_productos")
def listar_productos(limit: int = Query(100, ge=1, le=200), offset: int = Query(0, ge=0)):
    return list_products(limit=limit, offset=offset)

@router.get("/{product_id}", response_model=OneProduct, name = "Obtener un producto por ID")

def api_get_product(product_id: UUID = Path(...)):
    return get_products(product_id)


@router.post("/", response_model = OneProduct, name = "crear_producto")

def api_create_product(body: ProductCreate):
    #print(body)
    return create_product(body.model_dump())


@router.put("/{product_id}", response_model = OneProduct, name = "actualizar_producto")

def api_update_product(product_id: UUID, body: ProductUpdate):
    return update_product(product_id, body.model_dump(exclude_none = True))


@router.delete("/{product_id}", name = "eliminar_producto")

def api_delete_product(product_id: UUID):
    return delete_product(product_id)