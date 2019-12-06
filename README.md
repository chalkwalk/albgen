# Albgen

**TL;DR**: This is a simple tool used to generate a random track listing for an album.`
```
* ./albgen.py -h  # Some basic help.
* ./albgen.py     # Generate a random album prompt using the default parameters.
```

## Introduction
I recently found myself making very similar music, time after time. I'd fall into the same keys, times, tempos and modes and wanted to help inspire myself to branch out. To that end I created a simple tool to generate a random suggestion for an album (or at least a list of tracks). I used this tool as a guide in the creation of [an album](http://chalkwalk.bandcamp.com/album/cautious-solutions) which I made (start to finish) in 4 days over a long Thanksgiving weekend. Beyond the interest in the album, a number of people expressed an interest in the tool, as such I'm publishing it for anyone to use.

## Usage
The help should provide sufficient details and the defaults likely provide usable output, but for completeness the supported arguments are as follows:
```
* -h --help:                     Show usage help.
* -t --track_count (int)COUNT:   How many tracks the album will have.
* -m --max_bpm (int)MAX_BPM:     The fastest BPM to suggest.
* -i --min_bpm (int)MIN_BPM:     The slowest BPM to suggest.
* -e --exclude_mode (str)MODE:   A list of key modes to exclude.
* -a --max_length (int)MAX_LEN:  The longest track to suggest in seconds.
* -n --min_length (int)MIN_LEN:  The shortest track to suggest in seconds.
* -o --output_format (str)TYPE:  The format to output the album listing.
```
```
