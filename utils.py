class ValueOutOfRange(Exception):
    pass

class NoAvailableAction(Exception):
    pass

def element_wise_addition(x, y):
    return tuple([sum(i) for i in zip(x, y)])
