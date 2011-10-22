from functools import update_wrapper

def raises(exception):
    def decorator(fn):
        def wrapper(self, *args, **kw):
            self.assertRaises(exception, fn, self, *args, **kw)
        return update_wrapper(wrapper, fn)
    return decorator

def raises_regexp(exception, regex):
    def decorator(fn):
        def wrapper(self, *args, **kw):
            self.assertRaisesRegexp(exception, regex, fn, self, *args, **kw)
        return update_wrapper(wrapper, fn)
    return decorator

