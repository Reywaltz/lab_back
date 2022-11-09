import asyncio
from asyncpg import Record, Pool
from src.models.warehouse import Status, WarehouseItem


class WarehouseRepo:
    def __init__(self, db: Pool):
        self.db = db

    GET_PRODUCTS_QUERY = """
        SELECT products.id,name,cost,country,developer,color,type,status,placement_id,placement.occupied FROM PRODUCTS INNER JOIN PLACEMENT on PRODUCTS.placement_id=placement.id
    """

    GET_PLACEMENT_QUERY = """
        SELECT * FROM PLACEMENT WHERE placement.occupied=false
    """

    UPDATE_PLACE_STATUS = """
        UPDATE placement set occupied=$1 WHERE id=$2
    """

    UPDATE_PLACEMENT = """
        UPDATE products set placement_id=$1 WHERE id=$2
    """

    UPDATE_STATUS = """
        UPDATE products set status=$1 WHERE id=$2
    """

    INSERT_PRODUCT = """
        INSERT INTO PRODUCTS (name, cost, country, developer, color, type, status, placement_id)
         VALUES ($1, $2, $3, $4, $5, $6, $7, $8) returning id
    """

    async def get_products(self) -> list[Record]:
        rows = await self.db.fetch(self.GET_PRODUCTS_QUERY)
        return [dict(value) for value in rows]

    async def get_free_spaces(self) -> list[Record]:
        rows = await self.db.fetch(self.GET_PLACEMENT_QUERY)

        return [dict(value) for value in rows]

    async def change_placement(self, new_id: int, product: WarehouseItem):

        old_id = product.placement.id

        await asyncio.wait([
            self.db.fetch(self.UPDATE_PLACEMENT, new_id, product.id),
            self.db.fetch(self.UPDATE_PLACE_STATUS, True, new_id),
            self.db.fetch(self.UPDATE_PLACE_STATUS, False, old_id),
        ])

    async def update_status(self, product_id: int, status: Status):
        await self.db.fetch(self.UPDATE_STATUS, status, product_id)

    async def create_product(self, product: WarehouseItem):
        product_id = await self.db.fetch(
            self.INSERT_PRODUCT,
            product.name,
            product.cost,
            product.country,
            product.developer,
            product.color,
            product.type,
            product.status.value,
            product.placement.id,
        )
        await self.db.fetch(self.UPDATE_PLACE_STATUS, True, product.placement.id)

    @classmethod
    def create(cls, db: Pool):
        return cls(db)
