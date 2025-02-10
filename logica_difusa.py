import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

# --------------------------------------------------
# 1. Configuración del Sistema Difuso
# --------------------------------------------------

# Definición de variables difusas
consumo = ctrl.Antecedent(np.arange(0, 2501, 1), 'consumo')
costo = ctrl.Antecedent(np.arange(0, 3.01, 0.1), 'costo')
nivel_uso = ctrl.Consequent(np.arange(0, 3.1, 0.1), 'nivel_uso')

# Funciones para el consumo
consumo['bajo'] = fuzz.trimf(consumo.universe, [0, 300, 500])
consumo['medio'] = fuzz.trimf(consumo.universe, [400, 800, 1200])
consumo['alto'] = fuzz.trimf(consumo.universe, [1000, 1500, 2500])

# Funciones para el costo
costo['bajo'] = fuzz.trimf(costo.universe, [0, 0.5, 1.0])
costo['medio'] = fuzz.trimf(costo.universe, [0.5, 1.5, 2.0])
costo['alto'] = fuzz.trimf(costo.universe, [1.5, 2.5, 3.0])

# Funciones para el nivel de uso recomendado
nivel_uso['bajo'] = fuzz.trimf(nivel_uso.universe, [0, 0.5, 1.0])
nivel_uso['moderado'] = fuzz.trimf(nivel_uso.universe, [0.5, 1.5, 2.0])
nivel_uso['alto'] = fuzz.trimf(nivel_uso.universe, [1.5, 2.5, 3.0])

# --------------------------------------------------
# 2. Reglas Difusas
# --------------------------------------------------
reglas = [
    # Reglas base de consumo y costo
    ctrl.Rule(consumo['alto'] & costo['alto'], nivel_uso['bajo']),
    ctrl.Rule(consumo['medio'] & costo['medio'], nivel_uso['moderado']),
    ctrl.Rule(consumo['bajo'], nivel_uso['alto']),
    
    # Reglas adicionales para casos específicos
    ctrl.Rule(consumo['medio'] & costo['alto'], nivel_uso['bajo']),
    ctrl.Rule(consumo['alto'] & costo['medio'], nivel_uso['moderado']),
    
    # Regla prioritaria para dispositivos esenciales
    ctrl.Rule(consumo['alto'] | costo['alto'], nivel_uso['alto'].copy(), 'prioridad_esencial')
]

# --------------------------------------------------
# 3. Sistema de Control
# --------------------------------------------------
sistema_control = ctrl.ControlSystem(reglas)
sistema = ctrl.ControlSystemSimulation(sistema_control)

# --------------------------------------------------
# 4. Base de Datos de Dispositivos
# --------------------------------------------------
dispositivos = [
    {
        'id': "Refrigerador",
        'tipo': "Esencial",
        'consumo': 200,
        'costo': 0.8,
        'prioridad': 'alta'
    },
    {
        'id': "Aire Acondicionado",
        'tipo': "Confort",
        'consumo': 2000,
        'costo': 2.5,
        'prioridad': 'media'
    },
    {
        'id': "TV",
        'tipo': "Entretenimiento",
        'consumo': 150,
        'costo': 1.2,
        'prioridad': 'baja'
    },
    {
        'id': "Lavadora",
        'tipo': "Electrodoméstico",
        'consumo': 800,
        'costo': 2.0,
        'prioridad': 'media'
    },
    {
        'id': "Ordenador",
        'tipo': "Trabajo",
        'consumo': 300,
        'costo': 1.5,
        'prioridad': 'alta'
    }
]

# --------------------------------------------------
# 5. Función de Evaluación
# --------------------------------------------------
def evaluar_dispositivo(dispositivo):
    # Aplicar reglas difusas
    sistema.input['consumo'] = dispositivo['consumo']
    sistema.input['costo'] = dispositivo['costo']
    sistema.compute()
    
    # Obtener valor numérico y convertir a etiqueta lingüística
    valor_numerico = sistema.output['nivel_uso']
    membresias = {
        'bajo': fuzz.interp_membership(nivel_uso.universe, nivel_uso['bajo'].mf, valor_numerico),
        'moderado': fuzz.interp_membership(nivel_uso.universe, nivel_uso['moderado'].mf, valor_numerico),
        'alto': fuzz.interp_membership(nivel_uso.universe, nivel_uso['alto'].mf, valor_numerico)
    }
    
    # Prioridad especial para dispositivos esenciales
    if dispositivo['tipo'] == "Esencial":
        return 'ALTO (Prioridad Especial)'
    
    # Seleccionar etiqueta con mayor membresía
    return max(membresias, key=membresias.get).upper()

# --------------------------------------------------
# 6. Visualización de Funciones de Membresía
# --------------------------------------------------
fig, (ax0, ax1, ax2) = plt.subplots(nrows=3, figsize=(8, 9))

consumo.view(ax=ax0)
ax0.set_title('Consumo Energético')
costo.view(ax=ax1)
ax1.set_title('Costo de Energía')
nivel_uso.view(ax=ax2)
ax2.set_title('Nivel de Uso Recomendado')

plt.tight_layout()
plt.savefig('funciones_membresia.png')
plt.close()