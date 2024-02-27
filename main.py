import csv
from convertor import distance as d, temperature as t
import re
from pathlib import Path


def read_file(file: str):
    with open(file) as f:
        data = [line for line in csv.reader(f)]
    return data


def write_to_file(data: list, filename: str):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file, quoting=csv.QUOTE_NONE, escapechar='\\', quotechar='\'')
        writer.writerows(data)


def format_string(string: str) -> str:
    return f'"{string}"'


def extract_digits(string: str) -> float:
    return float(re.search(r'(\d+)', string).group())


def extract_paramter(string: str) -> str:
    return re.search(r'([a-z]+)', string, re.IGNORECASE).group()


def convert_temperature(temperature_str: str, target_parameter: str) -> str:
    target_parameter = target_parameter.lower()
    current_parameter = extract_paramter(temperature_str).lower()

    if current_parameter == target_parameter:
        return format_string(temperature_str)
    else:
        number_to_convert = extract_digits(temperature_str)
        if target_parameter == 'c':
            converted_number = t.fahrenheit_to_celsius(number_to_convert)
            return format_string(f'{converted_number}°C')
        elif target_parameter == 'f':
            converted_number = t.celsius_to_fahrenheit(number_to_convert)
            return format_string(f'{converted_number}°F')


def convert_distance(distance_str: str, target_parameter: str) -> str:
    target_parameter = target_parameter.lower()
    current_parameter = extract_paramter(distance_str).lower()

    if current_parameter == target_parameter:
        return format_string(distance_str)
    else:
        number_to_convert = extract_digits(distance_str)
        if target_parameter == 'ft':
            converted_number = d.meters_to_feet(number_to_convert)
            return format_string(f'{converted_number}ft')
        elif target_parameter == 'm':
            converted_number = d.feet_to_meters(number_to_convert)
            return format_string(f'{converted_number}m')


# need to handle possible errors and edge cases
def convert_parameters(data, distance_parameter: str, temperature_parameter: str):
    converted_data = []
    for line in data:
        converted_line = []
        # this is dataset header
        if data.index(line) == 0:
            converted_data.append(line)
        else:
            date, distance, temperature = line
            converted_line.append(date)
            converted_line.append(convert_distance(distance, distance_parameter))
            converted_line.append(convert_temperature(temperature, temperature_parameter))
            converted_data.append(converted_line)
    return converted_data


data = read_file("dataset.csv")
new_data = convert_parameters(data, distance_parameter='ft', temperature_parameter='C')

Path("./out").mkdir(parents=True, exist_ok=True)
write_to_file(new_data, 'out/converted_data.csv')