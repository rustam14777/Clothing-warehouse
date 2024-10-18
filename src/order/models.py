from datetime import date

from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class Order(Base):
    __tablename__ = 'orders'

    id: Mapped[int] = mapped_column(primary_key=True)
    name_user: Mapped[str] = mapped_column(nullable=False)
    birthdate: Mapped[date] = mapped_column(nullable=False)
    email_user: Mapped[str] = mapped_column(index=True, nullable=False)
    name_clothing: Mapped[str] = mapped_column(index=True, nullable=False)
    size: Mapped[str] = mapped_column(nullable=False)

    def __str__(self):
        return (f'{self.__class__.__name__}(id={self.id}, name_user={self.name_user}, '
                f'birthdate={self.birthdate}, email_user={self.email_user}, '
                f'name_clothing={self.name_clothing}, size={self.size})')

    def __repr__(self):
        return str(self)
