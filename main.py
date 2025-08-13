
import os
import numpy as np
from models.forest_fire_fIMG import ForestFireFIMG
from utils.analizar_imagen import analizar_imagen
from utils.diagnostico_inicial import diagnostico_inicial
from visualization.mostrar_mascara import mostrar_mascara
from visualization.animar_simulacion import animar_simulacion
from visualization.obtener_estados import obtener_estados


def ejecutar_simulacion():
    print("\n[INFO] si deseas detener la simulación manualmente, presiona Ctrl+C en la terminal.\n")
    ruta_imagen = 'forest.png'
    umbral = 128
    if not os.path.isfile(ruta_imagen):
        print(f"ERROR: no se encontro la imagen '{ruta_imagen}'")
        return
    arr, mascara_auto, _, _ = analizar_imagen(ruta_imagen, False)
    filas, columnas = arr.shape
    print(f"la imagen tiene dimensiones: {filas} filas x {columnas} columnas.")
    mascara = arr < umbral
    # USAR LA FILA CENTRAL PARA INICIAR EL INCENDIO
    fila_inicio = filas // 2
    parametros = {
        'image_path': ruta_imagen,
        'threshold': umbral,
        'start_row': fila_inicio,
    }
    try:
        modelo = ForestFireFIMG(parametros)
        modelo.setup()  # INICIALIZAR EL MODELO
        modelo.running = True  # FORZAR EJECUCION
        # PARA LIMITAR LA SIMULACION A UN NUMERO MAXIMO DE PASOS, USA LA SIGUIENTE LINEA Y AJUSTA EL VALOR:
        max_pasos = 200  # LIMITA A 200 PASOS PARA PRUEBAS
        # PARA EJECUTAR TODOS LOS PASOS POSIBLES (SIN TOPE), COMENTA LA LINEA ANTERIOR Y DESCOMENTA LA SIGUIENTE:
        # max_pasos = None
        estados = obtener_estados(modelo, max_pasos=max_pasos)
        # CALCULAR METRICAS FINALES
        porcentaje_quemados = None
        pasos = len(estados)
        if hasattr(modelo, 'forest') and hasattr(modelo, 'agents'):
            total_arboles = len(modelo.agents)
            quemados = sum(1 for a in modelo.agents if hasattr(a, 'condition') and a.condition == 2)
            if total_arboles > 0:
                porcentaje_quemados = quemados / total_arboles
        if porcentaje_quemados is not None:
            print(f"porcentaje de arboles quemados: {porcentaje_quemados*100:.2f}%")
        else:
            print("no se pudo calcular el porcentaje de arboles quemados.")
        print(f"pasos de simulacion: {pasos}")
        # GUARDAR LOS ESTADOS PARA REPETIR LA ANIMACION SIN VOLVER A SIMULAR
        return modelo, estados
    except Exception as e:
        print("ocurrio un error durante la simulacion:", e)

def main():
    while True:
        modelo, estados = ejecutar_simulacion()
        while True:
            import time
            print("mostrando animacion. Puedes ajustar la velocidad cambiando el argumento 'velocidad_ms' en animar_simulacion.")
            tiempo_inicio = time.time()
            animar_simulacion(modelo, estados, velocidad_ms=30)  # CAMBIA ESTE VALOR PARA AJUSTAR LA VELOCIDAD (ms)
            tiempo_total = time.time() - tiempo_inicio
            print(f"tiempo de animacion: {tiempo_total:.2f} segundos")
            repetir_anim = input("¿deseas repetir la animacion? (s/n): ").strip().lower()
            if repetir_anim != 's':
                break
        repetir = input("¿deseas repetir la simulacion completa? (s/n): ").strip().lower()
        if repetir != 's':
            print("fin del programa.")
            break

if __name__ == "__main__":
    main()
