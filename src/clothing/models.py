from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from src.database import Base


class Clothing(Base):
    __tablename__ = 'clothing'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True, index=True)

    sizes: Mapped[list['Size']] = relationship(back_populates='clothing', cascade='all, '
                                               'delete-orphan')

    def __str__(self):
        return f'{self.__class__.__name__}(id={self.id}, name={self.name})'

    def __repr__(self):
        return str(self)


class Size(Base):
    __tablename__ = 'sizes'

    id: Mapped[int] = mapped_column(primary_key=True)
    clothing_id: Mapped[int] = mapped_column(ForeignKey('clothing.id', ondelete='CASCADE'),
                                             index=True)
    size: Mapped[str] = mapped_column(nullable=False, index=True)
    quantity: Mapped[int] = mapped_column(nullable=False)

    clothing: Mapped['Clothing'] = relationship(back_populates='sizes')

    def __str__(self):
        return (f'{self.__class__.__name__}(id={self.id}, clothing_id={self.clothing_id}, '
                f'size={self.size}, '
                f'quantity'
                f'={self.quantity})')

    def __repr__(self):
        return str(self)
