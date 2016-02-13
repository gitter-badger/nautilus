# external imports
from nautilus import APIGateway
from graphene import Schema, ObjectType, String
from nautilus.api import ServiceObjectType
from nautilus.api.fields import Connection
# local imports
from .recipes import service as RecipeService
from .ingredients import service as IngredientService


# create the schema based on the query object
schema = Schema(name='Product Schema')

## define the schema that encapsulates the cloud

class Recipe(ServiceObjectType):

    class Meta:
        service = RecipeService
    
    # you can avoid circular/undefined references using strings - nautilus will look 
    # for the corresponding ServiceObjectType
    ingredients = Connection('Ingredient', description = 'The ingredients in this recipe.')



class Ingredient(ServiceObjectType):

    class Meta:
        service = IngredientService
    
    # connections are resolved/joined using the appropriate connection service
    recipes = Connection(Recipe, description = 'The recipes with this ingredient')


# add the query to the schema
schema.query = Query

# create a nautilus service with just the schema
service = APIGateway(schema=schema)