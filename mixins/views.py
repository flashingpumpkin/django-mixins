from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
class ContextMixin(object):
    """ 
    Extend the template context with a static / dynamic data before sending
    it to the template response. Only works with views making usage of
    :class:`django.views.generic.base.TemplateResponseMixin`
    """
    context = None
    """
    Dict of additional context to be passed into the template.
    """
    
    def get_context(self):
        """ 
        Returns :attr:`context` to extend the template context. Override to add
        context dynamically.
        """
        assert self.context is not None, "No 'context' attribute on {0}".format(self)
        assert isinstance(self.context , dict), "'context' attribute is not a dict"
        return self.context
    
    def render_to_response(self, context, **response_kwargs):
        context.update(self.get_context())
        return super(ContextMixin, self).render_to_response(context, **response_kwargs)

class ResponseKwargsMixin(object):
    """
    Pass static / dynamic response ``**kwargs`` into the response. This could
    be custom headers or a status code or whatever kwargs your response class
    takes. Only works with view making usage of 
    :class:`django.views.generic.base.TemplateResponseMixin`.
    """
    response_kwargs = None
    """
    Dict of kwargs to pass into the response class when instantiating.
    """
    
    def get_response_kwargs(self):
        """
        Returns :attr:`response_kwargs` to extend the response kwargs already
        received in :meth:`render_to_response`.
        """
        assert self.response_kwargs is not None, "No 'response_kwargs' attribute on {0}".format(self)
        assert isinstance(self.response_kwargs, dict), "'response_kwargs' attribute is not a dict"
        return self.response_kwargs
    
    def render_to_response(self, context, **response_kwargs):
        response_kwargs.update(self.get_response_kwargs())
        return super(ResponseKwargsMixin, self).render_to_response(context, **response_kwargs)
    

class TestMixin(object):
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

class LoggedInTestMixin(TestMixin):
    """ 
    Mixin that dispatches to different views depending on the user's logged in
    status **without redirecting the user**.
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


class LoginRequired(object):
    """
    Mixin wrapper around the ``django.contrib.auth.login_required``
    view decorator.
    """
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequired, self).dispatch(request, *args, **kwargs)
        
