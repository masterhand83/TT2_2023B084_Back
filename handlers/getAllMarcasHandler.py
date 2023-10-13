import azure.functions as func
from sqlalchemy import select;
from .models import Producto, Marca;
from sqlalchemy.ext.serializer import loads, dumps;
import json
from .connect import create_session;
def marca_as_dict(marca: Marca):
    return marca.as_dict()
def get_all_marcas_handler() -> func.HttpResponse:
    lista = []
    session = create_session()
    statement = select(Marca)
    data = session.scalars(statement).all()
    print(data)

    for d in data:
        lista.append(d.as_dict())
    session.close()
    return lista
