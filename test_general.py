import pytest
from handlers.hacerCompraHandler import hacer_compra_handler;
from handlers.getVentasListHandler import get_ventas_handler;
from handlers.addProductoHandler import add_producto_handler;
from handlers.addStockHandler import add_stock_handler;
from handlers.removeStockHandler import remove_stock_handler;

def sum(a, b):
  return a + b;
# declare type Producto = {
#   key: string;
#   codigo: string;
#   nombre: string;
#   marca: string;
#   stock: number;
#   precio: number;
# };
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

def test_hacer_compra():
  remove_stock_handler({
    "codigo": "PROD001",
    "merma": 100,
  })

  # print(get_ventas_handler())
  assert True

test_hacer_compra()