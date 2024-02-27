import csv
from convertor import distance as d, temperature as t
import re


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


def convert_temperature(temperature_str: str, target_parameter: str) -> str:
    current_parameter = temperature_str[-1:]
    if current_parameter.lower() == target_parameter.lower():
        return format_string(temperature_str)
    else:
        number_to_convert = int(temperature_str[:-2])
        if target_parameter.lower() == 'c':
            converted_number = t.fahrenheit_to_celsius(number_to_convert)
            return format_string(f'{converted_number}°C')
        elif target_parameter.lower() == 'f':
            converted_number = t.celsius_to_fahrenheit(number_to_convert)
            return format_string(f'{converted_number}°F')


def convert_distance(distance_str: str, target_parameter: str) -> str:
    current_parameter = distance_str[-1:]
    if current_parameter.lower() == target_parameter[-1:].lower():
        return distance_str
    else:
        if target_parameter.lower() == 'ft':
            number_to_convert = int(distance_str[:-1])
            converted_number = d.meters_to_feet(number_to_convert)
            return format_string(f'{converted_number}ft')
        elif target_parameter.lower() == 'm':
            number_to_convert = int(distance_str[:-2])
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
write_to_file(new_data, 'out/converted_data.csv')