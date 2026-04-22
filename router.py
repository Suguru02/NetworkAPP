from fastapi import APIRouter
from dao import HabrDao
from schemas import SHabr
from parser import parse


router = APIRouter(prefix='/habr', tags=['Habr'])

@router.post("/parse/")
async def data_parse() -> None:
    
    all_data = parse()

    for data in all_data:
        await HabrDao.add_data(
            title=data['title'],
            author=data['author'],
            publish_date=data['publish_date'],
            url=data['url']
        )


@router.get("/find/")
async def find_data(limit: int, offset: int) -> list[SHabr]:

    return await HabrDao.find_data(limit=limit, offset=offset)