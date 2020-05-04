class ResourcePending(Exception):
    pass


class ResourceFailed(Exception):
    pass


def take_action(status):
    if status in {'DELETE_PENDING', 'DELETE_IN_PROGRESS'}:
        raise ResourcePending
    raise ResourceFailed
