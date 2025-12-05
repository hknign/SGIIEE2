
import math
from decimal import Decimal
from asientos.models import Asiento


# ======================================================
#  PRECIOS Y ZONAS 
# ======================================================
def calcular_precio(evento, zona):
    if zona == "vip":
        return evento.precio_vip
    if zona == "avanzado":
        return evento.precio_avanzado
    return evento.precio_normal


def dividir_capacidad(capacidad):
    vip = int(capacidad * 0.10)
    avanzado = int(capacidad * 0.30)
    normal = capacidad - vip - avanzado
    return normal, avanzado, vip


# ======================================================
#  GENERADORES ORIGINALES 
# ======================================================
def posiciones_circulo(capacidad, padding=5):
    cx, cy = 50.0, 50.0
    max_r = 50.0 - padding
    posiciones = []
    anillos = int(math.sqrt(capacidad)) + 4
    for layer in range(anillos):
        r = (layer / max(1, anillos - 1)) * max_r
        if r < 1e-6:
            posiciones.append((cx, cy))
            continue
        puntos = max(6, int((2 * math.pi * r) / 4))
        for i in range(puntos):
            ang = 2 * math.pi * i / puntos
            x = cx + r * math.cos(ang)
            y = cy + r * math.sin(ang)
            posiciones.append((x, y))
            if len(posiciones) >= capacidad:
                return posiciones[:capacidad]
    return posiciones[:capacidad]


def posiciones_cuadrado(capacidad, padding=6):
    posiciones = []
    cx, cy = 50.0, 50.0
    max_side = 100.0 - padding * 2
    n = int(math.ceil(math.sqrt(capacidad)))
    if n <= 1:
        return [(cx, cy)]
    step = max_side / (n - 1)
    start = cx - max_side / 2
    for i in range(n):
        for j in range(n):
            x = start + j * step
            y = start + i * step
            posiciones.append((x, y))
            if len(posiciones) >= capacidad:
                return posiciones[:capacidad]
    return posiciones[:capacidad]


def posiciones_rectangulo(capacidad, padding=6, aspect=1.6):
    posiciones = []
    cx, cy = 50.0, 50.0
    h = 100.0 - padding * 2
    w = min(100.0 - padding * 2, h * aspect)
    cols = int(math.ceil(math.sqrt(capacidad * (w/h))))
    rows = int(math.ceil(capacidad / cols))
    step_x = w / max(1, (cols - 1))
    step_y = h / max(1, (rows - 1))
    start_x = cx - w/2
    start_y = cy - h/2
    for r in range(rows):
        for c in range(cols):
            x = start_x + c * step_x
            y = start_y + r * step_y
            posiciones.append((x, y))
            if len(posiciones) >= capacidad:
                return posiciones[:capacidad]
    return posiciones[:capacidad]


def posiciones_triangulo(capacidad, padding=6):
    posiciones = []
    max_w = 100.0 - padding * 2
    cx = 50.0
    rows = int(math.ceil(math.sqrt(2 * capacidad)))
    for r in range(rows):
        count = r + 1
        y = padding + (r / max(1, rows - 1)) * (100.0 - 2 * padding)
        if count == 1:
            posiciones.append((cx, y))
        else:
            span = max_w * (count / rows)
            start_x = cx - span / 2
            step = span / (count - 1)
            for c in range(count):
                x = start_x + c * step
                posiciones.append((x, y))
                if len(posiciones) >= capacidad:
                    return posiciones[:capacidad]
    return posiciones[:capacidad]


def posiciones_poligono(capacidad, lados, padding=6):
    posiciones = []
    cx, cy = 50.0, 50.0
    max_r = 50.0 - padding
    capas = int(math.sqrt(capacidad)) + 4
    for layer in range(1, capas + 1):
        r = (layer / capas) * max_r
        puntos = max(6, lados * layer)
        for i in range(puntos):
            ang = 2 * math.pi * i / puntos
            x = cx + r * math.cos(ang)
            y = cy + r * math.sin(ang)
            posiciones.append((x, y))
            if len(posiciones) >= capacidad:
                return posiciones[:capacidad]
    return posiciones[:capacidad]


