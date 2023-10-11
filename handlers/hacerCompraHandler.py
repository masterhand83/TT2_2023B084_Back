import azure.functions as func
from sqlalchemy import select,insert, update;
from .models import Venta,Producto, DetalleVenta;
from sqlalchemy.ext.serializer import loads, dumps;
import json
from .connect import create_session;
def hacer_compra_handler(lista_compras = []):
  listaMapeada = []
  session = create_session()
  stmt1 = insert(Venta)
  print(stmt1)
  venta_result = session.execute(stmt1)
  ventakey = venta_result.inserted_primary_key[0]

  for compra in lista_compras:
    find_producto = select(Producto).where(Producto.codigo == compra["key"]);
    producto = session.execute(find_producto).scalars().first();
    listaMapeada.append({
      "id_venta": ventakey,
      "codigo_producto": compra["key"],
      "cantidad": compra["cantidad"],
      "subtotal": compra["cantidad"] * producto.precio_unitario
    })
  stmt2 = insert(DetalleVenta).values(listaMapeada)
  session.execute(stmt2)
  print(stmt2)
  for compra in lista_compras:
    stmt3 = update(Producto).where(Producto.codigo == compra["key"]).values(existencias = Producto.existencias - compra["cantidad"])
    print(stmt3)
    session.execute(stmt3)
  session.commit()
  session.close()
  return True