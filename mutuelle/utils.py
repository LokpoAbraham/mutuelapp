from functools import wraps
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

def verrouille_si_exercice_cloture(modele, pk_name='pk'):
    """
    Décorateur pour empêcher la modification si l’exercice de l'objet est clôturé.
    modele : le modèle (ex : Cotisation)
    pk_name : nom du paramètre pk dans l’URL (souvent 'pk')
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            obj_pk = kwargs.get(pk_name)
            obj = get_object_or_404(modele, pk=obj_pk)
            if obj.exercice.cloture:
                messages.error(request, "Impossible : l'exercice est clôturé.")
                # Redirige vers la liste adaptée (modifie selon ton cas)
                if modele.__name__.lower() == "cotisation":
                    return redirect('cotisations_list')
                elif modele.__name__.lower() == "depense":
                    return redirect('depenses_list')
                else:
                    return redirect('/')
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
