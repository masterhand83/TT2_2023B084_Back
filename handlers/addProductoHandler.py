import azure.functions as func
from sqlalchemy import select,insert, update;
from .models import RegistroExistencia, Venta,Producto, DetalleVenta;
from sqlalchemy.ext.serializer import loads, dumps;
import json
from .connect import create_session;
# declare type Producto = {
#   key: string;
#   codigo: string;
#   nombre: string;
#   marca: string;
#   stock: number;
#   precio: number;
# };
def add_producto_handler(producto = {}):
  session = create_session()
  stmt1 = insert(Producto).values(
    codigo = producto["codigo"],
    nombre = producto["nombre"],
    precio_unitario = producto["precio"],
    existencias = producto["stock"],
    descripcion = "placeholder",
    id_marca = producto["marca"],
    activo = True
  )
  session.execute(stmt1)
  add_stock_history = (
    insert(RegistroExistencia)
    .values(
      codigo_producto = producto["codigo"],
      existencia = producto["stock"],
    )
  )
  session.execute(add_stock_history)
  session.commit()
  session.close()
  return True