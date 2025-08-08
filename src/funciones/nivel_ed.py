def valor_educacion_texto (value_original):
    """Retorno un string en base a un numero en tipo str"""
    if value_original == '1':
        return ("Primario incompleto")
    elif value_original == '2':
        return ("Primario completo")
    elif value_original == '3':
        return ("Secundario incompleto")
    elif value_original == '4':
        return ("Secundario completo")
    elif value_original == '5' or value_original == '6':
        return ("Superior o universitario")
    else:
        return ("Sin informacion")

        



def key_nivel_ed_str (info_individuos):
    """Creo nueva clave en info_individuos y agrego su valor en base al nivel educativo
    Recibo: Lista de diccionarios
    Retorno: Lista de diccionarios con nueva clave en cada diccionario y su valor"""
    for individuos in info_individuos:
        if 'NIVEL_ED' in (individuos):
            valor = individuos['NIVEL_ED']
            individuos["NIVEL_ED_str"] = valor_educacion_texto (valor)
        else:
            individuos["NIVEL_ED_str"] = None

