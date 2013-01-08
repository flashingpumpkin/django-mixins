import uuid


def connect(signal, **kwargs):
    """
    Decorator to connect to a signal.

    >>> @connect(post_save, sender=auth.User)
    >>> def printer(sender, instance, **kwargs):
    >>>     print 'Saved user', instance
    """
    kwargs.update({
            'weak': False,
            'dispatch_uid': str(uuid.uuid4())})
    def wrapper(func):
        signal.connect(func, **kwargs)
        return func
    return wrapper
