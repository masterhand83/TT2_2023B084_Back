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
        lista.append(d.as_dict())
    session.close()
    return func.HttpResponse(
        json.dumps(lista),
        headers={"Content-Type": "application/json"},
        mimetype="application/json",
        charset="utf-8",
    )
