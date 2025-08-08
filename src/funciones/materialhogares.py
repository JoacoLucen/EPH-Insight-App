def material_techumbre(list_dic_hogar):
    """
    Traducir los valores de IV4 de integer a strings:
        - Valor de 1 a 4 => 'Material durable'
        - Valor de 5 a 7 => 'Material precario'
        - Valor 9 u otro => 'No aplica'

    Args:
        list_dic_hogar (list[dict]): lista de diccionarios con datos de hogar

    Returns:
        list_dic_hogar (list[dict]): lista modificada con nueva clave 'MATERIAL_TECHUMBRE'
    """
    material_durable = {'1', '2', '3', '4'}
    material_precario = {'5', '6', '7'}

    for dic in list_dic_hogar:
        valor = str(dic.get('IV4', '')).strip()  # Convertir a string y quitar espacios.
        if valor in material_precario:
            dic['MATERIAL_TECHUMBRE'] = 'Material precario'
        elif valor in material_durable:
            dic['MATERIAL_TECHUMBRE'] = 'Material durable'
        elif valor == 9:
            dic['MATERIAL_TECHUMBRE'] = 'No aplica'
        else:                                       # Si hay valores distintos del 1 al 7 y el 9.
            dic['MATERIAL_TECHUMBRE'] = 'Sin Datos'
