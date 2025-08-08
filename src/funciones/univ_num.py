EDAD = "CH06"
NIVEL_EDUCATIVO = "NIVEL_ED"
def add_uni(data):
    for info in data:
        if not info.get(NIVEL_EDUCATIVO) or int(info.get(EDAD)) < 18:
            continue  # Salta si no hay nivel educativo o es menor de edad
        nivel = int(info[NIVEL_EDUCATIVO])
        if nivel == 6:
            univ = 1  # Universitario
        elif nivel < 6:
            univ = 0  # No Universitario
        elif nivel > 6:
            univ = 2  # No Aplica
        info["UNIVERSITARIO"] = univ
