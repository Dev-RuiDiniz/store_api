from typing import List, Optional
from uuid import UUID
from datetime import datetime

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
import pymongo
from bson import Decimal128

from store.db.mongo import db_client
from store.models.product import ProductModel
from store.schemas.product import ProductIn, ProductOut, ProductUpdate, ProductUpdateOut
from store.core.exceptions import NotFoundException, InsertException


class ProductUsecase:
    def __init__(self) -> None:
        self.client: AsyncIOMotorClient = db_client.get()
        self.database: AsyncIOMotorDatabase = self.client.get_database()
        self.collection = self.database.get_collection("products")

    async def create(self, body: ProductIn) -> ProductOut:
        try:
            product_model = ProductModel(**body.model_dump())
            await self.collection.insert_one(product_model.model_dump())
            return ProductOut(**product_model.model_dump())
        except Exception as exc:
            raise InsertException(str(exc))

    async def get(self, id: UUID) -> ProductOut:
        result = await self.collection.find_one({"id": id})

        if not result:
            raise NotFoundException(message=f"Produto não encontrado com o ID: {id}")

        return ProductOut(**result)

    async def query(
        self,
        price_min: Optional[float] = None,
        price_max: Optional[float] = None
    ) -> List[ProductOut]:
        filter_query = {}

        # Filtro por faixa de preço, se fornecido
        if price_min is not None or price_max is not None:
            price_filter = {}
            if price_min is not None:
                price_filter["$gt"] = Decimal128(str(price_min))
            if price_max is not None:
                price_filter["$lt"] = Decimal128(str(price_max))
            filter_query["price"] = price_filter

        results = self.collection.find(filter_query)
        return [ProductOut(**item) async for item in results]

    async def update(self, id: UUID, body: ProductUpdate) -> ProductUpdateOut:
        # Verifica se o produto existe antes de atualizar
        existing = await self.collection.find_one({"id": id})
        if not existing:
            raise NotFoundException(message=f"Produto não encontrado com o ID: {id}")

        update_data = body.model_dump(exclude_none=True)

        # Atualiza updated_at com o valor enviado ou com o horário atual
        update_data["updated_at"] = body.updated_at or datetime.utcnow()

        result = await self.collection.find_one_and_update(
            filter={"id": id},
            update={"$set": update_data},
            return_document=pymongo.ReturnDocument.AFTER,
        )

        return ProductUpdateOut(**result)

    async def delete(self, id: UUID) -> bool:
        product = await self.collection.find_one({"id": id})
        if not product:
            raise NotFoundException(message=f"Produto não encontrado com o ID: {id}")

        result = await self.collection.delete_one({"id": id})
        return result.deleted_count > 0


product_usecase = ProductUsecase()
