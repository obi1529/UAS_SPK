from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass

class Smartphone(Base):
    __tablename__ = "smartphone"

    id : Mapped[int] = mapped_column(primary_key=True)
    merek : Mapped[str]
    ram : Mapped[int]
    processor : Mapped[str]
    versi_os : Mapped[str]
    battery : Mapped[int]
    harga : Mapped[int]
    layar : Mapped[float]

    def __repr__(self) -> str :
        return f"id={self.id}, merek={self.merek}, ram={self.ram}, processor={self.processor}, versi_os={self.versi_os}, battery={self.battery}, harga={self.harga}, layar={self.layar}"

