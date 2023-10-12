import azure.functions as func
from sqlalchemy import select,insert, update;
from .models import Venta,Producto, DetalleVenta, RegistroExistencia;
from sqlalchemy.ext.serializer import loads, dumps;
import json
from .connect import create_session;
def add_stock_handler(entrada = {}):
  session = create_session()
  codigo = entrada["codigo"];
  newstock = entrada["newstock"];
  get_producto_stmt = (
    select(Producto).
    where(Producto.codigo == codigo)
  )
  producto = session.execute(get_producto_stmt).scalars().first()
  cantidad_actual = producto.existencias
  stmt = (
    update(Producto).
    where(Producto.codigo == codigo).
    values(existencias = Producto.existencias + newstock)
  )
  session.execute(stmt)
  update_historial_stock_stmt = (
    insert(RegistroExistencia)
    .values(
      codigo_producto = codigo,
      existencia = cantidad_actual + newstock,
    )
  )
  session.execute(update_historial_stock_stmt);
  session.commit()
  session.close()
  return True