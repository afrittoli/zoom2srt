#!/usr/bin/env python3

from datetime import time, timedelta
import unittest

import zoom2srt

class TestZoom2SRT(unittest.TestCase):

    def test_start(self):
        initial = timedelta(seconds=1)
        message = timedelta(seconds=10)
        expected = timedelta(seconds=9)
        self.assertEqual(zoom2srt.start(message, initial), expected)

    def test_start_message_early(self):
        initial = timedelta(seconds=10)
        message = timedelta(seconds=1)
        with self.assertRaisesRegex(Exception, "Message time 0:00:01 is before"):
            zoom2srt.start(message, initial)

    def test_start_previous(self):
        initial = timedelta(seconds=1)
        message = timedelta(seconds=10)
        previous = timedelta(seconds=11)
        expected = timedelta(seconds=11)
        self.assertEqual(zoom2srt.start(message, initial, previous), expected)

    def test_end(self):
        message = "From a : this is some longish message with several words"
        start = timedelta(seconds=10)
        expected = timedelta(seconds=15)
        self.assertEqual(zoom2srt.end(start, message), expected)

    def test_end_short(self):
        message = "Short"
        start = timedelta(seconds=10)
        expected = timedelta(seconds=11)
        self.assertEqual(zoom2srt.end(start, message), expected)

    def test_end_empty(self):
        message = ""
        start = timedelta(seconds=10)
        expected = start
        self.assertEqual(zoom2srt.end(start, message), expected)

    def test_transform(self):
        message_number = 5
        line = "00:01:30 from a : this is some sample message"
        initial = timedelta(seconds=10)
        expected = (["5", "00:01:20,000 --> 00:01:23,000", "a : this is some sample message"],
                    timedelta(minutes=1, seconds=23))
        self.assertEqual(zoom2srt.transform(line, message_number, initial), expected)

    def test_transform_no_padding(self):
        message_number = 5
        line = "11:01:30 from a : this is some sample message"
        initial = timedelta(seconds=10)
        expected = (["5", "11:01:20,000 --> 11:01:23,000", "a : this is some sample message"],
                    timedelta(hours=11, minutes=1, seconds=23))
        self.assertEqual(zoom2srt.transform(line, message_number, initial), expected)

    def test_transform_previous(self):
        message_number = 5
        line = "00:01:30 from a : this is some sample message"
        initial = timedelta(seconds=10)
        previous = timedelta(seconds=55)
        expected = (["5", "00:01:20,000 --> 00:01:23,000", "a : this is some sample message"],
                    timedelta(minutes=1, seconds=23))
        self.assertEqual(zoom2srt.transform(line, message_number, initial, previous), expected)

    def test_transform_previous_overlap(self):
        message_number = 5
        line = "00:01:30 from a : this is some sample message"
        initial = timedelta(seconds=10)
        previous = timedelta(minutes=1, seconds=22)
        expected = (["5", "00:01:22,000 --> 00:01:25,000", "a : this is some sample message"],
                    timedelta(minutes=1, seconds=25))
        self.assertEqual(zoom2srt.transform(line, message_number, initial, previous), expected)

if __name__ == '__main__':
    unittest.main()