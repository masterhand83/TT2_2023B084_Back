import azure.functions as func
from sqlalchemy import select, insert, update
from .models import Venta, Producto, DetalleVenta
from sqlalchemy.ext.serializer import loads, dumps
from functools import reduce
import json
from .connect import create_session
# SELECT * FROM DETALLE_VENTA dv;
# SELECT id_venta, SUM(cantidad) AS total_cantidad, SUM(subtotal) AS total FROM DETALLE_VENTA GROUP BY id_venta;

# SELECT
#     v.*,
#     dv.total_cantidad,
#     dv.total
# FROM
#     VENTA v
# LEFT JOIN
#     (SELECT id_venta, SUM(cantidad) AS total_cantidad, SUM(subtotal) AS total FROM DETALLE_VENTA GROUP BY id_venta) dv
# ON
#     v.id  = dv.id_venta;


# SELECT
# 	*
# FROM
# 	PRODUCTO p
# WHERE
# 	p.codigo IN (
# 	SELECT
# 		codigo_producto
# 	FROM
# 		DETALLE_VENTA dv
# 	WHERE
# 		dv.id_venta = '9A1A433E-F36B-1410-8BE6-006A7B6F75A4');
def sumarCantidades(accum, detalle):
    return accum + detalle["cantidad"]
def calcularTotal(accum, detalle):
    return accum + detalle["producto"]["precio_unitario"] * detalle["cantidad"];
def get_ventas_handler():
    session = create_session()
    stmt = select(Venta)
    final_result = []
    result = session.execute(stmt).scalars().all()
    session.commit()
    session.close()
    for r in result:
        venta_items = []
        for dt in r.detalles_venta:
            item = {
                "key": dt.codigo_producto,
                "cantidad": dt.cantidad,
                "producto": dt.producto.as_dict()
            }
            venta_items.append(item)
        cantidad = reduce(sumarCantidades, venta_items, 0)
        total = reduce(calcularTotal, venta_items, 0)

        venta = {
            "id": str(r.id),
            "fecha": str(r.fecha),
            "items":venta_items,
            "cantidad": cantidad,
            "total": total,
        }
        final_result.append(venta)
    return final_result
# declare type VentaItem = {
#   key: string;
#   cantidad: number;
#   producto: Producto;
# }
# declare type Venta = {
#   id: number;
#   fecha: string;
#   items: VentaItem[];
#   cantidad: number;
#   total: number;
# }
