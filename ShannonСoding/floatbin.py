
def float_to_binary(val: float) -> str:
    '''
    float -> binary

    : param val: Значение которое следует перевести в 2-ный код.
    : type val: float

    :return: Возвращает строку двоичного кода.
    :rtype:  str
    '''

    exponent = 0
    shifted_num = val

    while shifted_num != int(shifted_num):
        shifted_num *= 2
        exponent += 1

    if exponent == 0:
        return '{0:0b}'.format(int(shifted_num))

    binary='{0:0{1}b}'.format(int(shifted_num), exponent + 1)
    integer_part=binary[:-exponent]
    fractional_part=binary[-exponent:].rstrip('0')

    return '{0}.{1}'.format(integer_part, fractional_part)
