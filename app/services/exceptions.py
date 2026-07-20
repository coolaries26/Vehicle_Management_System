class ServiceException(Exception):
    pass


class NotFoundException(ServiceException):
    pass


class DuplicateRecordException(ServiceException):
    pass


class ValidationException(ServiceException):
    pass