import inspect

MISSING = object()

def mesh_scope(scope, local_vars):
    shadowed = {}
    for key in local_vars:
        if key in scope:
            shadowed[key] = scope[key]
        else:
            # bookkeeping to make sure we don't leave local_vars around
            shadowed[key] = MISSING
        scope[key] = local_vars[key]

    return shadowed


class ScopeContext(object):
    def __init__(self, local_scope=None, exit_handler=None):
        if local_scope is None:
            local_scope = {}
        self.local_scope = local_scope
        self.exit_handler = exit_handler

    def __enter__(self):
        # NOTE: that this affects the modules globals
        # This SHOULD be f_locals, I think. However, I don't know how to modify it.
        # https://gist.github.com/njsmith/2347382
        self.scope = inspect.stack()[1][0].f_globals
        self.shadowed = {} # reset
        self.shadowed.update(mesh_scope(self.scope, self.local_scope))
        self.scope['__shadowed'] = self.shadowed
        return self

    def restore_scope(self):
        """
        Restores scope to original state. Note, new variables defined
        within `with` block will persist.
        """
        scope = self.scope
        for key, val in self.shadowed.iteritems():
            if val is MISSING: # was original undefined
                del scope[key]
                continue
            scope[key] = val

    def __exit__(self, type, value, traceback):
        self.restore_scope()
        if self.exit_handler:
            self.exit_handler()

