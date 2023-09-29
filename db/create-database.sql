CREATE DATABASE [tt_database]
GO

USE [tt_database];
GO

CREATE TABLE MARCA
(
    id SMALLINT IDENTITY(1,1) NOT NULL,
    marca VARCHAR(50) NOT NULL,
    PRIMARY KEY (id)
);
GO

-- Definición de la tabla PRODUCTO
CREATE TABLE PRODUCTO
(
    codigo VARCHAR(20) NOT NULL,
    precio_unitario DECIMAL(8, 2) NOT NULL,
    existencias SMALLINT NOT NULL,
    nombre VARCHAR(80) NOT NULL,
    descripcion VARCHAR(200) NOT NULL,
    id_marca SMALLINT NOT NULL,
    activo BIT NOT NULL,
    PRIMARY KEY (codigo),
    FOREIGN KEY (id_marca) REFERENCES MARCA(id)
);
GO

-- Definición de la tabla VENTA
CREATE TABLE VENTA
(
    id UNIQUEIDENTIFIER NOT NULL DEFAULT NEWSEQUENTIALID(),
    fecha SMALLDATETIME NOT NULL DEFAULT GETDATE(),
    PRIMARY KEY (id)
);
GO

-- Definición de la tabla DETALLE_VENTA
CREATE TABLE DETALLE_VENTA
(
    id INT IDENTITY(1,1) NOT NULL,
    cantidad SMALLINT NOT NULL,
    codigo_producto VARCHAR(20) NOT NULL,
    id_venta UNIQUEIDENTIFIER NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (codigo_producto) REFERENCES PRODUCTO(codigo),
    FOREIGN KEY (id_venta) REFERENCES VENTA(id)
);
GO

-- Definición de la tabla TIPO_ACTUALIZACION
CREATE TABLE TIPO_ACTUALIZACION
(
    id TINYINT IDENTITY(1,1) NOT NULL,
    tipo CHAR(20) NOT NULL,
    PRIMARY KEY (id)
);
GO
-- Definición de la tabla CAMPO_ACTUALIZACION
CREATE TABLE CAMPO_ACTUALIZACION
(
    id TINYINT IDENTITY(1,1) NOT NULL,
    campo CHAR(15) NOT NULL,
    PRIMARY KEY (id)
);
GO
-- Definición de la tabla ACTUALIZACION_PRODUCTO
CREATE TABLE ACTUALIZACION_PRODUCTO
(
    id INT IDENTITY(1,1) NOT NULL,
    valor VARCHAR(200) NOT NULL,
    fecha SMALLDATETIME NOT NULL,
    codigo_producto VARCHAR(20) NOT NULL,
    id_tipo TINYINT NOT NULL,
    id_campo TINYINT NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (codigo_producto) REFERENCES PRODUCTO(codigo),
    FOREIGN KEY (id_tipo) REFERENCES TIPO_ACTUALIZACION(id),
    FOREIGN KEY (id_campo) REFERENCES CAMPO_ACTUALIZACION(id)
);
GO

INSERT INTO MARCA (marca) VALUES ('OfficeMaster');
INSERT INTO MARCA (marca) VALUES ('PaperTech');
INSERT INTO MARCA (marca) VALUES ('StationX');
INSERT INTO MARCA (marca) VALUES ('DeskPro');
INSERT INTO MARCA (marca) VALUES ('SupplyPlus');
INSERT INTO MARCA (marca) VALUES ('InkMasters');
INSERT INTO MARCA (marca) VALUES ('ErgoElite');
INSERT INTO MARCA (marca) VALUES ('FileWise');
INSERT INTO MARCA (marca) VALUES ('WriteRight');
INSERT INTO MARCA (marca) VALUES ('OfficeSolutions');
INSERT INTO MARCA (marca) VALUES ('TechNest');
INSERT INTO MARCA (marca) VALUES ('PaperFlow');
INSERT INTO MARCA (marca) VALUES ('DeskCraft');
INSERT INTO MARCA (marca) VALUES ('WorkWiz');
INSERT INTO MARCA (marca) VALUES ('EcoDesk');
INSERT INTO MARCA (marca) VALUES ('InkFlow');
INSERT INTO MARCA (marca) VALUES ('ErgoPro');
INSERT INTO MARCA (marca) VALUES ('FileSmart');
INSERT INTO MARCA (marca) VALUES ('WriteEase');
INSERT INTO MARCA (marca) VALUES ('OfficeGenius');
GO
INSERT INTO PRODUCTO (codigo, precio_unitario, existencias, nombre, descripcion, id_marca, activo)
VALUES ('PROD001', 49.99, 100, 'Teclado Inalámbrico', 'Teclado inalámbrico ergonómico con teclas silenciosas.', 1, 1);

INSERT INTO PRODUCTO (codigo, precio_unitario, existencias, nombre, descripcion, id_marca, activo)
VALUES ('PROD002', 299.99, 50, 'Monitor 27" Full HD', 'Monitor de 27 pulgadas con resolución Full HD y bordes delgados.', 2, 1);

INSERT INTO PRODUCTO (codigo, precio_unitario, existencias, nombre, descripcion, id_marca, activo)
VALUES ('PROD003', 14.99, 200, 'Mouse Óptico', 'Mouse óptico con diseño ergonómico y 3 botones.', 3, 1);

INSERT INTO PRODUCTO (codigo, precio_unitario, existencias, nombre, descripcion, id_marca, activo)
VALUES ('PROD004', 99.99, 30, 'Impresora Multifuncional', 'Impresora multifuncional a color con escáner y conectividad Wi-Fi.', 4, 1);

INSERT INTO PRODUCTO (codigo, precio_unitario, existencias, nombre, descripcion, id_marca, activo)
VALUES ('PROD005', 19.99, 150, 'Calculadora Científica', 'Calculadora científica con pantalla LCD y funciones avanzadas.', 5, 1);

INSERT INTO PRODUCTO (codigo, precio_unitario, existencias, nombre, descripcion, id_marca, activo)
VALUES ('PROD006', 39.99, 80, 'Mochila Portátil', 'Mochila para portátil de 15 pulgadas con compartimentos organizadores.', 6, 1);

INSERT INTO PRODUCTO (codigo, precio_unitario, existencias, nombre, descripcion, id_marca, activo)
VALUES ('PROD007', 9.99, 250, 'Bolígrafos Azules (Paquete de 10)', 'Bolígrafos de tinta azul ideales para tomar notas.', 7, 1);

INSERT INTO PRODUCTO (codigo, precio_unitario, existencias, nombre, descripcion, id_marca, activo)
VALUES ('PROD008', 69.99, 40, 'Silla de Oficina Ergonómica', 'Silla de oficina ergonómica con soporte lumbar y ajustes de altura.', 8, 1);

INSERT INTO PRODUCTO (codigo, precio_unitario, existencias, nombre, descripcion, id_marca, activo)
VALUES ('PROD009', 24.99, 120, 'Alfombrilla de Ratón', 'Alfombrilla de ratón con superficie suave y base antideslizante.', 9, 1);

INSERT INTO PRODUCTO (codigo, precio_unitario, existencias, nombre, descripcion, id_marca, activo)
VALUES ('PROD010', 149.99, 25, 'Escritorio de Oficina', 'Escritorio de oficina con cajones y espacio para computadora.', 10, 1);
GO