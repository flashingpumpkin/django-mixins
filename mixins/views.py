
class PredicateView(object):
    """
    A view that calls :meth:`test` with the request object and all parameters
    passed to :meth:`dispatch`. Expects :meth:`test` to return a view class that
    can handle the request and return a response.
    """
    
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        
    def test(self, request, *args, **kwargs):
        """ 
        Test the current request for expected conditions and return an 
        uninstantiated view to dispatch to. Subclasses are expected to override
        this method.
        """
        raise NotImplementedError
    
    def dispatch(self, request, *args, **kwargs):
        assert hasattr(self, 'test'), "No test method on {0}".format(self)
        
        view = self.test(request, *args, **kwargs)
        return view(*self.args, **self.kwargs).dispatch(request, *args, **kwargs)

class LoggedInPredicateView(PredicateView):
    """ 
    Mixin that dispatches to different views depending on the user's logged in
    status.
    """
    logged_in = None
    """ View to dispatch to in case we're logged in. """
    logged_out = None
    """ View to dispatch to in case we're not logged in. """
    
    def test(self, request, *args, **kwargs):
        """
        Test if the current user is logged in or not and return either 
        :attr:`logged_in` or :attr:`logged_out` 
        """
        assert self.logged_in is not None, "No view handling the logged in state on {0}".format(self)
        assert self.logged_out is not None, "No view handling the logged out state on {0}".format(self)
        
        if request.user.is_authenticated():
            return self.logged_in
        return self.logged_out