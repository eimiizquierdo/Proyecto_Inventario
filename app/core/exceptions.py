from fastapi import Request # Entrega el URL
from fastapi.exceptions import RequestValidationError # Entrega el mensaje de error
from fastapi.responses import JSONResponse # Preparar la respuesta

MNESAJES_ERROR = {

    # Crea las validadciones en exceptions.py para considerar cuando manden como 
    # parámetros números negativos o textos en lugar de números

    "listar_productos":{
        "Limit":{
            "less_than_equal":"El límite debe ser menor o igual a 200",
            "greater_than_equal":"El límite debe ser mayor o igual a 0",
            "int_parsing":"El límite debe ser un número"
        },
        "Offset":{
            "greater_than_equal":"Offset debe ser mayor o igual a 0",
            "int_parsing":"Offset debe ser un número"
        }
    },

    "crear_producto":{
        "name":{
            "missing":"El campo name es requerido",
        },
        "quantity":{
            "missing":"El campo quantity es requerido",
            "int_parsing":"El campo quantity debe ser un número"
        },
        "ingreso_date":{
            "missing":"El campo ingreso_date es requerido",
        },
        "min_stock":{
            "greater_than_equal":"El stock mínimo debe ser mayor o igual a 0",
            "int_parsing":"El campo min_stock debe ser un número",
            "missing":"El campo min_stock es requerido",
        },
        "max_stock":{
            "greater_than_equal":"El stock máximo debe ser mayor o igual a 0",
            "less_than_equal":"El stock máximo debe ser menor o igual a 1000",
            "int_parsing":"El campo max_stock debe ser un número",
            "missing":"El campo max_stock es requerido",
        }
    },

    "obtener_producto":{
        "product_id":{
            "uuid_parsing":"El ID no es de tipo UUID",
            "missing":"El campo product_id es requerido",
        }
    },

    "actualizar_producto":{
        "product_id":{
            "uuid_parsing":"El ID no es de tipo UUID",
            "missing":"El campo product_id es requerido",
        }
    },

    "eliminar_producto":{
        "product_id":{
            "uuid_parsing":"El ID no es de tipo UUID",
            "missing":"El campo Id del Producto es requerido",
        }
    }   
}

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errores = [] # Se prepara una lista para almacenar todos los errores
    ruta_obj = request.scope.get("route")
    ruta_name = getattr(ruta_obj, "name", "")

    for error in exc.errors():
        parametro = error.get("loc", [None])[-1]
        tipo = error.get("type", "")
        ctx = error.get("ctx", {})

        ruta_dicc = MNESAJES_ERROR.get(ruta_name, {})
        parametro_dicc = ruta_dicc.get(parametro, {})

        mensaje_dicc = parametro_dicc.get(tipo)
        if mensaje_dicc:
            try:
                mensaje = mensaje_dicc.format(**ctx)
            except Exception:
                mensaje = mensaje_dicc
            errores.append(mensaje)
            continue

        # Fallbacks generales cuando no hay mapping específico
        msg = error.get("msg", "Valor inválido")
        if tipo.startswith("type_error.integer") or tipo.startswith("type_error.number"):
            errores.append(f"El parámetro {parametro} debe ser un número")
        elif "not_ge" in tipo:
            limit_value = ctx.get("limit_value") or ctx.get("ge") or ctx.get("limit")
            if limit_value is not None:
                errores.append(f"El parámetro {parametro} debe ser mayor o igual a {limit_value}")
            else:
                errores.append(f"El parámetro {parametro} tiene un valor menor al permitido")
        elif "not_le" in tipo:
            limit_value = ctx.get("limit_value") or ctx.get("le") or ctx.get("limit")
            if limit_value is not None:
                errores.append(f"El parámetro {parametro} debe ser menor o igual a {limit_value}")
            else:
                errores.append(f"El parámetro {parametro} tiene un valor mayor al permitido")
        else:
            errores.append(f"Error en el parámetro {parametro}: {msg}")
    return JSONResponse(
        status_code=422, # en la validacion de la informacion es 422
        content={
            "detalles": errores
        }
    )
