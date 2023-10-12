import azure.functions as func
import logging
import json
from handlers.getProductoListHandler import get_producto_list_handler;
from handlers.hacerCompraHandler import hacer_compra_handler;
from handlers.getVentasListHandler import get_ventas_handler;
from handlers.addProductoHandler import add_producto_handler;
from handlers.addStockHandler import add_stock_handler;
from handlers.removeStockHandler import remove_stock_handler;
from handlers.desactivarProductoHandler import desactivar_producto_handler;


app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)


@app.route(route="get-lista-productos", methods=["GET"])
def get_producto(req: func.HttpRequest) -> func.HttpResponse:
    return get_producto_list_handler(req)

@app.route(route="get-lista-ventas", methods=["GET"])
def get_ventas(req: func.HttpRequest) -> func.HttpResponse:
    result = get_ventas_handler();
    return func.HttpResponse(
        json.dumps(result),
        headers={"Content-Type": "application/json"},
        mimetype="application/json",
        charset="utf-8",
    )


# {
#     "codigo": "123",
#     "newstock": 5,
# }
@app.route(route="desactivar-producto", methods=["POST"])
def desactivar_producto(req: func.HttpRequest) -> func.HttpResponse:
    text_body = req.get_body().decode()
    dictionary_body = json.loads(text_body)
    result = desactivar_producto_handler(dictionary_body["codigo"])
    return func.HttpResponse(
        status_code=200
    )

# {
#     "codigo": "123",
#     "merma": 100,
# }
@app.route(route="remove-stock", methods=["POST"])
def remove_stock(req: func.HttpRequest) -> func.HttpResponse:
    text_body = req.get_body().decode()
    dictionary_body = json.loads(text_body)
    result = remove_stock_handler(dictionary_body)
    return func.HttpResponse(
        status_code=200
    )


# {
#     "codigo": "123",
#     "newstock": 100,
# }
@app.route(route="add-stock", methods=["POST"])
def add_stock(req: func.HttpRequest) -> func.HttpResponse:
    text_body = req.get_body().decode()
    dictionary_body = json.loads(text_body)
    result = add_stock_handler(dictionary_body)
    return func.HttpResponse(
        status_code=200
    )
# {
#     "key": "1234",
#     "codigo": "123",
#     "nombre": "producto por añadir 3",
#     "marca": 1,
#     "stock": 123,
#     "precio": 500.05
# }
@app.route(route="add-producto", methods=["POST"])
def add_producto(req: func.HttpRequest) -> func.HttpResponse:
    text_body = req.get_body().decode()
    dictionary_body = json.loads(text_body)
    result = add_producto_handler(dictionary_body)
    return func.HttpResponse(
        status_code=200
    )
# [
#   {
#     "key": "PROD003",
#     "cantidad": 2,
#     "producto": {
#       "key": "PROD003",
#       "codigo": "PROD001",
#       "nombre": "Producto 1",
#       "marca": "Marca 1",
#       "stock": 10,
#       "precio": 100
#     }
#   },
#   {
#     "key": "PROD004",
#     "cantidad": 2,
#     "producto": {
#       "key": "PROD004",
#       "codigo": "PROD001",
#       "nombre": "Producto 1",
#       "marca": "Marca 1",
#       "stock": 10,
#       "precio": 100
#     }
#   }
# ]
@app.route(route="hacer-compra", methods=["POST"])
def hacer_compra(req: func.HttpRequest) -> func.HttpResponse:
    text_body = req.get_body().decode()
    dictionary_body = json.loads(text_body)
    result = hacer_compra_handler(dictionary_body)
    return func.HttpResponse(
        status_code=200
    )


@app.route(route="hacer-compra", methods=["POST"])
def hacer_compra(req: func.HttpRequest) -> func.HttpResponse:
    text_body = req.get_body().decode()
    dictionary_body = json.loads(text_body)
    result = hacer_compra_handler(dictionary_body)
    return func.HttpResponse(
        status_code=200
    )
@app.route(route="tt-backend")
def tt_backend(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
            "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
            status_code=200
        )
