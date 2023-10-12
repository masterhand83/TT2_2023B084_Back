""" ORM classes used to map the IM database tables to Python objects using SQLAlchemy. """

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.types import DateTime, Uuid, SmallInteger
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER, SMALLDATETIME, BIT
from sqlalchemy.dialects.mssql import VARCHAR, CHAR
from sqlalchemy.dialects.mssql import INTEGER, SMALLINT, TINYINT, DECIMAL
from sqlalchemy import text, ForeignKey
from typing import List


class Base(DeclarativeBase):
    """ Base class for ORM mapping of the IM database tables. """
    pass


class Marca(Base):
    """ Class used for ORM mapping of the MARCA table.

    :param id: (Primary Key) identifier of the object.
    :param marca: brand name.
    :param productos: (Relationship) list of :class:`Producto` objects associated with the brand.
    :return: ORM object for the MARCA table.

    Generated SQL:
        CREATE TABLE [MARCA] (
            id SMALLINT NOT NULL IDENTITY,
            marca VARCHAR(50) NOT NULL,
            PRIMARY KEY (id)
        )
    """

    __tablename__ = 'MARCA'

    id: Mapped[SmallInteger] = mapped_column(SMALLINT, primary_key=True)
    marca: Mapped[str] = mapped_column(VARCHAR(50), nullable=False)
    productos: Mapped[List["Producto"]] = relationship("Producto", back_populates="marca")
    def as_dict(self):
        return {
            "id": self.id,
            "marca": self.marca
        }

    def __repr__(self):
        return f"Marca(id={self.id}, marca={self.marca})"


class Producto(Base):
    """ Class used for ORM mapping of the PRODUCTO table.

    :param codigo: (Primary Key) identifier of the object.
    :param nombre: product name.
    :param precio_unitario: unit price of the product.
    :param existencias: number of products in stock.
    :param descripcion: description of the product.
    :param id_marca: (Foreign Key) identifier of the :class:`Marca` object.
    :param activo: indicates if the product is active or not.
    :param marca: (Relationship) :class:`Marca` object associated with the product.
    :param actualizaciones: (Relationship) list of :class:`ActualizacionProducto` objects associated with the product.
    :param detalles_venta: (Relationship) list of :class:`DetalleVenta` objects associated with the product.
    :return: ORM object for the PRODUCTO table.

    Generated SQL:
        CREATE TABLE [PRODUCTO] (
            codigo VARCHAR(20) NOT NULL,
            nombre VARCHAR(80) NOT NULL,
            precio_unitario DECIMAL(8, 2) NOT NULL,
            existencias SMALLINT NOT NULL,
            descripcion VARCHAR(200) NOT NULL,
            id_marca SMALLINT NOT NULL,
            activo BIT NOT NULL DEFAULT 1,
            PRIMARY KEY (codigo),
            FOREIGN KEY(id_marca) REFERENCES [MARCA] (id)
        )
    """

    __tablename__ = 'PRODUCTO'

    codigo: Mapped[str] = mapped_column(VARCHAR(20), primary_key=True)
    nombre: Mapped[str] = mapped_column(VARCHAR(80), nullable=False)
    precio_unitario: Mapped[float] = mapped_column(DECIMAL(8, 2), nullable=False)
    existencias: Mapped[SmallInteger] = mapped_column(SMALLINT, nullable=False)
    descripcion: Mapped[str] = mapped_column(VARCHAR(200), nullable=False)
    id_marca: Mapped[SmallInteger] = mapped_column(ForeignKey("MARCA.id"), nullable=False)
    activo: Mapped[bool] = mapped_column(BIT, nullable=False, server_default=text("1"))

    marca: Mapped["Marca"] = relationship("Marca", back_populates="productos")
    actualizaciones: Mapped[List["ActualizacionProducto"]] = relationship("ActualizacionProducto",
                                                                          back_populates="producto")
    detalles_venta: Mapped[List["DetalleVenta"]] = relationship("DetalleVenta", back_populates="producto")
    historial_merma: Mapped[List["RegistroMerma"]] = relationship("RegistroMerma", back_populates="producto")
    historial_existencia: Mapped[List["RegistroExistencia"]] = relationship("RegistroExistencia", back_populates="producto")

    def __repr__(self):
        return (f"Producto(codigo={self.codigo}, nombre={self.nombre}, precio_unitario={self.precio_unitario}, "
                f"existencias={self.existencias}, descripcion={self.descripcion}, id_marca={self.id_marca},"
                f" activo={self.activo})")
    def as_dict(self):
        return {
            "codigo": self.codigo,
            "nombre": self.nombre,
            "precio_unitario": float(self.precio_unitario),
            "existencias": self.existencias,
            "descripcion": self.descripcion,
            "marca": self.marca.marca,
            "activo": self.activo
        }

