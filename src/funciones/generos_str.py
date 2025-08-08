def int_to_str (list_disc_indi):
    """cambia losv alores de CH04 de integer a string
        valor 1 = Masculino.
        valor 2 = Femenino.
        
    Args:
        list_disc_indi (list_disc): recibe los datos en crudo

    Returns:
        _type_: los devuelve ya modificados
    """
    for d in list_disc_indi:
        valor = d.get('CH04')  # evita KeyError

        if str(valor) == '1' or valor == 1:
            d['CH04_str'] = 'Masculino'
        elif str(valor) == '2' or valor == 2:
            d['CH04_str'] = 'Femenino'
        else:
            d['CH04_str'] = 'sin información'
