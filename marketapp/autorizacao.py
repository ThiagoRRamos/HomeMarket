from django.contrib.auth.decorators import user_passes_test


def _eh_cliente(user):
    return not hasattr(user, 'supermercado')


def _eh_supermercado(user):
    return hasattr(user, 'supermercado')


def apenas_supermercado():
    return user_passes_test(_eh_supermercado)


def apenas_cliente():
    return user_passes_test(_eh_cliente)
