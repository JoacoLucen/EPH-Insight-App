def condicion_laboral(personas):
    for p in personas:
        # Si la persona está ocupada (ESTADO = 1) y es patrón o cuenta propia
        if p["ESTADO"] == '1' and p["CAT_OCUP"] in ('1', '2'):
            p["CONDICION_LABORAL"] = "Ocupado autónomo"

        # Si está ocupada y es obrero o empleado, Trabajador familiar sin remuneración o Ns/Nr 
        elif p["ESTADO"] == '1' and p["CAT_OCUP"] in ('3', '4', '9'):
            p["CONDICION_LABORAL"] = "Ocupado dependiente"

        # Desocupado (ESTADO = 2)
        elif p["ESTADO"] == '2':
            p["CONDICION_LABORAL"] = "Desocupado"
    
        # Inactivo (no busca ni tiene trabajo, ESTADO = 3)
        elif p["ESTADO"] == '3':
            p["CONDICION_LABORAL"] = "Inactivo"
    
        # Casos fuera de categoría esperada o sin información
        elif p["ESTADO"] == '4':
            p["CONDICION_LABORAL"] = "Fuera de categoría/sin información"
    
        # Cualquier otro valor se considera inválido
        else:
            p["CONDICION_LABORAL"] = "Dato inválido"