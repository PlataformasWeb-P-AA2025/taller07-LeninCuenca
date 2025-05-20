from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from genera_tablas import Club, Jugador
from configuracion import cadena_base_datos

engine = create_engine(cadena_base_datos)
Session = sessionmaker(bind=engine)
session = Session()

# Leer y guardar los clubes
with open("data/datos_clubs.txt", "r", encoding="utf-8") as f_clubs:
    for linea in f_clubs:
        datos = linea.strip().split(";")
        if len(datos) == 3:
            nombre, deporte, fundacion = datos
            club = Club(nombre=nombre, deporte=deporte, fundacion=int(fundacion))
            session.add(club)

session.commit()  # Guarda los clubes y asigna sus IDs

# Leer y guardar los jugadores
with open("data/datos_jugadores.txt", "r", encoding="utf-8") as f_jugadores:
    for linea in f_jugadores:
        datos = linea.strip().split(";")
        if len(datos) == 4:
            nombre_club, posicion, dorsal, nombre_jugador = datos
            # Busca el club directamente en la base de datos
            club = session.query(Club).filter_by(nombre=nombre_club).first()
            if club:
                jugador = Jugador(
                    nombre=nombre_jugador,
                    dorsal=int(dorsal),
                    posicion=posicion.lower(),
                    club=club
                )
                session.add(jugador)

session.commit()
print("Datos guardados correctamente.")