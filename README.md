# PIMU-project

This repository contains message-parser.py script.
It was intended to parse big text files with potentially unsafe message queries into large number of formatted files, each within its author and his or her messages.

Usage:
message_parser.py [-h] first_file_number filename
Arguments:
first_file_number - integer, needed for processed file naming system compliance.
filename - name of the file with long message queries.
Usage example:
python message_parser.py 5487 orig24.txt > meta10.txt

Script application results:
Source text data with 10 huge unreadable files populated into 10 archives with additional metadata, collected during parsing.
These archives contain lots of text files with small and processed contents, attached images and sounds as separate files, connected by file naming system.
