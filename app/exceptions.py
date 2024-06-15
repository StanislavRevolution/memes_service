from fastapi import HTTPException, status


class MemesException(HTTPException):
    status_code = 500
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserAlreadyExistsException(MemesException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Пользователь уже существует"


class IncorrectEmailOrPasswordException(MemesException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверная почта или пароль"


class TokenExpiredException(MemesException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Срок действия токена истек"


class TokenAbsentException(MemesException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Отсутствуют права доступа (токен)"


class IncorrectTokenFormatException(MemesException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверный формат токена"


class UserIsNotPresentException(MemesException):
    status_code = status.HTTP_401_UNAUTHORIZED


class ErrorLoadingImageToS3Exception(MemesException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Ошибка при загрузке изображения в удаленное хранилище"


class EmpyMemesStorageException(MemesException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Не удалось найти мем/мемы"
