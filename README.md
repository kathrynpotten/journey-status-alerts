# Tube Delay Status

Script for scraping tube line status from TfL and parsing that status based on personal route.

This can then be run in the a-Shell app as part of an Apple Shortcut to create an automated update message for a commuter.
At specified time (e.g. morning/evening before expected commute time), the script is run in the a-Shell extension. Shortcuts extracts the created file from a-Shell and sends the contents (the 'delay status message') to a chosen contact as a message.
