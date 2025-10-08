create database mitienda3;
use mitienda3;
CREATE TABLE articulo_de_carrito (
ID INT primary key auto_increment,
FOREIGN KEY (articulo_de_carrito) REFERENCES ID_producto(ID),
producto varchar(20),
cantidad varchar (20) ,
ID_producto INT
);

CREATE TABLE productos (
ID INT primary key auto_increment,
nombre varchar(20),
descripcion varchar (20) ,
precio float,
image varchar(150),
cantidad INT
 );
CREATE TABLE usuario(
ID INT primary key auto_increment,
primer_nombre varchar(20),
correo_Electronico varchar (20) unique,
contrasena DATE
);
CREATE DATABASE mitienda3;
USE mitienda3;
SELECT
    P.nombre AS Producto,
    SUM(C.cantidad) AS Cantidad_Total_Vendida,
    SUM(P.precio * C.cantidad) AS Valor_Total_en_Carritos
FROM
    articulo_de_carrito AS C
JOIN
    productos AS P ON C.ID_producto = P.ID
GROUP BY
    P.nombre
ORDER BY
    Valor_Total_en_Carritos DESC;
CREATE TABLE productos (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(50) NOT NULL,
    descripcion VARCHAR(255),
    precio DECIMAL(10, 2) NOT NULL,
    imagen VARCHAR(255),
    cantidad INT NOT NULL
);

CREATE TABLE usuarios (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    primer_nombre VARCHAR(50) NOT NULL,
    correo_Electronico VARCHAR(100) UNIQUE NOT NULL,
    contrasena VARCHAR(255) NOT NULL
);

CREATE TABLE articulo_de_carrito (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    ID_usuario INT NOT NULL,
    ID_producto INT NOT NULL,
    cantidad INT NOT NULL,
    FOREIGN KEY (ID_usuarios) REFERENCES usuarios(ID),
    FOREIGN KEY (ID_producto) REFERENCES productos(ID)
);

INSERT INTO productos (nombre, descripcion, precio, imagen, cantidad) VALUES
('Laptop Pro', 'Portátil potente y ligero', 1250.00, 'img/laptop-pro.jpg', 15),
('Mouse Ergo', 'Ratón ergonómico inalámbrico', 25.99, 'img/mouse-ergo.jpg', 50),
('Teclado Mecánico', 'Teclado RGB con switches azules', 85.50, 'img/teclado-mecanico.jpg', 30),
('Monitor 27p 4K', 'Monitor LED 4K de 27 pulgadas', 450.00, 'img/monitor-4k.jpg', 10),
('Webcam HD', 'Cámara web con enfoque automático', 49.99, 'img/webcam-hd.jpg', 40),
('Disco SSD 1TB', 'Unidad de estado sólido 1TB', 99.95, 'img/ssd-1tb.jpg', 25),
('Audífonos BT', 'Auriculares inalámbricos con cancelación', 110.00, 'img/audifonos-bt.jpg', 35),
('Router WiFi 6', 'Router de alta velocidad WiFi 6', 150.00, 'img/router-wifi6.jpg', 20),
('Impresora Laser', 'Impresora láser monocromática', 199.90, 'img/impresora-laser.jpg', 5),
('Smartwatch S3', 'Reloj inteligente deportivo', 180.00, 'img/smartwatch-s3.jpg', 22),
('Cable HDMI 2m', 'Cable HDMI 2.1 de 2 metros', 12.50, 'img/cable-hdmi.jpg', 100),
('Power Bank 20K', 'Batería externa de 20000mAh', 35.75, 'img/powerbank.jpg', 60),
('Funda Laptop 15"', 'Funda protectora para portátiles 15"', 18.00, 'img/funda-laptop.jpg', 80),
('Tablet Android', 'Tablet de 10 pulgadas, 128GB', 299.99, 'img/tablet-android.jpg', 12),
('Hub USB-C 7en1', 'Adaptador USB-C con múltiples puertos', 55.00, 'img/hub-usbc.jpg', 45),
('Micrófono Cond.', 'Micrófono de condensador para streaming', 75.00, 'img/microfono-cond.jpg', 18),
('Lámpara Escritorio', 'Lámpara LED de escritorio regulable', 30.50, 'img/lampara-led.jpg', 55),
('Silla Gamer', 'Silla ergonómica para videojuegos', 280.00, 'img/silla-gamer.jpg', 8),
('Tarjeta Gráfica', 'GPU de alto rendimiento, 8GB VRAM', 550.00, 'img/gpu-8gb.jpg', 7),
('Ventilador USB', 'Mini ventilador portátil USB', 10.99, 'img/ventilador-usb.jpg', 90);

INSERT INTO usuarios (primer_nombre, correo_Electronico, contrasena) VALUES
('Andrea', 'andrea.m@mail.com', '$2a$10$hashedpasswordA'),
('Carlos', 'carlos.r@mail.com', '$2a$10$hashedpasswordB'),
('Sofía', 'sofia.g@mail.com', '$2a$10$hashedpasswordC'),
('Javier', 'javier.p@mail.com', '$2a$10$hashedpasswordD'),
('Daniela', 'daniela.z@mail.com', '$2a$10$hashedpasswordE'),
('Ricardo', 'ricardo.s@mail.com', '$2a$10$hashedpasswordF'),
('Lucía', 'lucia.t@mail.com', '$2a$10$hashedpasswordG'),
('Miguel', 'miguel.h@mail.com', '$2a$10$hashedpasswordH'),
('Elena', 'elena.a@mail.com', '$2a$10$hashedpasswordI'),
('Fernando', 'fernando.q@mail.com', '$2a$10$hashedpasswordJ');

INSERT INTO articulo_de_carrito (ID_usuario, ID_producto, cantidad) VALUES
(1, 1, 1), (1, 2, 2), (1, 5, 1), (1, 11, 3), (1, 19, 1), (1, 20, 5),
(2, 3, 1), (2, 4, 1), (2, 10, 1), (2, 12, 2), (2, 14, 1), (2, 16, 1),
(3, 1, 1), (3, 5, 2), (3, 7, 1), (3, 9, 1), (3, 11, 1), (3, 13, 4), (3, 15, 1),
(4, 2, 1), (4, 4, 1), (4, 6, 1), (4, 8, 1), (4, 10, 1), (4, 12, 1), (4, 14, 1),
(5, 1, 1), (5, 3, 2), (5, 5, 1), (5, 7, 1), (5, 9, 1), (5, 11, 2), (5, 13, 1),
(6, 2, 1), (6, 4, 1), (6, 6, 1), (6, 8, 1), (6, 10, 1), (6, 12, 1), (6, 14, 1), (6, 16, 1), (6, 18, 1),
(7, 1, 1), (7, 3, 1), (7, 5, 1), (7, 7, 1), (7, 9, 1), (7, 11, 1), (7, 13, 1), (7, 15, 1), (7, 17, 1), (7, 19, 1),
(8, 2, 3), (8, 4, 1), (8, 6, 1), (8, 8, 1), (8, 10, 1), (8, 12, 1), (8, 14, 1), (8, 16, 1), (8, 18, 1), (8, 20, 2),
(9, 1, 2), (9, 3, 1), (9, 5, 1), (9, 7, 1), (9, 9, 1), (9, 11, 1), (9, 13, 1),
(10, 15, 1), (10, 17, 1), (10, 19, 1), (10, 20, 1);
