import azure.functions as func
from sqlalchemy import select, insert, update
from .models import Venta, Producto, DetalleVenta, RegistroMerma
from sqlalchemy.ext.serializer import loads, dumps
import json
from .connect import create_session


def remove_stock_handler(entrada={}):
    session = create_session()
    codigo = entrada["codigo"]
    merma = entrada["merma"]
    get_producto_stmt = select(Producto).where(Producto.codigo == codigo)
    producto = session.execute(get_producto_stmt).scalars().first()
    existencias_actual = producto.existencias
    if existencias_actual < merma:
        print("No es posible remover existencias mayores a las actuales")
        return False
    stmt = (
        update(Producto).
        where(Producto.codigo == codigo).
        values(existencias=Producto.existencias - merma)
    )
    session.execute(stmt)
    add_mermas_stmt = (
        insert(RegistroMerma).values(
            codigo_producto=codigo,
            merma=merma,
        )
    )
    session.execute(add_mermas_stmt)
    session.commit()
    session.close()
    return True
