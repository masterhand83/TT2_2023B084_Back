import azure.functions as func
from sqlalchemy import select,insert, update;
from .models import RegistroExistencia, Venta,Producto, DetalleVenta;
from sqlalchemy.ext.serializer import loads, dumps;
import json
from .connect import create_session;
def edit_producto_handler(producto = {}):

  session = create_session()
  update_stmt = (
    update(Producto)
    .where(Producto.codigo == producto["codigo"])
    .values(
      nombre = producto["nombre"],
      precio_unitario = producto["precio_unitario"],
      id_marca = producto["marca"],
    )
  )
  session.execute(update_stmt)
  session.commit()
  session.close()
  return True