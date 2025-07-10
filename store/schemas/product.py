from decimal import Decimal
from typing import Annotated, Optional
from datetime import datetime

from bson import Decimal128
from pydantic import AfterValidator, Field

from store.schemas.base import BaseSchemaMixin, OutSchema


# 👇 Converte Decimal128 → Decimal para entrada do MongoDB
def convert_decimal_128(v):
    if isinstance(v, Decimal128):
        return v.to_decimal()
    return v


# Usar em campos que recebem Decimal do MongoDB
DecimalFromDB = Annotated[Decimal, AfterValidator(convert_decimal_128)]


class ProductBase(BaseSchemaMixin):
    name: str = Field(..., description="Product name")
    quantity: int = Field(..., description="Product quantity")
    price: Decimal = Field(..., description="Product price")
    status: bool = Field(..., description="Product status")


class ProductIn(ProductBase):
    ...


class ProductOut(ProductIn, OutSchema):
    updated_at: Optional[datetime] = Field(None, description="Data da última atualização")


class ProductUpdate(BaseSchemaMixin):
    quantity: Optional[int] = Field(None, description="Product quantity")
    price: Optional[DecimalFromDB] = Field(None, description="Product price")
    status: Optional[bool] = Field(None, description="Product status")
    updated_at: Optional[datetime] = Field(None, description="Data manual de atualização")


class ProductUpdateOut(ProductOut):
    ...
