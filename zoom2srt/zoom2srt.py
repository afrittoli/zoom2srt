#!/usr/bin/env python3

from datetime import time, timedelta
import fileinput
import math
import optparse
import sys

def str2timedelta(time_string):
    t = time.fromisoformat(time_string)
    return timedelta(hours=t.hour, minutes=t.minute, seconds=t.second)

def start(message_delta, initial_delta, previous_delta=None):
    if initial_delta > message_delta:
        raise Exception("Message time {} is before the specified initial time {}".format(
            message_delta, initial_delta))
    start_delta = message_delta - initial_delta
    if previous_delta is not None and start_delta < previous_delta:
        # Simple approach to avoid overlapping messages
        start_delta = previous_delta
    return start_delta

def end(start_delta, message):
    # Assuming 150 words per minute, adding
    if not message:
        return start_delta
    words = len(message.split())
    duration = math.ceil(words / 15 * 6)
    return start_delta + timedelta(seconds=duration)

def transform(line, message_number, initial_delta, previous_delta=None):
    section = []
    chat_time_string, _, message = line.split(maxsplit=2)
    # Section number
    section.append("{}".format(message_number))
    # Timestamps
    start_delta = start(str2timedelta(chat_time_string), initial_delta, previous_delta)
    start_padding = "0" if start_delta.total_seconds() < 36000 else ""
    end_delta = end(start_delta, message)
    end_padding = "0" if end_delta.total_seconds() < 36000 else ""
    section.append("{}{},000 --> {}{},000".format(
        start_padding, start_delta, end_padding, end_delta))
    # Subtitle text
    section.append("{}".format(message))
    return section, end_delta

def write_all(input_file, output, initial_time_string):
    line_number = 0
    previous_delta = None
    for line in fileinput.input(input_file):
        if line_number == 0:
            # If initial timestamp is not set, use the timestamp of the first chat message
            if initial_time_string == "":
                initial_time_string = line.split(maxsplit=1)[0]
            initial_delta = str2timedelta(initial_time_string)
        # Skip direct messages
        if '(privately) :' in line:
            continue
        line_number += 1
        section, previous_delta = transform(line, line_number, initial_delta, previous_delta)
        section = ["\n" + x for x in section]
        output.writelines(section)

def main():
    description = "Transform a chat log into an SRT file"
    parser = optparse.OptionParser(description=description)
    parser.add_option("-i", "--input", dest="input_file", action="store", type="string",
                      help="Read zoom chat data from FILENAME. Example format: \"hh:mm:ss    From Guest1 : A kind message to everyone\"")
    parser.add_option("-o", "--output", dest="output_file", action="store", type="string",
                      help="Write SRT data to FILENAME")
    parser.add_option("-t", "--initial-timestamp", dest="timestamp", action="store", type="string",
                      help="Time of the day at which the video content started")

    (options, _) = parser.parse_args()

    if options.output_file:
        with open(target, 'w') as h:
            write_all(options.input_file, h, options.timestamp)
    else:
        write_all(options.input_file, sys.stdout, options.timestamp)

if __name__ == "__main__":
   main()