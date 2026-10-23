-- Esquema de la BD "Inventario ligero para Pymes"
-- Basado en el dump de MySQL 8.0.46 del 2026-10-15.
-- Compatible con MySQL 8.0.16+ y MariaDB 10.4+ (los CHECK necesitan esas versiones).
--
-- Uso:  mysql -u root -p < inventario_pymes.sql
--
-- OJO: este script BORRA las tablas y sus datos si ya existen (DROP TABLE).
-- No reimportar sobre una BD con datos que se quieran conservar.

-- create data base es el comadno que crea la db si es que no existe, si ya existe no hace nada. esto cn (if not exists y si no existe la crea con el nombre de la base de datos, si ya existe no hace nada.)
CREATE DATABASE IF NOT EXISTS `inventario_pymes`
  DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci; -- Guarda el texto usando UTF-8 completo (hasta 4 bytes), para que pueda almacenar letras especiales, idiomas y emojis sin errores.
USE `inventario_pymes`; -- cmo la db esta en cada equipo "use" hace que se seleccione esta db para que los siguientes comandos se ejecuten en esta.

SET NAMES utf8mb4;
SET @OLD_FOREIGN_KEY_CHECKS = @@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS `movimientos`;
DROP TABLE IF EXISTS `productos`;

--
-- Tabla productos
-- activo = 0 es un producto dado de baja (HU-03). No se borra porque
-- la FK de movimientos impide el DELETE si tiene historial.
--

CREATE TABLE `productos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `sku` varchar(50) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `categoria` varchar(100) DEFAULT NULL,
  `stock_actual` int NOT NULL DEFAULT 0,
  `stock_minimo` int NOT NULL DEFAULT 0,
  `activo` tinyint(1) NOT NULL DEFAULT 1,
  PRIMARY KEY (`id`),
  UNIQUE KEY `sku` (`sku`),
  CONSTRAINT `chk_stock_actual` CHECK (`stock_actual` >= 0),
  CONSTRAINT `chk_stock_minimo` CHECK (`stock_minimo` >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Tabla movimientos
--

CREATE TABLE `movimientos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `producto_id` int NOT NULL,
  `tipo` enum('entrada','salida') NOT NULL,
  `cantidad` int NOT NULL,
  `fecha` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_producto_fecha` (`producto_id`, `fecha`),
  CONSTRAINT `movimientos_ibfk_1` FOREIGN KEY (`producto_id`) REFERENCES `productos` (`id`),
  CONSTRAINT `chk_cantidad` CHECK (`cantidad` > 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

SET FOREIGN_KEY_CHECKS = @OLD_FOREIGN_KEY_CHECKS;

--
-- Datos de prueba para la demo y las pruebas
--   SKU-002: stock 5, para el CA de HU-06 (sacar 8 debe fallar)
--   SKU-003: stock bajo el mínimo, para HU-08
--   SKU-004: stock igual al mínimo, también debe avisar (HU-08 usa <=)
--   Las tildes sirven para probar el CSV de HU-10 en Excel
--

INSERT INTO `productos` (`sku`, `nombre`, `categoria`, `stock_actual`, `stock_minimo`) VALUES
  ('SKU-001', 'Arroz grado 1 1kg',      'Abarrotes', 20,  5),
  ('SKU-002', 'Café molido 250g',       'Abarrotes',  5,  3),
  ('SKU-003', 'Detergente líquido 3L',  'Limpieza',   2,  4),
  ('SKU-004', 'Cuaderno universitario', 'Librería',  10, 10);
