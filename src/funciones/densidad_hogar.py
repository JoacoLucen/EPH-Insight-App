def function_value(spaces, people):

    if not spaces.isnumeric():
        return 0

    spaces_int = int(spaces)
    people_int = int(people)
        
    if spaces_int == 0 or people_int == 0:
        return 0
    else:
        density = people_int / spaces_int

    if density <= 1:
        return "Bajo"
    elif 1 < density <= 2:
        return "Medio"
    else:
        return "Alto"

def key_densidad_hogar(info_hogares):
    """Recibo la lista de diccionarios y creo la nueva key con sus respectivos values"""
    for hog in info_hogares:
        valor = None
        if "II1" in hog and "IX_TOT" in hog:
            spaces = hog["II1"]
            people = hog["IX_TOT"]
            valor = function_value(spaces, people)
        hog["DENSIDAD_HOGAR"] = valor