class RegistroMerma(Base):
    __tablename__ = 'REGISTRO_MERMA'

    id: Mapped[int] = mapped_column(INTEGER, primary_key=True)
    codigo_producto: Mapped[str] = mapped_column(
        ForeignKey("PRODUCTO.codigo"),
        nullable=False
    )
    fecha: Mapped[DateTime] = mapped_column(
        SMALLDATETIME,
        nullable=False,
        server_default=text("GETDATE()")
    )
    merma: Mapped[SmallInteger] = mapped_column(SMALLINT, nullable=False)
    subtotal: Mapped[float] = mapped_column(DECIMAL(8, 2), nullable=False)
    producto: Mapped["Producto"] = relationship(
        "Producto",
        back_populates="historial_merma"
    )

class RegistroExistencia(Base):
    __tablename__ = 'REGISTRO_EXISTENCIA'

    id: Mapped[int] = mapped_column(INTEGER, primary_key=True)
    codigo_producto: Mapped[str] = mapped_column(
        ForeignKey("PRODUCTO.codigo"),
        nullable=False
    )
    fecha: Mapped[DateTime] = mapped_column(
        SMALLDATETIME,
        nullable=False,
        server_default=text("GETDATE()")
    )
    existencia: Mapped[SmallInteger] = mapped_column(SMALLINT, nullable=False)
    producto: Mapped["Producto"] = relationship(
        "Producto",
        back_populates="historial_existencia"
    )




class Venta(Base):
    """ Class used for ORM mapping of the VENTA table.

    :param id: (Primary Key) identifier of the object.
    :param fecha: date and time of the sale.
    :param detalles_venta: (Relationship) list of :class:`DetalleVenta` objects associated with the sale.
    :return: ORM object for the VENTA table.

    Generated SQL:
        CREATE TABLE [VENTA] (
            id UNIQUEIDENTIFIER NOT NULL DEFAULT NEWSEQUENTIALID(),
            fecha SMALLDATETIME NOT NULL DEFAULT GETDATE(),
            PRIMARY KEY (id)
        )
    """
    __tablename__ = 'VENTA'

    id: Mapped[Uuid] = mapped_column(UNIQUEIDENTIFIER, primary_key=True, server_default=text("NEWSEQUENTIALID()"))
    fecha: Mapped[DateTime] = mapped_column(SMALLDATETIME, nullable=False, server_default=text("GETDATE()"))
    detalles_venta: Mapped[List["DetalleVenta"]] = relationship("DetalleVenta", back_populates="venta")

    def __repr__(self):
        return f"Venta(id={self.id}, fecha={self.fecha})"


class DetalleVenta(Base):
    """ Class used for ORM mapping of the DETALLE_VENTA table.

    :param id: (Primary Key) identifier of the object.
    :param cantidad: number of products sold.
    :param codigo_producto: (Foreign Key) identifier of the :class:`Producto` object.
    :param id_venta: (Foreign Key) identifier of the :class:`Venta` object.
    :param venta: (Relationship) :class:`Venta` object associated with the sale detail.
    :param producto: (Relationship) :class:`Producto` object associated with the sale detail.
    :return: ORM object for the DETALLE_VENTA table.

    Generated SQL:
        CREATE TABLE [DETALLE_VENTA] (
            id INTEGER NOT NULL IDENTITY,
            cantidad SMALLINT NOT NULL,
            codigo_producto VARCHAR(20) NOT NULL,
            id_venta UNIQUEIDENTIFIER NOT NULL,
            PRIMARY KEY (id),
            FOREIGN KEY(codigo_producto) REFERENCES [PRODUCTO] (codigo),
            FOREIGN KEY(id_venta) REFERENCES [VENTA] (id)
        )
    """
    __tablename__ = 'DETALLE_VENTA'

    id: Mapped[int] = mapped_column(INTEGER, primary_key=True)
    cantidad: Mapped[SmallInteger] = mapped_column(SMALLINT, nullable=False)
    subtotal: Mapped[float] = mapped_column(DECIMAL(8, 2), nullable=False)
    codigo_producto: Mapped[str] = mapped_column(ForeignKey("PRODUCTO.codigo"), nullable=False)
    id_venta: Mapped[Uuid] = mapped_column(ForeignKey("VENTA.id"), nullable=False)
    venta: Mapped["Venta"] = relationship("Venta", back_populates="detalles_venta")
    producto: Mapped["Producto"] = relationship("Producto", back_populates="detalles_venta")

    def __repr__(self):
        return f"DetalleVenta(id={self.id}, cantidad={self.cantidad}, codigo_producto={self.codigo_producto}, " \
               f"id_venta={self.id_venta})"



