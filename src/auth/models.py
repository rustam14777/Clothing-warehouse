import datetime

from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    surname: Mapped[str] = mapped_column(nullable=False)
    birthdate: Mapped[datetime.date] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)
    is_admin: Mapped[bool] = mapped_column(default=False)
    is_user: Mapped[bool] = mapped_column(default=True)

    def __str__(self):
        return (
            f'{self.__class__.__name__}(id={self.id}, name={self.name}, surname={self.surname}, '
            f'birthdate={self.birthdate}, '
            f'email={self.email}, hashed_password={self.hashed_password}, '
            f'is_active={self.is_active}, is_admin={self.is_admin}, is_user={self.is_user}'
        )

    def __repr__(self):
        return str(self)
