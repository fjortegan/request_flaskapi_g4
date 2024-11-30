def user_password_correcto(dict_usuarios : dict[str,str],usuario,contraseña):

    try:

      if dict_usuarios[usuario] == contraseña :

        return True
      
    except KeyError:
       
       return False