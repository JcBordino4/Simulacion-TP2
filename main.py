import random
import math

# Funcion para generar números con distribución uniforme en [a, b]
def uniform_gen(a, b, n):
    return [round(a + random.random() * (b - a), 4) for _ in range(n)]

# Funcion para generar números con distribución exponencial negativa usando: X = -1/λ * ln(1 - RND)
def exponencial_gen(mu, n):
    lam = 1 / mu  # lambda es el inverso de la media
    return [round(-1 / lam * math.log(1 - random.random()), 4) for _ in range(n)]

# Funcion para generar números con distribución normal usando el método de Box-Muller
def normal_gen(mu, sigma, n):
    resultados = []
    for _ in range(n // 2):
        rnd1 = random.random()
        rnd2 = random.random()
        z1 = math.sqrt(-2 * math.log(rnd1)) * math.cos(2 * math.pi * rnd2)
        z2 = math.sqrt(-2 * math.log(rnd1)) * math.sin(2 * math.pi * rnd2)
        x1 = round(z1 * sigma + mu, 4)
        x2 = round(z2 * sigma + mu, 4)
        resultados.extend([x1, x2])
    
    if n % 2 == 1:  # Si el tamaño de muestra es impar, generamos uno más
        rnd1 = random.random()
        rnd2 = random.random()
        z = math.sqrt(-2 * math.log(rnd1)) * math.cos(2 * math.pi * rnd2)
        resultados.append(round(z * sigma + mu, 4))

    return resultados

def main():
    print("Seleccione la distribución:")
    print("1. Uniforme [a, b]")
    print("2. Exponencial negativa")
    print("3. Normal (Box-Muller)")
    
    opcion = input("Ingrese una opción (1/2/3): ")

    try:
        n = int(input("Ingrese el tamaño de la muestra (máx. 1 millón): "))
        if n <= 0 or n > 1_000_000:
            raise ValueError("Tamaño de muestra inválido.")
    except ValueError as e:
        print(f"Error: {e}")
        return

    if opcion == "1":
        a = float(input("Ingrese el valor de a: "))
        b = float(input("Ingrese el valor de b: "))
        muestra = uniform_gen(a, b, n)

    elif opcion == "2":
        mu = float(input("Ingrese el valor de mu (media): "))
        if mu <= 0:
            print("La media debe ser mayor que 0 para la distribución exponencial.")
            return
        muestra = exponencial_gen(mu, n)

    elif opcion == "3":
        mu = float(input("Ingrese el valor de mu (media): "))
        sigma = float(input("Ingrese el valor de sigma (desviación estándar): "))
        muestra = normal_gen(mu, sigma, n)

    else:
        print("Opción no válida.")
        return

    print(f"\nPrimeros 10 valores generados ({len(muestra)} en total):")
    print(muestra[:10])

if __name__ == "__main__":
    main()
