import subprocess
import sys
import os

# Obtiene la ruta absoluta del directorio donde se encuentra este script
# Esto asegura que requirements.txt se encuentre correctamente
script_dir = os.path.dirname(os.path.abspath(__file__))
requirements_path = os.path.join(script_dir, 'requirements.txt')

print("Iniciando la instalación de dependencias...")
print(f"Buscando requirements.txt en: {requirements_path}")

try:
    # Construye el comando para ejecutar pip usando el intérprete de Python actual
    # sys.executable es el path al intérprete de Python que está ejecutando este script
    command = [sys.executable, "-m", "pip", "install", "-r", requirements_path]

    # Ejecuta el comando
    # capture_output=True para capturar stdout y stderr
    # text=True para que la salida sea texto (string)
    # check=True para que lance una excepción si el comando falla
    result = subprocess.run(command, capture_output=True, text=True, check=True)

    print("\n--- Instalación de Pip completada exitosamente ---")
    print("STDOUT:")
    print(result.stdout)
    print("STDERR:")
    print(result.stderr)

except subprocess.CalledProcessError as e:
    print(f"\n--- ERROR durante la instalación de Pip (Código de salida: {e.returncode}) ---")
    print("STDOUT:")
    print(e.stdout)
    print("STDERR:")
    print(e.stderr)
    sys.exit(1) # Sale con un código de error
except FileNotFoundError:
    print(f"\n--- ERROR: No se encontró requirements.txt en {requirements_path} ---")
    sys.exit(1)
except Exception as e:
    print(f"\n--- Ocurrió un error inesperado: {e} ---")
    sys.exit(1)