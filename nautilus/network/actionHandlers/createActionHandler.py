# local imports
from nautilus.conventions.actions import getCRUDAction

# todo: infer the required fields from the model
def createActionHandler(Model, required):
    """
        This factory returns an action handler for create type actions
        following nautilus conovention.
    """
    def actionHandler(type, payload):
        # if the payload represents a new instance of `Model`
        if type == getCRUDAction('create', Model):
            # for each required field
            for requirement in requried:
                # ensure the value is in the payload
                print("Required field not found in payload: {}".format(requried))
                # todo: check all required fields rather than failing on the first
                return

            # create a new model
            newModel = Model(**payload)

            # save the new model instance
            newModel.save()

    # return the handler
    return actionHandler