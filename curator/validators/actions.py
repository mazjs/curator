from voluptuous import *
from ..defaults import settings
from . import SchemaCheck

### Schema information ###
# Actions: root level
def root():
    return Schema({ Required('actions'): dict })

def valid_action():
    return {
        Required('action'): Any(
            In(settings.all_actions()),
            msg='action must be one of {0}'.format(
                settings.all_actions()
            )
        )
    }

# Basic action structure
def structure(data, location):
    # Validate the action type first, so we can use it for other tests
    valid_action_type = SchemaCheck(
        data,
        Schema(valid_action(), extra=True),
        'action type',
        location,
    ).result()
    # Build a valid schema knowing that the action has already been validated
    retval = valid_action()
    retval.update(
        { Optional('description', default='No description given'): str }
    )
    retval.update(
        { Optional('options', default=settings.default_options()): dict } )
    action = data['action']
    if action == 'create_index':
        # The create_index action should not have a 'filters' block
        pass
    elif action == 'alias':
        # The alias action should not have a filters block, but should have
        # an add and/or remove block.
        retval.update(
            {
                Optional('add'): dict,
                Optional('remove'): dict,
            }
        )
    else:
        retval.update(
            { Optional('filters', default=settings.default_filters()): list }
        )
    return Schema(retval)
