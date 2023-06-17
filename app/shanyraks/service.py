from app.config import database
from .adapters.s3_service import S3Service
from .repository.repository import ShanyrakRepository


class Service:
    def __init__(self, repository: ShanyrakRepository):
        self.repository = repository
        self.s3_service = S3Service()


def get_service():
    repository = ShanyrakRepository(database)
    svc = Service(repository)
    return svc