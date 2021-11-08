import abc
import logging

from liang import (
    environment,
    errors
)

logger = logging.getLogger(__name__)


class FailureHandler(abc.ABC):

    @abc.abstractmethod
    def handle(self, context: environment.ExecutionContext):
        pass


class RaiseExceptionFailureHandler(FailureHandler):

    def handle(self, context: environment.ExecutionContext):
        message = f"Function {context.function.__name__!r} expected to have {context.metric_name} to be {context.metric_expected}"
        if context.metric_actual:
            message += f" but is actually {context.metric_actual}"
        raise errors.MetricNotSatisfiedError(message)


class LogWarningFailureHandler(FailureHandler):

    def handle(self, context: environment.ExecutionContext):
        message = f"Function {context.function.__name__!r} expected to have {context.metric_name} to be {context.metric_expected}"
        if context.metric_actual:
            message += f" but is actually {context.metric_actual}"
        logger.warning(message)

