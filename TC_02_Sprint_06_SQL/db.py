import sqlite3
from mimesis import Generic
from mimesis.locales import Locale
import random

dict_querys = {
    "query_create_table_categoria": """CREATE TABLE IF NOT EXISTS categoria (
                                        Id_categoria INTEGER PRIMARY KEY,
                                        Nombre TEXT);""",
    "query_create_table_producto": """CREATE TABLE IF NOT EXISTS producto (
                                        Id_producto INTEGER PRIMARY KEY,
                                        Nombre TEXT,
                                        Precio REAL,
                                        Categoria INTEGER,
                                        FOREIGN KEY (Categoria) REFERENCES categoria(Id_categoria));""",
    "query_create_table_clientes": """CREATE TABLE IF NOT EXISTS clientes (
                                        Id_cliente INTEGER PRIMARY KEY,
                                        Nombre TEXT,
                                        Direccion TEXT);""",
    "query_create_table_ventas": """CREATE TABLE IF NOT EXISTS ventas (
                                        Id_ventas INTEGER PRIMARY KEY,
                                        Producto INTEGER,
                                        Cantidad INTEGER,
                                        Cliente INTEGER,
                                        Precio INTEGER,
                                        Fecha DATETIME,
                                        FOREIGN KEY (Producto) REFERENCES producto(Id_producto),
                                        FOREIGN KEY (Cliente) REFERENCES clientes(Id_cliente));""",
    "query_create_table_proveedor": """CREATE TABLE IF NOT EXISTS proveedor (
                                        Id_proveedor INTEGER PRIMARY KEY,
                                        Nombre TEXT,
                                        Direccion TEXT,
                                        Ciudad TEXT,
                                        Provincia TEXT,
                                        Telefono INTEGER);""",
    "query_create_table_compras": """CREATE TABLE IF NOT EXISTS compras (
                                        Id_compra INTEGER PRIMARY KEY,
                                        Producto INTEGER,
                                        Proveedor INTEGER,
                                        Precio REAL,
                                        Cantidad INTEGER,
                                        Fecha DATETIME,
                                        FOREIGN KEY (Producto) REFERENCES producto(Id_producto),
                                        FOREIGN KEY (Proveedor) REFERENCES proveedor(Id_proveedor));"""
}

productos_por_categoria = {
    "Herramientas manuales": ["Martillo", "Destornillador", "Llave inglesa", "Alicate", "Cúter"],
    "Herramientas eléctricas": ["Taladro", "Amoladora", "Sierra eléctrica", "Pulidora"],
    "Pinturas": ["Pintura Latex", "Esmalte sintético", "Barniz", "Rodillo", "Brocha"],
    "Fontanería": ["Llave de paso", "Tubo PVC", "Codo PVC", "Sellador"],
    "Electricidad": ["Interruptor", "Cable eléctrico", "Regleta", "Enchufe"],
    "Tornillería": ["Tornillos", "Tuercas", "Arandelas", "Tacos"],
    "Construcción": ["Cemento", "Yeso", "Arena", "Ladrillos"]
}

g = Generic(locale=Locale.IT)

def add_cliente(cliente):
    query = '''INSERT INTO clientes(Nombre, Direccion)
                VALUES(?,?)'''
    
    cursor.execute(query, cliente)    
    
    connection.commit()
    
def add_proveedor(proveedor):
    query = '''INSERT INTO proveedor(Nombre, Direccion, Ciudad, Provincia, Telefono)
                VALUES(?,?,?,?,?)'''
    
    cursor.execute(query, proveedor)    
    
    connection.commit()
    
def add_categoria(categoria):
    query = '''INSERT INTO categoria(Nombre)
                VALUES(?)'''
    
    cursor.execute(query, categoria)    
    
    connection.commit()
    
def add_producto(producto):
    query = '''INSERT INTO producto(Nombre, Precio, Categoria)
                VALUES(?,?,?)'''
    
    cursor.execute(query, producto)    
    
    connection.commit()
    
def add_compra(compra):
    query = '''INSERT INTO compras(Producto, Proveedor, Precio, Cantidad, Fecha)
                VALUES(?,?,?,?,?)'''
    
    cursor.execute(query, compra)    
    
    connection.commit()
    
    
def add_venta(venta):
    query = '''INSERT INTO ventas(Producto, Cantidad, Cliente, Precio, Fecha)
                VALUES(?,?,?,?,?)'''
    
    cursor.execute(query, venta)    
    
    connection.commit()

connection = sqlite3.connect("base_de_datos_ferreteria.db")

cursor = connection.cursor()

for query in dict_querys.values():
    cursor.execute(query)
    
connection.commit()

# ---------------------- CATEGORIAS ----------------------

for key in productos_por_categoria.keys():
    add_categoria((key,))

# ---------------------- PRODUCTO ----------------------
cursor.execute("SELECT Id_categoria FROM categoria")
categorias_ids = [row[0] for row in cursor.fetchall()]

for id_cat, productos in zip(categorias_ids, productos_por_categoria.values()):
    for producto in productos:
        add_producto((producto, g.finance.price(), id_cat))

# ---------------------- CLIENTE ----------------------
for id_cli in range(20):
    add_cliente((g.person.full_name(), g.address.address()))
    
# ---------------------- PROVEEDOR ----------------------
for id_cli in range(20):
    add_proveedor((g.finance.company(), g.address.address(), g.address.city(), g.address.province(), g.person.phone_number()))

# ---------------------- COMPRA ----------------------
cursor.execute("SELECT Id_producto, Precio FROM producto")
productos = [row for row in cursor.fetchall()]
cursor.execute("SELECT Id_proveedor FROM proveedor")
proveedor_ids = [row[0] for row in cursor.fetchall()]


for compra in range(20):
    pro = random.choice(productos)
    provee = random.choice(proveedor_ids)
    cantidad = random.randint(1,10)
    add_compra((pro[0], random.choice(proveedor_ids), pro[1] * cantidad, cantidad, g.datetime.datetime(2025, 2025)))

# ---------------------- VENTA ----------------------
import random

cursor.execute("SELECT Id_producto, Precio FROM producto")
productos = [row for row in cursor.fetchall()]
cursor.execute("SELECT Id_cliente FROM clientes")
clientes_ids = [row[0] for row in cursor.fetchall()]


for compra in range(20):
    pro = random.choice(productos)
    provee = random.choice(clientes_ids)
    cantidad = random.randint(1,10)
    add_venta((pro[0], cantidad, random.choice(clientes_ids), pro[1] * cantidad, g.datetime.datetime(2025, 2025)))
    
connection.close()