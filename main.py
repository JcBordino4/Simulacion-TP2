import random
import math
import typer
import matplotlib.pyplot as plt
from rich import print
from rich.panel import Panel
from rich.table import Table
from InquirerPy import inquirer

app = typer.Typer()

descripcion = """
Este programa genera números aleatorios según tres distribuciones:
• Uniforme [a, b]
• Exponencial negativa (μ)
• Normal (μ, σ)

Luego, permite visualizar:
• Los valores generados.
• Tabla de frecuencias por intervalos.
• Histograma gráfico (matplotlib).
"""

# Funciones de generación

def validar_muestra(x):
    try:
        if x is None or str(x).strip() == "":
            return False
        val = int(x)
        if val <= 0 or val > 1_000_000:
            return False
        return True
    except ValueError:
        raise False

def uniform_gen(a, b, n):
    return [round(a + random.random() * (b - a), 4) for _ in range(n)]

def exponencial_gen(mu, n):
    lam = 1 / mu
    return [round(-1 / lam * math.log(1 - random.random()), 4) for _ in range(n)]

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
    if n % 2 == 1:
        rnd1 = random.random()
        rnd2 = random.random()
        z = math.sqrt(-2 * math.log(rnd1)) * math.cos(2 * math.pi * rnd2)
        resultados.append(round(z * sigma + mu, 4))
    return resultados

def mostrar_todos(muestra):
    table = Table(title=f"Todos los valores generados ({len(muestra)})")
    table.add_column("Índice", style="cyan", justify="right")
    table.add_column("Valor", style="magenta", justify="right")

    for i, val in enumerate(muestra):
        table.add_row(str(i), str(val))
    print(table)

def tabla_frecuencias(muestra, k):
    minimo = min(muestra)
    maximo = max(muestra)
    ancho = (maximo - minimo) / k
    intervalos = [0] * k

    for valor in muestra:
        idx = int((valor - minimo) / ancho)
        if idx == k:  # caso borde
            idx -= 1
        intervalos[idx] += 1

    table = Table(title=f"Tabla de frecuencias (k={k})")
    table.add_column("Intervalo", style="green")
    table.add_column("Frecuencia", style="yellow")

    for i in range(k):
        lim_inf = round(minimo + i * ancho, 4)
        lim_sup = round(minimo + (i + 1) * ancho, 4)
        intervalo = f"[{lim_inf}, {lim_sup})"
        table.add_row(intervalo, str(intervalos[i]))

    print(table)

def graficar_histograma(muestra, k):
    plt.hist(muestra, bins=k, edgecolor='black')
    plt.title("Histograma de Frecuencia")
    plt.xlabel("Valor")
    plt.ylabel("Frecuencia")
    plt.grid(True)
    plt.show()

@app.command()
def generar():
    print(Panel("Generador de Variables Aleatorias", title="[bold cyan]Simulación - TP2", subtitle="Grupo 16", expand=False))
    print(descripcion)
    print()
    dist = inquirer.select(
        message="Seleccioná la distribución:",
        choices=["Uniforme", "Exponencial", "Normal"]
    ).execute()

    while True:
        try:
            n = inquirer.number(
                message="¿Tamaño de muestra? (hasta 1.000.000):",
                validate=lambda x: "Debe ingresar un número entero entre 1 y 1.000.000." if not x.strip() or not validar_muestra(x) else True,
                default=1000
            ).execute()

            # Asegurarse de que el valor no sea una cadena vacía antes de convertirlo a entero
            if not n.strip():
                raise ValueError("Debe ingresar un número válido.")

            n = int(n)
            break  # Salir del bucle si el valor es válido
        except ValueError as e:
            print(f"[red]{e}[/red]")
            print("[yellow]Por favor, intente de nuevo.[/yellow]")

    if dist == "Uniforme":
        while True:
            try:
                a = inquirer.text(message="Valor de [a]:").execute()
                if not a.strip() or not a.replace('.', '', 1).isdigit():
                    raise ValueError("Debe ingresar un número válido para a.")
                a = float(a)

                b = inquirer.text(message="Valor de [b]:").execute()
                if not b.strip() or not b.replace('.', '', 1).isdigit():
                    raise ValueError("Debe ingresar un número válido para b.")
                b = float(b)

                if a >= b:
                    raise ValueError("El valor de a debe ser menor que b.")

                break  # Salir del bucle si ambos valores son válidos
            except ValueError as e:
                print(f"[red]{e}[/red]")
                print("[yellow]Por favor, intente de nuevo.[/yellow]")

        muestra = uniform_gen(a, b, n)
    elif dist == "Exponencial":
        while True:
            try:
                mu = inquirer.text(message="Valor de mu (media):").execute()
                if not mu.strip() or not mu.replace('.', '', 1).isdigit():
                    raise ValueError("Debe ingresar un número válido para mu.")
                mu = float(mu)

                if mu <= 0:
                    raise ValueError("La media debe ser mayor a 0.")

                break  # Salir del bucle si el valor es válido
            except ValueError as e:
                print(f"[red]{e}[/red]")
                print("[yellow]Por favor, intente de nuevo.[/yellow]")

        muestra = exponencial_gen(mu, n)

    elif dist == "Normal":
        while True:
            try:
                # Validación para la media (μ)
                mu = inquirer.text(message="Valor de mu (media):").execute()
                if not mu.strip() or not mu.replace('.', '', 1).replace('-', '', 1).isdigit():
                    raise ValueError("Debe ingresar un número válido para mu.")
                mu = float(mu)

                # Validación para la desviación estándar (σ)
                sigma = inquirer.text(message="Valor de sigma (desviación estándar):").execute()
                if not sigma.strip() or not sigma.replace('.', '', 1).isdigit():
                    raise ValueError("Debe ingresar un número válido para sigma.")
                sigma = float(sigma)

                if sigma <= 0:
                    raise ValueError("La desviación estándar (sigma) debe ser mayor a 0.")

                break  # Salir del bucle si ambos valores son válidos
            except ValueError as e:
                print(f"[red]{e}[/red]")
                print("[yellow]Por favor, intente de nuevo.[/yellow]")

    muestra = normal_gen(mu, sigma, n)

    while True:
        opcion = inquirer.select(
            message="¿Qué deseas hacer ahora?",
            choices=[
                "Ver primeros 10 valores",
                "Ver todos los valores",
                "Ver tabla de frecuencias",
                "Ver histograma gráfico",
                "Salir"
            ]
        ).execute()

        if opcion == "Ver primeros 10 valores":
            table = Table(title=f"Primeros 10 valores - {dist}")
            table.add_column("Índice", style="cyan")
            table.add_column("Valor", style="magenta")
            for i, val in enumerate(muestra[:10]):
                table.add_row(str(i), str(val))
            print(table)

        elif opcion == "Ver todos los valores":
            mostrar_todos(muestra)

        elif opcion == "Ver tabla de frecuencias":
            k = int(inquirer.select(
                message="¿Cuántos intervalos?",
                choices=["10", "15", "20", "25"]
            ).execute())
            tabla_frecuencias(muestra, k)

        elif opcion == "Ver histograma gráfico":
            k = int(inquirer.select(
                message="¿Cuántos intervalos?",
                choices=["10", "15", "20", "25"]
            ).execute())
            graficar_histograma(muestra, k)

        elif opcion == "Salir":
            print("[green]Gracias por usar el generador. ¡Hasta luego![/green]")
            break

if __name__ == "__main__":
    app()
