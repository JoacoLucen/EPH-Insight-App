#Renombro las variables con un nombre mas significativo
TIPO_PISO = "IV3"
HAY_AGUA = "IV6"
ORIGEN_AGUA = "IV7"
TIENE_BANIO = "IV8"
UBICACION_BANIO = "IV9"
TIPO_BANIO = "IV10"
DESAGUE = "IV11"


def condicion_de_habitabilidad(hogares):
    
    # Inicializa puntaje
    for h in hogares: 
        points = 0
        # Condición inmediata de habitabilidad insuficiente
        # Si no hay baño o agua
        if (h[TIENE_BANIO] == '2' or h[HAY_AGUA] == '3'):
            h["CONDICION_DE_HABITABILIDAD"] = "Insuficiente"
        else:
            # Condiciones estructurales básicas del hogar

            # Tipo de vivienda (mejor cuanto menor el número)
            match h[TIPO_PISO] :
                case "2":
                    points += 1
                case "1":
                    points += 2
            # Tipo de baño
            match h[HAY_AGUA] :
                case "2":
                    points += 1
                case "1":
                    points += 2
            # Tipo de agua
            match h[ORIGEN_AGUA] :
                case "3":
                    points += 1
                case "2":
                    points += 2
                case "1":
                    points += 3
            # Tipo de desagüe
            match h[UBICACION_BANIO] :
                case "2":
                    points += 1
                case "1":
                    points += 3
            #Tipo baño
            match h[TIPO_BANIO] :
                case "2":
                    points += 1
                case "1":
                    points += 2
            #Manejo de desague
            match h[DESAGUE] :
                case "2":
                    points += 2
                case "1":
                    points += 4

            match h["MATERIAL_TECHUMBRE"]:
                case "Material precario":
                    points += 1
                case "Material durable":
                    points += 2

            # Asignación final según puntaje acumulado
            if points <= 4:
                h["CONDICION_DE_HABITABILIDAD"] = "Insuficiente"
            elif points <= 8:
                h["CONDICION_DE_HABITABILIDAD"] = "Regular"
            elif points < 16:
                h["CONDICION_DE_HABITABILIDAD"] = "Saludable"
            else :  # points >= 16
                h["CONDICION_DE_HABITABILIDAD"] = "Buena"