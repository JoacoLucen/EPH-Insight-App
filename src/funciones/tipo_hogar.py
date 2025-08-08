def key_tipo_hogar(list_dic_hogar):
    for dic in list_dic_hogar:
        cant_personas = int(dic.get('IX_TOT', 0))
        if cant_personas == 1:
            dic['TIPO_HOGAR'] = 'Unipersonal'
        elif 2 <= cant_personas <= 4:
            dic['TIPO_HOGAR'] = 'Nuclear'
        elif cant_personas >= 5:
            dic['TIPO_HOGAR'] = 'Extendido'
        else:
            dic['TIPO_HOGAR'] = 'Sin Datos'
