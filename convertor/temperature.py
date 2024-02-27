def celsius_to_fahrenheit(number: float) -> float:
    return round(((number * 9/5) + 32), 2)


def fahrenheit_to_celsius(number: float) -> float:
    return round((5/9 * (number - 32)), 2)

