import abc

from liang import (
    environment,
    utils
)


class FailureHandler(abc.ABC):

    @abc.abstractmethod
    def handle(self, context: environment.ExecutionContext):
        pass


class RaiseExceptionFailureHandler(FailureHandler):

    def handle(self, context: environment.ExecutionContext):
        func = context.function
        signature = utils.get_function_signature(context.args, context.kwargs)

        raise RuntimeError(
            f"Function {func.__name__!r}({signature}) expected to have {context.metric_name} to be "
            f"{context.metric_expected} but is actually {context.metric_actual}.")
