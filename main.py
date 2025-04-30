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

    n = int(inquirer.number(
        message="¿Tamaño de muestra? (hasta 1.000.000):",
        validate=lambda x: 0 < int(x) <= 1_000_000,
        default=1000
    ).execute())

    if dist == "Uniforme":
        a = float(inquirer.text(message="Valor de [a]:").execute())
        b = float(inquirer.text(message="Valor de [b]:").execute())
        muestra = uniform_gen(a, b, n)

    elif dist == "Exponencial":
        mu = float(inquirer.text(message="Valor de mu (media):").execute())
        if mu <= 0:
            print("[red]La media debe ser mayor a 0.[/red]")
            raise typer.Abort()
        muestra = exponencial_gen(mu, n)

    elif dist == "Normal":
        mu = float(inquirer.text(message="Valor de mu (media):").execute())
        sigma = float(inquirer.text(message="Valor de sigma (desviación estándar):").execute())
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
