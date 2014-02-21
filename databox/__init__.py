from databox.context import ScopeContext
from databox.munge import MungeManager, MungeOp

class FrameColumn(object):
    """ dummy object to represent a dataframe column """
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name

    def __str__(self):
        return repr(self)

def dplyr(df):
    manager = MungeManager(df)
    scope = {}
    # dplyr funcs
    scope['group_by'] = MungeOp(manager, 'group_by')
    scope['summarize'] = MungeOp(manager, 'summarize')
    scope['arrange'] = MungeOp(manager, 'arrange')
    scope['head'] = MungeOp(manager, 'head')
    # column scope
    for c in df.columns:
        scope[c] = FrameColumn(c)
    # regular ops
    scope['sum'] = MungeOp(manager, 'sum', top_level=False)
    scope['desc'] = MungeOp(manager, 'desc', top_level=False)
    context = ScopeContext(scope, manager.exit)
    return context

if __name__ == '__main__':
    import pandas as pd
    df = pd.util.testing.makeDataFrame()
    with dplyr(df):
        group_by(A, B)
        summarize(total=sum(C))
        arrange(desc(D))

    # manager.operations => [group_by(A,B), summarize(total=sum(C)), arrange(desc(D))]
