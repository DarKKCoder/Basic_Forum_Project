CREATE DATABASE foro_db;
USE foro_db;

CREATE TABLE usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    correo VARCHAR(150) UNIQUE NOT NULL,
    contraseña VARCHAR(255) NOT NULL,
    rol VARCHAR(50) NOT NULL
);
CREATE TABLE foros (
    id_foro INT AUTO_INCREMENT PRIMARY KEY,
    id_autor INT NOT NULL,
    nombre_foro VARCHAR(100) DEFAULT 'General',
    descripcion TEXT,
    FOREIGN KEY (id_autor) REFERENCES usuarios(id_usuario)
);
CREATE TABLE fechas (
    id_fecha INT AUTO_INCREMENT PRIMARY KEY,
    dia INT NOT NULL,
    mes INT NOT NULL,
    anio INT NOT NULL,
    hora TIME
);
CREATE TABLE comentarios (
    id_comentario INT AUTO_INCREMENT PRIMARY KEY,
    id_autor INT NOT NULL,
    id_foro INT NOT NULL,
    contenido TEXT NOT NULL,
    id_fecha INT NOT NULL,
    activo BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (id_autor) REFERENCES usuarios(id_usuario),
    FOREIGN KEY (id_foro) REFERENCES foros(id_foro),
    FOREIGN KEY (id_fecha) REFERENCES fechas(id_fecha)
);
CREATE TABLE foros_privados (
    id_foro_privado INT PRIMARY KEY,
    FOREIGN KEY (id_foro_privado) REFERENCES foros(id_foro)
);
CREATE TABLE whitelist_foros_privados (
    id_whitelist INT AUTO_INCREMENT PRIMARY KEY,
    id_foro_privado INT NOT NULL,
    id_usuario INT NOT NULL,
    FOREIGN KEY (id_foro_privado) REFERENCES foros_privados(id_foro_privado),
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
);
