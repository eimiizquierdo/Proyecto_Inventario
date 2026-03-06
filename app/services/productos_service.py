from uuid import UUID
from datetime import date, timezone
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from app.core.supabase_client import get_supabase
from app.core.config import config
from postgrest import CountMethod

def _table():
    sb = get_supabase()
    return sb.schema(config.supabase_schema).table(config.supabase_table)

def list_products(limit: int = 100, offset: int = 0):
    try:
        res = _table().select("*", count=CountMethod.exact).range(offset, offset + limit-1).execute()
        return {"items": res.data if res.data else [], "Total": res.count or 0}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al mostrar los registros:: {e}")

def get_products(product_id: UUID):
    try:
        res = _table().select("*").eq("id", str(product_id)).execute()
        #Encontrar con un limite
        #res = _table().select("*").eq("id", str(product_id)).execute()
        if not res.data:
            raise HTTPException(status_code=404, detail=f"Error al encontrar el registro con el id {product_id}")
        return {"item": res.data[0]}
    except Exception as e:
        raise HTTPException(status_code = 500, detail = f"Error al mostrar los registros: {e}")

def create_product(datos:dict):
    try:
        datos = jsonable_encoder(datos)
        print(datos)
        res = _table().insert(datos).execute()
        return {"item" : res.data[0] if res.data else None}
    except Exception as e:
        raise HTTPException(status_code = 500, detail = f"Error al insertar el nuevo registro: {e}")

def update_product(product_id: UUID, datos: dict):
    try:
        if not datos or not product_id:
            raise HTTPException(status_code = 400, detail = "Error, datos incompletos")
        datos = jsonable_encoder(datos)
        res = _table().update(datos).eq("id", str(product_id)).execute()
        return {"item": res.data[0] if res.data else None}
    except Exception as e:
        raise HTTPException(status_code = 500, detail = f"Error al modificar el registro: {e}")

def delete_product(product_id: UUID):
    try:
        if not product_id:
            raise HTTPException(status_code = 404, detail = "Error, datos incompletos")
        res = _table().delete().eq("id", str(product_id)).execute()
        return {"item": res.data[0] if res.data else None}
    except Exception as e:
        raise HTTPException(status_code = 500, detail = f"Error al eliminar el registro: {e}")

