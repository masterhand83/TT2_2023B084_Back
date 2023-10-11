import azure.functions as func
import logging
import json
from handlers.getProductoListHandler import get_producto_list_handler;
from handlers.hacerCompraHandler import hacer_compra_handler;
from handlers.getVentasListHandler import get_ventas_handler;


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
