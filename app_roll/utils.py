from .models import MesaHasUsuario, Mesa

def obtener_mesas_gamemaster(user_id):
    mesas_gamemaster = MesaHasUsuario.objects.filter(
        usuario_id=user_id, 
        rol='GAMEMASTER'
    ).select_related('mesa')  # Usa `select_related` para optimizar el acceso a la mesa asociada

    # Extrae los datos de las mesas
    mesas_data = [
        {
            'id': relacion.mesa.id,
            'nombre': relacion.mesa.nombre,
            'tematica' : relacion.mesa.tematica,
            
        }
        for relacion in mesas_gamemaster
    ]
    return mesas_data