class TipoActualizacion(Base):
    """ Class used for ORM mapping of the TIPO_ACTUALIZACION table.

    :param id: (Primary Key) identifier of the object.
    :param tipo: type of update.
    :param actualizaciones: (Relationship) list of :class:`ActualizacionProducto` objects associated with the type.
    :return: ORM object for the TIPO_ACTUALIZACION table.

    Generated SQL:
        CREATE TABLE [TIPO_ACTUALIZACION] (
            id TINYINT NOT NULL IDENTITY,
            tipo CHAR(20) NOT NULL,
            PRIMARY KEY (id)
        )
    """
    __tablename__ = 'TIPO_ACTUALIZACION'

    id: Mapped[int] = mapped_column(TINYINT, primary_key=True)
    tipo: Mapped[str] = mapped_column(CHAR(20), nullable=False)
    actualizaciones: Mapped[List["ActualizacionProducto"]] = relationship("ActualizacionProducto",
                                                                          back_populates="tipo")

    def __repr__(self):
        return f"TipoActualizacion(id={self.id}, tipo={self.tipo})"


class CampoActualizacion(Base):
    """ Class used for ORM mapping of the CAMPO_ACTUALIZACION table.

    :param id: (Primary Key) identifier of the object.
    :param campo: field to update.
    :param actualizaciones: (Relationship) list of :class:`ActualizacionProducto` objects associated with the field.
    :return: ORM object for the CAMPO_ACTUALIZACION table.

    Generated SQL:
        CREATE TABLE [CAMPO_ACTUALIZACION] (
            id TINYINT NOT NULL IDENTITY,
            campo CHAR(15) NOT NULL,
            PRIMARY KEY (id)
        )
    """
    __tablename__ = 'CAMPO_ACTUALIZACION'

    id: Mapped[int] = mapped_column(TINYINT, primary_key=True)
    campo: Mapped[str] = mapped_column(CHAR(15), nullable=False)
    actualizaciones: Mapped[List["ActualizacionProducto"]] = relationship("ActualizacionProducto",
                                                                          back_populates="campo")

    def __repr__(self):
        return f"CampoActualizacion(id={self.id}, campo={self.campo})"


class ActualizacionProducto(Base):
    """ Class used for ORM mapping of the ACTUALIZACION_PRODUCTO table.

    :param id: (Primary Key) identifier of the object.
    :param valor: new value of the field.
    :param fecha: date and time of the update.
    :param codigo_producto: (Foreign Key) identifier of the :class:`Producto` object.
    :param id_tipo: (Foreign Key) identifier of the :class:`TipoActualizacion` object.
    :param id_campo: (Foreign Key) identifier of the :class:`CampoActualizacion` object.
    :param producto: (Relationship) :class:`Producto` object associated with the update.
    :param tipo: (Relationship) :class:`TipoActualizacion` object associated with the update.
    :param campo: (Relationship) :class:`CampoActualizacion` object associated with the update.
    :return: ORM object for the ACTUALIZACION_PRODUCTO table.

    Generated SQL:
        CREATE TABLE [ACTUALIZACION_PRODUCTO] (
            id INTEGER NOT NULL IDENTITY,
            valor VARCHAR(200) NOT NULL,
            fecha SMALLDATETIME NOT NULL DEFAULT GETDATE(),
            codigo_producto VARCHAR(20) NOT NULL,
            id_tipo TINYINT NOT NULL,
            id_campo TINYINT NOT NULL,
            PRIMARY KEY (id),
            FOREIGN KEY(codigo_producto) REFERENCES [PRODUCTO] (codigo),
            FOREIGN KEY(id_tipo) REFERENCES [TIPO_ACTUALIZACION] (id),
            FOREIGN KEY(id_campo) REFERENCES [CAMPO_ACTUALIZACION] (id)
        )
    """
    __tablename__ = 'ACTUALIZACION_PRODUCTO'

    id: Mapped[int] = mapped_column(INTEGER, primary_key=True)
    valor: Mapped[str] = mapped_column(VARCHAR(200), nullable=False)
    fecha: Mapped[DateTime] = mapped_column(SMALLDATETIME, nullable=False, server_default=text("GETDATE()"))
    codigo_producto: Mapped[str] = mapped_column(ForeignKey("PRODUCTO.codigo"), nullable=False)
    id_tipo: Mapped[int] = mapped_column(ForeignKey("TIPO_ACTUALIZACION.id"), nullable=False)
    id_campo: Mapped[int] = mapped_column(ForeignKey("CAMPO_ACTUALIZACION.id"), nullable=False)
    producto: Mapped["Producto"] = relationship("Producto", back_populates="actualizaciones")
    tipo: Mapped["TipoActualizacion"] = relationship("TipoActualizacion", back_populates="actualizaciones")
    campo: Mapped["CampoActualizacion"] = relationship("CampoActualizacion", back_populates="actualizaciones")

    def __repr__(self):
        return (f"ActualizacionProducto(id={self.id}, valor={self.valor}, fecha={self.fecha}, "
                f"codigo_producto={self.codigo_producto}, id_tipo={self.id_tipo}, id_campo={self.id_campo})")