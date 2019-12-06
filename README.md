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

### Example Invocation
Below is an invocation with the short form command line parameters, and corresponding output using all the available command line parameters:
```
$ ./albgen.py -t 1 -m 100 -i 10 -e Locrian -e Lydian -a 200 -n 100 -o human
1 - Your Strange Tradition (2:44)
A Smooth, Dull, Happy track in 4/4,
The key of F Dorian at 20bpm.

$ ./albgen.py --track_count 2 --max_bpm 200 --min_bpm 100 --exclude_mode Ionian --exclude_mode Aeolian --max_length 300 --min_length 200 --output_format csv
"Track","Title","Tempo/BPM","Time Signature","Length/s","Key","Mode","Colour","Mood","Texture"
"1","The Real People","156","7/8","274","Eb","Locrian","Dull","Melancholy","Rough"
"2","A Faithful Kiss","146","7/8","250","C","Mixolydian","Brilliant","Sad","Natural"
```
