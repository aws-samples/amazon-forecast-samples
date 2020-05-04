class ResourcePending(Exception):
    pass


class ResourceFailed(Exception):
    pass


def take_action(status):
    if status in {'CREATE_PENDING', 'CREATE_IN_PROGRESS'}:
        raise ResourcePending
    if status != 'ACTIVE':
        raise ResourceFailed
    return True

def take_action_delete(status):
    if status in {'DELETE_PENDING', 'DELETE_IN_PROGRESS'}:
        raise ResourcePending
    raise ResourceFailed

