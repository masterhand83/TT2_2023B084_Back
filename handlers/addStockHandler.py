import azure.functions as func
from sqlalchemy import select,insert, update;
from .models import Venta,Producto, DetalleVenta;
from sqlalchemy.ext.serializer import loads, dumps;
import json
from .connect import create_session;
def add_stock_handler(entrada = {}):
  session = create_session()
  codigo = entrada["codigo"];
  newstock = entrada["newstock"];
  stmt = (
    update(Producto).
    where(Producto.codigo == codigo).
    values(existencias = Producto.existencias + newstock)
  )
  session.execute(stmt)
  session.commit()
  session.close()
  return True