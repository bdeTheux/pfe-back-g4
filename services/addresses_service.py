from db import database
from models.Address import Address

database = database.get_database()


def get_addresses() -> list:
    mango = {
        'selector': {'type': 'Address'},
        'fields': ['campus', 'lat', 'long']
    }
    return list(database.find(mango))


def get_address_by_id(_id: str) -> Address:
    return Address.load(database, _id)


def create_address(_campus: str, _lat: str, _long: str) -> str:
    if Address.load(database, _campus):
        raise AttributeError("L'adresse existe déjà.")
    database[_campus] = dict(type='Address', campus=_campus, lat=_lat, long=_long)
    return _campus


def delete_address(_id: str):
    address = Address.load(database, _id)
    if not address:
        raise AttributeError("L'adresse n'existe pas/plus.")
    return database.delete(address)


def edit_address(_id: str, _campus: str, _lat: str, _long: str):
    address = Address.load(database, _id)
    if not address:
        raise AttributeError("L'adresse n'existe pas/plus.")

    if _campus and _campus != address.campus:
        database.copy(address, _campus)
        copy = Address.load(database, _campus)
        database.delete(address)
        address = copy

    if _lat:
        address.lat = _lat
    if _long:
        address.long = _long
    return address.store(database)
