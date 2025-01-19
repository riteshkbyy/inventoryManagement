from django.conf import settings
from bson.objectid import ObjectId
# Create your models here.
class Supplier:
    collection = settings.MONGO_DB["suppliers"]

    @staticmethod
    def create(name, contact_info):
        data = {"name": name, "contact_info": contact_info}
        return Supplier.collection.insert_one(data)

    @staticmethod
    def get_all():
        return list(Supplier.collection.find())

    @staticmethod
    def get_by_id(supplier_id):
        return Supplier.collection.find_one({"_id": ObjectId(supplier_id)})

    @staticmethod
    def delete(supplier_id):
        return Supplier.collection.delete_one({"_id": ObjectId(supplier_id)})

    @property
    def id(self):
        return str(self._id)