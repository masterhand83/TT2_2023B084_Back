import azure.functions as func
from sqlalchemy import select,insert, update;
from .models import Venta,Producto, DetalleVenta, RegistroExistencia;
from sqlalchemy.ext.serializer import loads, dumps;
import json
from .connect import create_session;
def desactivar_producto_handler(codigo = ""):
  session = create_session()
  disable_stmt = (
    update(Producto)
    .where(Producto.codigo == codigo)
    .values(activo=False)
  )
  session.execute(disable_stmt);
  session.commit()
  session.close()
  return True