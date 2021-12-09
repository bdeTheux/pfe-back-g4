from db import database
from models.Address import Address

database = database.get_database()


def get_addresses():
    mango = {
        'selector': {'type': 'Addresses'},
        'fields': ['campus', 'lat', 'long']
    }
    return list(database.find(mango))


def get_address_by_id(_id):
    return Address.load(database, _id)


def create_address(_data):
    if Address.load(database, _data.campus):
        raise AttributeError("The address exists already")
    database[_data['campus']] = {'campus': _data['campus'], 'lat': _data['lat'], 'long': _data['long']}
    return _data['campus']


def delete_address(_id):
    address = Address.load(database, _id)
    if not address:
        raise AttributeError("No reference")
    return database.delete(address)


def edit_address(_id, _data):
    address = Address.load(database, _id)
    if not address:
        raise AttributeError("No reference")

    if _data['campus'] and _data['campus'] != address.campus:
        database.copy(address, _data['campus'])
        copy = Address.load(database, _data['campus'])
        database.delete(address)
        address = copy

    if _data['lat']:
        address.lat = _data['lat']
    if _data['long']:
        address.long = _data['long']
    return address.store(database)
