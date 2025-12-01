CREATE TABLE `proveedor` (
  `Id_proveedor` integer PRIMARY KEY,
  `Nombre` varchar(255),
  `Direccion` varchar(255),
  `Ciudad` varchar(255),
  `Provincia` varchar(255),
  `Telefono` integer
);

CREATE TABLE `producto` (
  `Id_producto` integer PRIMARY KEY,
  `Nombre` varchar(255),
  `Precio` float,
  `Categoria` integer
);

CREATE TABLE `ventas` (
  `Id_ventas` integer PRIMARY KEY,
  `Producto` varchar(255),
  `Cantidad` integer,
  `Cliente` varchar(255),
  `Precio` integer,
  `Fecha` datetime
);

CREATE TABLE `compras` (
  `Id_compra` integer PRIMARY KEY,
  `Producto` varchar(255),
  `Proveedor` varchar(255),
  `Precio` integer,
  `Cantidad` integer,
  `Fecha` datetime
);

CREATE TABLE `categoria` (
  `Id_categoria` integer PRIMARY KEY,
  `Nombre` varchar(255)
);

CREATE TABLE `clientes` (
  `Id_cliente` integer PRIMARY KEY,
  `Nombre` varchar(255),
  `Direccion` varchar(255)
);

ALTER TABLE `ventas` ADD FOREIGN KEY (`Producto`) REFERENCES `producto` (`Id_producto`);

ALTER TABLE `producto` ADD FOREIGN KEY (`Categoria`) REFERENCES `categoria` (`Id_categoria`);

ALTER TABLE `ventas` ADD FOREIGN KEY (`Cliente`) REFERENCES `clientes` (`Id_cliente`);

ALTER TABLE `compras` ADD FOREIGN KEY (`Proveedor`) REFERENCES `proveedor` (`Id_proveedor`);

ALTER TABLE `compras` ADD FOREIGN KEY (`Producto`) REFERENCES `producto` (`Id_producto`);
