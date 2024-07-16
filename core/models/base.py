from sqlalchemy.orm import mapped_column, Mapped, declared_attr, DeclarativeBase


class Base(DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"


    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)