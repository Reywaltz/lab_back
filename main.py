from decimal import Decimal
import uvicorn
from fastapi import FastAPI, Request, Depends
import asyncpg
from pydantic import BaseModel, Field
from fastapi.responses import ORJSONResponse
from fastapi.middleware.cors import CORSMiddleware
from src.models.warehouse import Status
from src.repository import WarehouseRepo
from src.models.placement import Placement

from src.models import WarehouseItem

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=["*"],
    allow_headers=["*"],
)


async def get_db(request: Request) -> asyncpg.Connection:
    return request.app.db


async def get_repo(request: Request) -> WarehouseRepo:
    yield request.app.repo


async def warehouse_repo(db: asyncpg.Connection = Depends(get_db)):
    yield WarehouseRepo(db)


@app.on_event('startup')
async def startup():
    app.db = await conn_db()
    app.repo = WarehouseRepo(app.db)
    print(app.db)


async def conn_db() -> asyncpg.Pool:
    DB_URL = 'postgres://test:test@localhost:5433/test'
    # DB_URL = 'postgres://rypnfejq:38qfNhBDlZpBzTSiog3yphjQCH1q1X7F@mouse.db.elephantsql.com/rypnfejq'
    pool = await asyncpg.create_pool(dsn=DB_URL)
    return pool


@app.get(
    '/api/v1/products',
    response_model=list[WarehouseItem],
    response_class=ORJSONResponse,
)
async def get_products(repository: WarehouseRepo = Depends(get_repo)) -> list[WarehouseItem]:
    out = []
    res = await repository.get_products()
    for item in res:
        placement = Placement(
            **{"id": item.get('placement_id'), "occupied": item.get("occupied")})
        out.append(WarehouseItem(placement=placement, **item))
    return out


@app.get(
    '/api/v1/places',
    response_model=list[Placement],
    response_class=ORJSONResponse,
)
async def get_free_places(rep=Depends(get_repo)) -> list[Placement]:
    places = await rep.get_free_spaces()
    return [Placement(**item) for item in places]


@app.post(
    '/api/v1/place/{new_id}',
    response_class=ORJSONResponse,
)
async def change_place(
    new_id: int,
    product: WarehouseItem,
    repository: WarehouseRepo = Depends(warehouse_repo)
):
    await repository.change_placement(new_id, product)


class ChangeStatus(BaseModel):
    status: Status


@app.post(
    '/api/v1/product/{product_id}',
    response_class=ORJSONResponse,
)
async def update_status(
    product_id: int,
    status: ChangeStatus,
    repository: WarehouseRepo = Depends(warehouse_repo)
):
    await repository.update_status(product_id, status.status.value)


class InputForm(BaseModel):
    name: str = Field(alias="nameValue")
    cost: Decimal = Field(alias="moneyValue")
    country: str = Field(alias="countryValue")
    developer: str = Field(alias="developerValue")
    color: str = Field(alias="colorValue")
    type: str = Field(alias="typeValue")
    status: Status = Field(alias="statusValue")
    placement: Placement = Field(alias="placeValue")


@app.post(
    '/api/v1/product',
    response_class=ORJSONResponse,
)
async def create_product(product: InputForm, repository: WarehouseRepo = Depends(warehouse_repo)):
    await repository.create_product(product)

if __name__ == '__main__':
    uvicorn.run(
        app,
        host='0.0.0.0',
        port=8000,
    )