# ======================================================
#   GENERAR ESCENARIO CENTRAL 
# ======================================================
def generar_escenario(forma):
    cx, cy = 50, 50
    size = 18  

    if forma == "circulo":
        return {"tipo": "circulo", "cx": cx, "cy": cy, "r": size/2, "titulo": "ESCENARIO"}

    if forma == "cuadrado":
        return {"tipo": "rect", "x": cx-size/2, "y": cy-size/2, "w": size, "h": size, "titulo": "ESCENARIO"}

    if forma == "rectangulo":
        return {"tipo": "rect", "x": cx-(size*1.6)/2, "y": cy-(size*0.8)/2,
                "w": size*1.6, "h": size*0.8, "titulo": "ESCENARIO"}

    if forma == "triangulo":
        h = size
        return {
            "tipo": "polygon",
            "points": [(cx, cy-h/2), (cx-h/2, cy+h/2), (cx+h/2, cy+h/2)],
            "titulo": "ESCENARIO"
        }

    if forma == "hexagono":
        pts = []
        r = size/2
        for i in range(6):
            ang = 2*math.pi*i/6
            pts.append((cx+r*math.cos(ang), cy+r*math.sin(ang)))
        return {"tipo": "polygon", "points": pts, "titulo": "ESCENARIO"}

    if forma == "octagono":
        pts = []
        r = size/2
        for i in range(8):
            ang = 2*math.pi*i/8
            pts.append((cx+r*math.cos(ang), cy+r*math.sin(ang)))
        return {"tipo": "polygon", "points": pts, "titulo": "ESCENARIO"}

    # fallback
    return {"tipo": "rect", "x": cx-size/2, "y": cy-size/2, "w": size, "h": size, "titulo": "ESCENARIO"}


# ======================================================
#   PUNTO FUERA DE ESCENARIO 
# ======================================================
def punto_fuera_de_escenario(x, y, escenario):
    if escenario["tipo"] == "circulo":
        dx = x - escenario["cx"]
        dy = y - escenario["cy"]
        return math.hypot(dx, dy) > escenario["r"]

    if escenario["tipo"] == "rect":
        return not (
            escenario["x"] <= x <= escenario["x"] + escenario["w"] and
            escenario["y"] <= y <= escenario["y"] + escenario["h"]
        )

    if escenario["tipo"] == "polygon":
        pts = escenario["points"]
        inside = False
        n = len(pts)
        for i in range(n):
            x1, y1 = pts[i]
            x2, y2 = pts[(i+1) % n]
            if ((y1 > y) != (y2 > y)) and \
               (x < (x2-x1)*(y-y1)/(y2-y1+0.0001) + x1):
                inside = not inside
        return not inside

    return True


# ======================================================
#   ZONAS 
# ======================================================
def asignar_zonas_por_distancia(posiciones, capacidad):
    normal_count, avanzado_count, vip_count = dividir_capacidad(capacidad)
    centro = (50.0, 50.0)
    lista = []
    for (x, y) in posiciones:
        dx = x - centro[0]
        dy = y - centro[1]
        d = math.hypot(dx, dy)
        lista.append({"x": x, "y": y, "d": d})
    lista.sort(key=lambda o: o["d"])
    for i, item in enumerate(lista):
        if i < vip_count:
            item["zona"] = "vip"
        elif i < vip_count + avanzado_count:
            item["zona"] = "avanzado"
        else:
            item["zona"] = "normal"
    return lista[:capacidad]


# ======================================================
#   FUNCIÓN PRINCIPAL
# ======================================================
def generar_asientos(evento):
    capacidad = int(evento.capacidad)
    forma = (evento.forma_recinto or "cuadrado").lower()

 
    escenario = generar_escenario(forma)

    if forma == "circulo":
        posiciones = posiciones_circulo(capacidad)
    elif forma == "cuadrado":
        posiciones = posiciones_cuadrado(capacidad)
    elif forma == "rectangulo":
        posiciones = posiciones_rectangulo(capacidad)
    elif forma == "triangulo":
        posiciones = posiciones_triangulo(capacidad)
    elif forma == "hexagono":
        posiciones = posiciones_poligono(capacidad, lados=6)
    elif forma == "octagono":
        posiciones = posiciones_poligono(capacidad, lados=8)
    else:
        posiciones = posiciones_cuadrado(capacidad)

    posiciones = [p for p in posiciones if punto_fuera_de_escenario(p[0], p[1], escenario)]

  
    while len(posiciones) < capacidad:
        extra = posiciones_cuadrado(capacidad)
        extra = [p for p in extra if punto_fuera_de_escenario(p[0], p[1], escenario)]
        posiciones += extra
        posiciones = posiciones[:capacidad]

 
    asignadas = asignar_zonas_por_distancia(posiciones, capacidad)

 
    Asiento.objects.filter(evento=evento).delete()

    creados = []
    numero_por_letra = {}

    for idx, item in enumerate(asignadas):
        x = float(item["x"])
        y = float(item["y"])
        zona = item["zona"]

        fila = chr(65 + (idx // 26) % 26)
        numero_por_letra.setdefault(fila, 0)
        numero_por_letra[fila] += 1
        numero = numero_por_letra[fila]

        precio = calcular_precio(evento, zona)

        a = Asiento.objects.create(
            evento=evento,
            fila=fila,
            numero=numero,
            pos_x=max(0, min(100, x)),
            pos_y=max(0, min(100, y)),
            zona=zona,
            precio=precio,
            estado="disponible"
        )
        creados.append(a)

    return {
        "asientos": creados,
        "escenario": escenario
    }
