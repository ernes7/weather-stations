import os
import multiprocessing
import itertools


# define a function to read a single file
def read_weather_file(filename):
    lines = []
    with open(filename) as f:
        # iterate over the lines in the file
        for line in f:
            # split the line on the tab character
            records = line.strip().split("\t")
            records_dict = {
                "date": records[0],
                "max_temp": None if str(records[1]) == "-9999" else int(records[1]),
                "min_temp": None if str(records[2]) == "-9999" else int(records[2]),
                "precipitation": None
                if str(records[3]) == "-9999"
                else int(records[3]),
                # Exclude the file extension from the file name
                "station": filename.split("/")[-1].split(".")[0],
            }
            # Append the dictionary to the array
            lines.append(records_dict)
    return lines


# Use multiprocessing to optimize the reading of the data
def read_weather_data(directory) -> list:
    filenames = os.listdir(directory)
    with multiprocessing.Pool() as pool:
        # map the read_file function to the list of filenames
        results = pool.map(
            read_weather_file,
            [os.path.join(directory, filename) for filename in filenames],
        )
        return list(itertools.chain.from_iterable(results))


def read_yield_data(file) -> list:
    # Initialize an empty array
    records_array = []

    # Open the file in read mode
    with open(file) as file:
        lines = file.readlines()
        # Read each line in the file
        for line in lines:
            # Split the line into separate records using the tab character as the delimiter
            records = line.strip().split("\t")
            # Create a dictionary for the current line using the records and specific keys
            records_dict = {
                "year": None if str(records[0]) == "-9999" else records[0],
                "total_harvested": None
                if str(records[1]) == "-9999"
                else int(records[1]),
            }
            # Append the dictionary to the array
            records_array.append(records_dict)

    return records_array


def analyze(records):
    # Create a dictionary to store the data for each pair
    pairs = {}

    # Extract the year-station pairs and store the data for each pair
    for d in records:
        pair = (d["station"], d["date"].year)
        if pair not in pairs:
            pairs[pair] = {
                "station": pair[0],
                "year": pair[1],
                "max_temps": [],
                "min_temps": [],
                "precipitations": [],
            }
        if d["max_temp"] is not None:
            pairs[pair]["max_temps"].append(d["max_temp"] / 10)
        if d["min_temp"] is not None:
            pairs[pair]["min_temps"].append(d["min_temp"] / 10)
        if d["amount_precipitation"] is not None:
            pairs[pair]["precipitations"].append(d["amount_precipitation"] / 1000)

    # Calculate the averages and totals for each pair
    for pair, data in pairs.items():
        pairs[pair]["avg_max_temp"] = (
            0
            if len(data["max_temps"]) == 0
            else round(sum(data["max_temps"]) / len(data["max_temps"]), 3)
        )
        pairs[pair]["avg_min_temp"] = (
            0
            if len(data["min_temps"]) == 0
            else round(sum(data["min_temps"]) / len(data["min_temps"]), 3)
        )
        pairs[pair]["total_precipitation"] = round(sum(data["precipitations"]), 3)

    # Convert the output to the desired format
    result = [
        {
            "station": data["station"],
            "year": data["year"],
            "avg_max_temp": data["avg_max_temp"],
            "avg_min_temp": data["avg_min_temp"],
            "total_precipitation": data["total_precipitation"],
        }
        for data in pairs.values()
    ]

    # Sort the pairs by station name
    return sorted(result, key=lambda x: x["station"])
