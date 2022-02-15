CREATE DATABASE youtube;

use youtube;

CREATE TABLE Users( nombreCompleto varchar(255) not null, nombreUsuario varchar(255) not null, correoElectronico varchar(255) not null, contrasena varchar(255) not null, fraseRecuperacion varchar(255) not null, iniciosIncorrectos int not null, primary key(nombreUsuario) );

CREATE TABLE Tokens( idToken int auto_increment, nombreUsuario varchar(255) not null, token varchar(255) not null, PRIMARY KEY(idToken), FOREIGN KEY (nombreUsuario) REFERENCES Users(nombreUsuario) ON DELETE CASCADE );

CREATE TABLE Videos( idVideo int auto_increment, nombreUsuario varchar(255) not null, nombreVideo varchar(255) not null, etiquetas varchar(255) not null, tamano varchar(255) not null, rutaEnS3 varchar(255) not null, fechaSubida date not null, publico bool not null, PRIMARY KEY (idVideo), FOREIGN KEY (nombreUsuario) REFERENCES Users(nombreUsuario) ON DELETE CASCADE );

CREATE TABLE Comments( idComment int auto_increment, nombreUsuario varchar(255) not null, idVideo int not null, content varchar(255) not null, idResp int, PRIMARY KEY(idComment), FOREIGN KEY (nombreUsuario) REFERENCES Users(nombreUsuario) ON DELETE CASCADE, FOREIGN KEY (idVideo) REFERENCES Videos(idVideo) ON DELETE CASCADE, FOREIGN KEY (idResp) REFERENCES Comments(idComment) ON DELETE CASCADE);

CREATE TABLE VotesV( idVoteV int auto_increment, nombreUsuario varchar(255) not null, idVideo int not null, contentVote int, PRIMARY KEY(idVoteV), FOREIGN KEY (nombreUsuario) REFERENCES Users(nombreUsuario) ON DELETE CASCADE, FOREIGN KEY (idVideo) REFERENCES Videos(idVideo) ON DELETE CASCADE);

CREATE TABLE VotesC( idVoteC int auto_increment, nombreUsuario varchar(255) not null, idComment int not null, contentVote int, PRIMARY KEY(idVoteC), FOREIGN KEY (nombreUsuario) REFERENCES Users(nombreUsuario) ON DELETE CASCADE, FOREIGN KEY (idComment) REFERENCES Comments(idComment) ON DELETE CASCADE);
