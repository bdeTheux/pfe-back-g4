from db import database
from models.Address import Address

database = database.get_database()


def get_addresses():
    mango = {
        'selector': {'type': 'Address'},
        'fields': ['campus', 'lat', 'long']
    }
    return list(database.find(mango))


def get_address_by_id(_id):
    return Address.load(database, _id)


def create_address(_campus, _lat, _long):
    if Address.load(database, _campus):
        raise AttributeError("The address exists already")
    database[_campus] = {'type': 'Address', 'campus': _campus, 'lat': _lat, 'long': _long}
    return _campus


def delete_address(_id):
    address = Address.load(database, _id)
    if not address:
        raise AttributeError("No reference")
    return database.delete(address)


def edit_address(_id, _campus, _lat, _long):
    address = Address.load(database, _id)
    if not address:
        raise AttributeError("No reference")

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
