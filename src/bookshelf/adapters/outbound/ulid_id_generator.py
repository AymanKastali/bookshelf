from ulid import ULID

from bookshelf.domain.port.id_generator import IdGenerator


class UlidIdGenerator(IdGenerator):
    def generate(self) -> str:
        return str(ULID())
