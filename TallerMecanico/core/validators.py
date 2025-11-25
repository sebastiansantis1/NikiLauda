import re
from django.core.exceptions import ValidationError
import requests
from django.conf import settings

#####
#####Rut
#####

def formatear_rut(rut):  
    return re.sub(r'[^0-9kK]', '', rut) # Limpiar el rut para solo numeros y K.

def validar_rut_chileno(rut):
    """
    Valida un RUT chileno real usando módulo 11.
    Formatos válidos: 12345678-5, 12.345.678-5, 123456785
    """

    if not rut:
        raise ValidationError("El RUT no puede estar vacío.")

    # Normalizar: quitar puntos y guiones
    rut = rut.replace(".", "").replace("-", "").upper()

    if len(rut) < 2:
        raise ValidationError("El RUT es demasiado corto.")

    cuerpo = rut[:-1]
    dv = rut[-1]

    if not cuerpo.isdigit():
        raise ValidationError("El RUT es inválido.")

    # --- Calcular DV ---
    suma = 0
    multiplo = 2

    for c in reversed(cuerpo):
        suma += int(c) * multiplo
        multiplo += 1
        if multiplo > 7:
            multiplo = 2

    resto = suma % 11
    dv_calculado = 11 - resto

    if dv_calculado == 11:
        dv_calculado = "0"
    elif dv_calculado == 10:
        dv_calculado = "K"
    else:
        dv_calculado = str(dv_calculado)

    # Comparar DV
    if dv != dv_calculado:
        raise ValidationError(f"El RUT no es válido. DV esperado: {dv_calculado}")

    return rut
#####    
#####Texto
#####

def validar_solo_texto(value):  #Solo letras a-z y A-Z 
    if not re.fullmatch(r"[A-Za-zÁÉÍÓÚáéíóúÑñ ]+", value):
        raise ValidationError("El campo solo debe contener letras.")

def validar_texto_numeros(value): #solo letras y numeros positivos.
    if not re.fullmatch(r"[A-Za-z0-9ÁÉÍÓÚáéíóúÑñ ]+", value):
        raise ValidationError("El campo solo debe contener letras y números.")

def validar_caracteres_especiales(value):
    if not re.fullmatch(r"[A-Za-z0-9@+/\- ]+", value):
        raise ValidationError("Caracteres permitidos: letras, números, @, +, /, -")
    
    
#####
#####Patentes
#####
    
def validar_patente_api(patente):
    api_key=getattr(settings, "PATENTE_API_KEY", None)
    if not api_key:
        return None
    
    url = f"https://chile.getapi.cl/v1/vehicles/plate/{patente}"
    
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    
    try:
        response = requests.get(url, headers=headers,timeout=5)
        if response.status_code == 200:
            data = response.json()
            return data
        return None
    except Exception:
        return None
    
    