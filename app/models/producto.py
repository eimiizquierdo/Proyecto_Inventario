from pydantic import BaseModel, Field, field_validator

from datetime import datetime, date
from uuid import UUID

def validar_fecha_ingreso(value:date) -> date:
    if value > date.today():
        raise ValueError("La fecha de ingreso no puede ser mayor a la fecha actual")
    return value

class ProductCreate(BaseModel):
    name : str = Field(min_length = 1, max_length = 200)
    quantity : int = Field(ge = 1)
    ingreso_date : date = Field(default_factory = date.today)
    min_stock : int = Field(ge = 0)
    max_stock : int = Field(ge = 0, le = 1000)
    created_at : datetime = Field(default_factory = datetime.now)
    updated_at : datetime = Field(default_factory = datetime.now)

class ProductUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=200)
    quantity: int | None = Field(default=None, ge=1)
    ingreso_date: date | None = None
    min_stock: int | None = Field(default=None, ge=0)
    max_stock: int | None = Field(default=None, ge=0, le=1000)
    created_at: datetime | None = Field(default = None)
    updated_at: datetime | None = Field(default_factory=datetime.now)

    @field_validator("ingreso_date")
    def validar_fecha_ingreso(cls, value:date) -> date:
        return validar_fecha_ingreso(value)
    
class ProductOut(BaseModel):
    id : UUID
    name : str
    quantity : int
    ingreso_date : date
    min_stock : int
    max_stock : int
    created_at : datetime
    updated_at : datetime

class ProductList(BaseModel):
    total : int
    items : list[ProductOut]
    

class OneProduct(BaseModel):
    item : ProductOut