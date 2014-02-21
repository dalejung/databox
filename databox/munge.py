class MungeManager(object):
    def __init__(self, obj):
        self.obj = obj
        self.operations = []

    def add_op(self, op):
        self.operations.append(op)

    def exit(self):
        print self.operations

class MungeOp(object):
    def __init__(self, manager, op_name, top_level=True):
        self.manager = manager
        self.op_name = op_name
        self.top_level = top_level

    def __call__(self, *args, **kwargs):
        op_call = MungeOpCall(self, *args, **kwargs)
        if self.top_level:
            self.manager.add_op(op_call)
        return op_call

class MungeOpCall(object):
    def __init__(self, op, *args, **kwargs):
        self.op = op
        self.args = args
        self.kwargs = kwargs

    def __repr__(self):
        argstring = ''
        if self.args:
            argstring += ",".join([str(arg) for arg in self.args])
        if self.kwargs:
            argstring += ",".join(["{k}={v}".format(k=k, v=v) for k,v
                                   in self.kwargs.iteritems()])
        return "{op_name}({argstring})".format(op_name=self.op.op_name,
                                                    argstring=argstring)

