from src.models.placement import Placement
from src.models import WarehouseItem

mock_places = [
    {

        'id': 1,
        'occupied': True,
    },
    {
        'id': 2,
        'occupied': True,
    },
    {
        'id': 3,
        'occupied': True,
    },
    {
        'id': 4,
        'occupied': False,
    },
    {
        'id': 5,
        'occupied': False,
    },
]

places = [Placement(**mock) for mock in mock_places]

mock_response = [
    WarehouseItem(**{
        'id': 1,
        'name': 'Кофемашина',
        'cost': 512.123,
        'country': 'Россия',
        'developer': 'Bosh',
        'color': 'Красный',
        'type': 'Машина',
        'status': 'Доступен',
        'placement': places[0].dict()
    }),
    WarehouseItem(**{
        'id': 2,
        'name': 'Apple Watch',
        'cost': 100,
        'country': 'США',
        'developer': 'Apple',
        'color': 'Жёлтый',
        'type': 'Часы',
        'status': 'Не доступен',
        'placement': places[1].dict()
    }),
    WarehouseItem(**{
        'id': 3,
        'name': 'Кружка',
        'cost': 2000,
        'country': 'Китай',
        'color': 'Синяя',
        'developer': 'OnePlus',
        'type': 'Посуда',
        'status': 'Списан',
        'placement': places[2].dict()
    }),
]
