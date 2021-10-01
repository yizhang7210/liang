class ExecutionContext:
    def __init__(self, func, args, kwargs, metric_name, metric_expected, metric_actual):
        self.function = func
        self.args = args
        self.kwargs = kwargs
        self.metric_name = metric_name
        self.metric_expected = metric_expected
        self.metric_actual = metric_actual

