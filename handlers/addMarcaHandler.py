import azure.functions as func
from sqlalchemy import select,insert, update;
from .models import Venta,Marca,Producto, DetalleVenta, RegistroExistencia;
from sqlalchemy.ext.serializer import loads, dumps;
import json
from .connect import create_session;
def add_marca_handler(nombreMarca = ""):
  session = create_session()
  stmt = (
    insert(Marca)
    .values(
      marca=nombreMarca
    )
  )
  session.execute(stmt)
  session.commit()
  session.close()
  return True