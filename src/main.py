import argparse
import json
from typing import List, Dict, Tuple, Union
from datetime import datetime, timedelta


def read_events_from_file(input_file: str) -> Tuple[Dict, datetime, datetime]:
    """
     Read events from a JSON file and return a list of events, and 2 timestamps, the first and the last.
     Having the total duration and the number of events in a minute will make the average calculation more efficient, avoiding repeated calculations
     Parameters:
         input_file (str): Path to the input JSON file.
     Returns:
        events (dict(dict)): A dictionary of dictionaries, where the key is the timestamp, and the inner dictionary is the
        total duration of the events that occurred in that minute, and the number of events that also occurred on that minute.
        first_timestamp (datetime): the first timestamp on the input (rounded down)
        last_timestamp (datetime): the last timestamp on the input (rounded up)
     """
    events = {}
    if input_file:
        with open(input_file, 'r') as file:
            for line in file:
                line = json.loads(line)
                timestamp = datetime.strptime(line['timestamp'], '%Y-%m-%d %H:%M:%S.%f')
                timestamp = timestamp.replace(second=0, microsecond=0)
                if timestamp in events:
                    events[timestamp] = {'total_duration': events[timestamp]['total_duration'] + line['duration'], 'number_of_events': events[timestamp]['number_of_events'] + 1}
                else:
                    events[timestamp] = {'total_duration': line['duration'], 'number_of_events': 1}
    existing_timestamps = list(events)
    # have to round up the last timestamp because we will then search for the previous x minutes
    return events, existing_timestamps[0], existing_timestamps[-1] + timedelta(minutes=1)


def write_to_file(average_time: List[Dict[str, Union[str, float]]], output_file: str = 'output.json') -> None:
    """
    Save moving average delivery times to file.
    Parameters:
        average_time (list): List of dictionaries containing date and average delivery time.
        output_file (str): Path to the output JSON file. Default is 'output.json'.
    """
    with open(output_file, 'w') as file:
        json.dump(average_time, file, indent=2)

    print(f"Moving average delivery times saved to {output_file}")


def calculate_average_specific_timestamp(events: Dict, timestamp: datetime, window_size: int):
    """
     Calculates the moving average for a specific timestamp
     Parameters:
         events (dict(dict)): Dictionary of all the events in the input file
         timestamp (datetime): The timestamp in question to calculate the average for
         window_size (int): The window size, in minutes
     Returns:
        average (int/float): The average for that specific timestamp
     """
    timestamps_to_consider = []
    current_time = timestamp - timedelta(minutes=window_size)
    while current_time < timestamp:
        timestamps_to_consider.append(current_time)
        current_time += timedelta(minutes=1)

    total_duration = 0
    total_events = 0
    for timestamp in timestamps_to_consider:
        event = events.get(timestamp, {})
        total_duration += event.get('total_duration', 0)
        total_events += event.get('number_of_events', 0)

    # To avoid division by zero
    if total_events == 0:
        return total_duration
    return round(total_duration/total_events, 2)


def calculate_moving_average(input_file: str, window_size: int) -> None:
    """
     Calculates the moving average for the specified input file
     Parameters:
         input_file (str): Path to the input file
         window_size (int): The window size, in minutes
     """
    events, first_timestamp, last_timestamp = read_events_from_file(input_file)

    output_timestamps = []
    current_time = first_timestamp
    while current_time <= last_timestamp:
        output_timestamps.append(current_time)
        current_time += timedelta(minutes=1)

    average_delivery_times = []
    for timestamp in output_timestamps:
        average_delivery_times.append({'date': timestamp.strftime('%Y-%m-%d %H:%M:%S'), 'average_delivery_time': calculate_average_specific_timestamp(events, timestamp, window_size)})

    write_to_file(average_delivery_times)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Calculate moving average of translation delivery time.')
    parser.add_argument('--input_file', type=str, help='Path to the input JSON file')
    parser.add_argument('--window_size', type=int, help='Number of minutes to consider for the moving average window')
    args = parser.parse_args()
    input_file, window_size = args.input_file, args.window_size
    calculate_moving_average(input_file=input_file, window_size=window_size)
