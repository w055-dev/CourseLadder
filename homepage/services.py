from src.services import CourseService

_service: CourseService | None = None


def get_service() -> CourseService:
    """Возвращает единственный экземпляр CourseService."""
    global _service
    if _service is None:
        _service = CourseService()
        _service.load()
    return _service


def reset_service() -> None:
    """Сбрасывает кэш."""
    global _service
    _service = None
