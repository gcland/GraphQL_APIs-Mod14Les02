import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from models import Inventory as InventoryModel, db
from sqlalchemy.orm import Session

class Inventory(SQLAlchemyObjectType):
    class Meta:
        model = InventoryModel

class Query(graphene.ObjectType):
    inventories = graphene.List(Inventory)

    def resolve_inventories(self, info):
        return db.session.execute(db.select(InventoryModel)).scalars()
    
class AddInventory(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        quantity = graphene.Int(required=True)
        price = graphene.Float(required=True)
        category = graphene.String(required=True)

    inventory = graphene.Field(Inventory)

    def mutate(self, info, name, quantity, price, category):
        with Session(db.engine) as session:
            with session.begin():
                inventory = InventoryModel(name=name, quantity=quantity, price=price, category=category)
                session.add(inventory)

            session.refresh(inventory)
            return AddInventory(inventory=inventory)
        
class UpdateInventory(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        name = graphene.String(required=True)
        quantity = graphene.Int(required=True)
        price = graphene.Float(required=True)
        category = graphene.String(required=True)

    inventory = graphene.Field(Inventory)

    def mutate(self, info, id, name, quantity, price, category):
        with Session(db.engine) as session:
            with session.begin():
                inventory = session.execute(db.select(InventoryModel).where(InventoryModel.id == id)).scalars().first()
                if inventory:
                    inventory.name = name
                    inventory.quantity = quantity
                    inventory.price = price
                    inventory.category = category
                else:
                    return None

            session.refresh(inventory)
            return UpdateInventory(inventory=inventory)
        
class DeleteInventory(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    inventory = graphene.Field(Inventory)

    def mutate(self, info, id):
        with Session(db.engine) as session:
            with session.begin():
                inventory = session.execute(db.select(InventoryModel).where(InventoryModel.id == id)).scalars().first()
                if inventory:
                    session.delete(inventory)
                    return 'Deleted.'
                else:
                    return None
            session.refresh(inventory)
            return DeleteInventory(inventory=inventory)

class Mutation(graphene.ObjectType):
    create_inventory = AddInventory.Field()
    update_inventory = UpdateInventory.Field()
    delete_inventory = DeleteInventory.Field()

