import azure.functions as func
from sqlalchemy import select;
from .models import Producto;
from sqlalchemy.ext.serializer import loads, dumps;
import json
from .connect import create_session;
def get_producto_list_handler(req: func.HttpRequest) -> func.HttpResponse:
    lista = []
    session = create_session()
    statement = select(Producto)
    data = session.scalars(statement).all()
    for d in data:
        print(d.marca)
        d_dict = {
            "codigo": d.codigo,
            "nombre": d.nombre,
            "precio_unitario": float(d.precio_unitario),
            "existencias": d.existencias,
            "descripcion": d.descripcion,
            "marca": d.marca.marca,
            "activo": d.activo
        }
        lista.append(d.as_dict())
    session.close()
    print(lista)
    return func.HttpResponse(
        json.dumps(lista),
        headers={"Content-Type": "application/json"},
        mimetype="application/json",
        charset="utf-8",
    )
