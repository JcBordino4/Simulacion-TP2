import random
import math
import typer
import matplotlib.pyplot as plt
import scipy.stats as stats
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

Luego, permite:
• Visualizar los valores generados.
• Generar una tabla de frecuencias por intervalos.
• Generar Histograma gráfico (usamos matplotlib).
• Realizar pruebas de bondad de ajuste para la distribucion elegida (con Chi-cuadrado).
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



def prueba_bondad(muestra, k, dist, params):
    minimo = min(muestra)
    maximo = max(muestra)
    ancho_intervalo = (maximo - minimo) / k
    intervalos = [0] * k

    # Contar frecuencias observadas por intervalo
    for valor in muestra:
        idx = int((valor - minimo) / ancho_intervalo)
        if idx == k:  # por si valor == maximo
            idx -= 1
        intervalos[idx] += 1

    frecuencias_observadas = intervalos
    n = len(muestra)

    # Calcular frecuencias esperadas según la distribución elegida
    frecuencias_esperadas = []
    for i in range(k):
        li = minimo + i * ancho_intervalo
        ls = li + ancho_intervalo

        if dist == "Uniforme":
            a, b = params
            prob = stats.uniform.cdf(ls, loc=a, scale=b - a) - stats.uniform.cdf(li, loc=a, scale=b - a)

        elif dist == "Exponencial":
            mu, = params
            prob = stats.expon.cdf(ls, scale=mu) - stats.expon.cdf(li, scale=mu)

        elif dist == "Normal":
            mu, sigma = params
            prob = stats.norm.cdf(ls, loc=mu, scale=sigma) - stats.norm.cdf(li, loc=mu, scale=sigma)

        else:
            raise ValueError("Distribución no soportada.")

        frecuencias_esperadas.append(prob * n)

    # Ajustar las frecuencias esperadas para que sumen igual que las observadas
    suma_obs = sum(frecuencias_observadas)
    suma_esp = sum(frecuencias_esperadas)
    frecuencias_esperadas = [fe * suma_obs / suma_esp for fe in frecuencias_esperadas]

    # --- 1) Mostrar tabla original ---
    table_original = Table(title=f"Tabla Original Chi-Cuadrado (k={k})")
    table_original.add_column("Intervalo", style="cyan", justify="center")
    table_original.add_column("Fo", style="magenta", justify="right")
    table_original.add_column("Fe", style="yellow", justify="right")
    table_original.add_column("(Fo-Fe)²/Fe", style="green", justify="right")

    for i in range(k):
        li = round(minimo + i * ancho_intervalo, 4)
        ls = round(li + ancho_intervalo, 4)
        fo = frecuencias_observadas[i]
        fe = frecuencias_esperadas[i]
        chi_i = (fo - fe) ** 2 / fe if fe != 0 else 0

        table_original.add_row(
            f"[{li}, {ls})",
            str(fo),
            f"{fe:.2f}",
            f"{chi_i:.4f}"
        )

    print(table_original)

    # --- 2) Agrupar intervalos con Fe < 5 ---
    fo_agrup = []
    fe_agrup = []
    intervalos_agrupados = []
    chi2_acum = 0

    acumulado_fo = 0
    acumulado_fe = 0
    li_actual = minimo

    for i in range(k):
        acumulado_fo += frecuencias_observadas[i]
        acumulado_fe += frecuencias_esperadas[i]

        # Cuando la Fe acumulada es >= 5, cerramos el intervalo agrupado
        if acumulado_fe >= 5:
            ls_actual = minimo + (i + 1) * ancho_intervalo
            intervalos_agrupados.append((round(li_actual,4), round(ls_actual,4)))
            fo_agrup.append(acumulado_fo)
            fe_agrup.append(acumulado_fe)
            acumulado_fo = 0
            acumulado_fe = 0
            li_actual = ls_actual

    # Si quedó algo sin agrupar, agregarlo al último intervalo
    if acumulado_fe > 0:
        if intervalos_agrupados:
            # fusionar con el último intervalo
            ult_li, ult_ls = intervalos_agrupados[-1]
            intervalos_agrupados[-1] = (ult_li, round(minimo + k * ancho_intervalo,4))
            fo_agrup[-1] += acumulado_fo
            fe_agrup[-1] += acumulado_fe
        else:
            # si no había intervalos (caso raro)
            intervalos_agrupados.append((round(li_actual,4), round(minimo + k * ancho_intervalo,4)))
            fo_agrup.append(acumulado_fo)
            fe_agrup.append(acumulado_fe)

    # --- 3) Mostrar tabla con intervalos agrupados ---
    table_agrup = Table(title=f"Tabla Agrupada Chi-Cuadrado (sin Fe < 5)")
    table_agrup.add_column("Intervalo", style="cyan", justify="center")
    table_agrup.add_column("Fo", style="magenta", justify="right")
    table_agrup.add_column("Fe", style="yellow", justify="right")
    table_agrup.add_column("(Fo-Fe)²/Fe", style="green", justify="right")
    table_agrup.add_column("Chi² Acum.", style="bold", justify="right")

    for i in range(len(fo_agrup)):
        fo = fo_agrup[i]
        fe = fe_agrup[i]
        chi_i = (fo - fe) ** 2 / fe if fe != 0 else 0
        chi2_acum += chi_i

        li, ls = intervalos_agrupados[i]
        intervalo_str = f"[{li}, {ls})"
        table_agrup.add_row(
            intervalo_str,
            str(fo),
            f"{fe:.2f}",
            f"{chi_i:.4f}",
            f"{chi2_acum:.4f}"
        )

    print(table_agrup)

    # --- 4) Resultado final usando scipy para comparar (con intervalos agrupados) ---
    chi2, p_valor = stats.chisquare(f_obs=fo_agrup, f_exp=fe_agrup)

    # Determinar grados de libertad
    k_agrup = len(fo_agrup)
    if dist == "Normal":
        m = 2
    else:
        m = 1
    v = k_agrup - 1 - m

    print(Panel(f"""
[bold]Prueba de bondad de ajuste Chi-Cuadrado (intervalos agrupados)[/bold]

Valor Chi² calculado: [cyan]{chi2:.4f}[/cyan]
Valor-p: [cyan]{p_valor:.4f}[/cyan]
Grados de libertad (v): [cyan]{v}[/cyan]  →  v = k - 1 - m  (donde k = {k_agrup}, m = {m})

{"[green]No se rechaza[/green]" if p_valor > 0.05 else "[red]Se rechaza[/red]"} la hipótesis nula de que la muestra proviene de una distribución {dist.lower()}.

[bold][underline]¿Qué significa esto?[/underline][/bold]

El valor Chi² indica cuánto difieren las frecuencias observadas de las esperadas según la distribución teórica.
El valor-p representa la probabilidad de obtener una diferencia igual o mayor a la observada, 
si la muestra realmente sigue esa distribución. 
Un valor-p alto (mayor a 0.05) sugiere que la diferencia es pequeña y puede deberse al azar, 
por lo tanto no se rechaza la hipótesis nula.
""", title="Resultado Chi-Cuadrado", expand=False))



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
                validate=lambda x: 0 <= int(x) < 1000000,
                default=1000
            ).execute()

            n = int(n)
            break  # Salir del bucle si el valor es válido
        except ValueError as e:
            print(f"[red]{e}[/red]")
            print("[yellow]Por favor, intente de nuevo.[/yellow]")

    if dist == "Uniforme":
        while True:
            try:
                a = float(inquirer.text(message="Valor de [a]:").execute())
                b = float(inquirer.text(message="Valor de [b]:").execute())

                if a >= b:
                    raise ValueError("El valor de a debe ser menor que b.")

                break
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
                "Realizar prueba Chi-Cuadrado",
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

        elif opcion == "Realizar prueba Chi-Cuadrado":
            k = int(inquirer.select(
                message="¿Cuántos intervalos para la prueba?",
                choices=["10", "15", "20", "25"]
            ).execute())

            if dist == "Uniforme":
                params = (a, b)
            elif dist == "Exponencial":
                params = (mu,)
            elif dist == "Normal":
                params = (mu, sigma)

            prueba_bondad(muestra, k, dist, params)

        elif opcion == "Salir":
            print("[green]Gracias por usar el generador. ¡Hasta luego![/green]")
            break


if __name__ == "__main__":
    app()
