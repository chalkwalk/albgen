#!/usr/bin/python3
"""A tool to generate a human readable brief for making an album. """

from random import gauss
from random import random

import os
import argparse

modes = ['lydian', 'ionian', 'mixolydian', 'dorian', 'aeolian', 'phrygian',
        'locrian']

parser = argparse.ArgumentParser(description='Generate an album listing.')

parser.add_argument('--track_count', '-t', metavar='COUNT', default=0, type=int, help='Show many tracks the album will have (use this or album_length).')
parser.add_argument('--album_length', '-a', metavar='TIME', default=0, type=int, help='How long the album should be in seconds (use this or track_count).')
parser.add_argument('--max_bpm', '-m', type=int, default=150, help='The fastest BPM to suggest.')
parser.add_argument('--min_bpm', '-i', type=int, default=70, help='The slowest BPM to suggest.')
parser.add_argument('--exclude_mode', '-e', metavar='MODE', action='append', default=[], choices=modes, type=lambda s: s.lower(), help='(Repeated) A musical mode to exclude.')
parser.add_argument('--max_length', '-x', metavar='MAX_LEN', type=int, default=330, help='The longest track to suggest in seconds.')
parser.add_argument('--min_length', '-n', metavar='MIN_LEN', type=int, default=150, help='The shortest track to suggest in seconds.')
parser.add_argument('--output_format', '-o', metavar='TYPE', type=lambda s: s.lower(), choices=['human', 'yaml', 'csv', 'html', 'www'], default='human', help='The format to output the album listing.')

args = parser.parse_args()

if args.track_count > 0 and args.album_length > 0:
  raise Exception('You may no specify track_count and album_length.')


def PathCanonicalize(filename):
  # Given a path, if it's absolute, return it, if it's relative, assume it's
  # relative to the directory containing the executable.
  if os.path.isabs(filename):
    return filename
  else:
    return os.path.join(os.path.dirname(__file__), filename)


def LoadWordList(filename):
  # Load the lines of a file into a list and return it.
  file_path = PathCanonicalize(filename)
  with open(file_path, 'r') as file:
    words = [word.strip() for word in file.readlines()]
    return words


adjectives = LoadWordList('data/adjectives.txt')

nouns = LoadWordList('data/nouns.txt')


def GetUniformRandom():
  return random()


def GetGaussRandom():
  return (gauss(0, 1) + 3.0) / 6.0


def NumberToBPM(number):
  # Given a number (approximately) in the unit interval, return a BPM based on
  # the command line arguments.
  bpm_range = args.max_bpm - args.min_bpm
  return round(args.min_bpm + bpm_range * number)


def PDFNumberToString(words, number):
  # Given a list of tuples (word, weight) and a number (approximately) in the
  # unit interval return a word from the list using weight as the relative
  # probability of each word.
  pdf_sum = 0.0
  for (_, b) in words:
    pdf_sum += b
  limit = pdf_sum * number
  pdf_partial_sum = 0.0
  for (a, b) in words:
    pdf_partial_sum += b
    if pdf_partial_sum >= limit:
      return a
  # This is here to handle numbers > 1.0 (in case we used a gaussian probability)
  return words[-1][0]


def ListNumberToString(words, number, probability_of_none=0.0):
  # Given a list of words, a number (approximately) in the unit interval and a
  # probability of none return a word from the list based on the number or None
  # based on the probability.
  if probability_of_none < 1.0:
    scaled_number = number * (1.0 / (1.0 - probability_of_none))
  else:
    return None
  if scaled_number > 1.0: return None
  if isinstance(words[0], tuple):
    # If the probabilities are weighted, handle it appropriately.
    return PDFNumberToString(words, number)
  else:
    index = int(number * len(words))
    if index < 0: index = 0
    if index >= len(words): index = len(words) - 1
    return words[index]

def NumberToKey(number):
  # Given a number in the unit interval return a corresponding musical note.
  return ListNumberToString([
      'Cb', 'C', 'C#', 'Db', 'D', 'D', 'D#', 'Eb', 'E', 'E#', 'Fb', 'F', 'F#',
      'Gb', 'G', 'G', 'G#', 'Ab', 'A', 'A', 'A#', 'Bb', 'B', 'B#'
  ], number)


def NumberToMode(number):
  # Given a number in the unit interval return a corresponding musical mode.
  return ListNumberToString(
          [x for x in modes if x not in args.exclude_mode], number)


def NumberToColour(number):
  # Given a number in the unit interval return a corresponding adjectival musical colour.
  return ListNumberToString([
      'brilliant', 'bright', 'neutral', 'dull', 'dark'
  ], number)


def NumberToMood(number):
  # Given a number in the unit interval return a corresponding adjectival musical mood.
  return ListNumberToString([
      'ecstatic', 'happy', 'calm', 'mellow', 'melancholy', 'sad', 'devastated'
  ], number)


def NumberToTimeSignature(number):
  # Given a number in the unit interval return a corresponding musical time signature.
  return ListNumberToString([
      ('2/4', 1), ('3/4', 20), ('4/4', 68), ('7/8', 8), ('5/4', 3)], number)


def NumberToTexture(number):
  # Given a number in the unit interval return a corresponding adjectival musical texture.
  return ListNumberToString(['gritty', 'rough', 'natural', 'smooth'], number)


def SecondsToMinutes(seconds):
  # Given a number in seconds, return a corresponding string in minutes and seconds.
  return '%d:%02d' % (seconds/60, seconds % 60)


def NumberToLength(number):
  # Given a number (approximately) in the unit interval, return a track length
  # in seconds based on the command line arguments.
  length_range = args.max_length - args.min_length
  length_in_seconds = round(args.min_length + length_range * number)
  return length_in_seconds


def NumberToArticle(number, probability_of_none=0.2):
  # Given a number in the unit interval and probability return an article or none.
  return ListNumberToString([
      ('my', 1), ('your', 1), ('his', 1), ('her', 1), ('our', 1),
      ('their', 1), ('the', 3), ('a', 3)
  ], number, probability_of_none)


def NumberToAdjective(number, probability_of_none=0.05):
  # Given a number in the unit interval and probability return an adjective or none.
  return ListNumberToString(adjectives, number, probability_of_none)


def NumberToNoun(number, probability_of_none=0.01):
  # Given a number in the unit interval and probability return a noun or none.
  return ListNumberToString(nouns, number, probability_of_none)


def PluraliseNoun(noun):
  # Given a noun, return its plural.
  word = noun.lower()
  if word.endswith('fe'):
    return noun[:-2] + 'ves'
  if word.endswith('ff'):
    return noun
  if word.endswith('f'):
    return noun[:-1] + 'ves'
  if word.endswith('o') or word.endswith('x'):
    return noun + 'es'
  if word.endswith('us'):
    return noun[:-2] + 'i'
  if word.endswith('is'):
    return noun[:-2] + 'es'
  if word.endswith('on') and not (word.endswith('ion') or word.endswith('son')):
    return noun[:-2] + 'a'
  if word.endswith('sh') or word.endswith('ch') or word.endswith('ss'):
    return noun + 'es'
  if word.endswith('ay') or word.endswith('oy'):
    return noun + 's'
  if word.endswith('y'):
    return noun[:-1] + 'ies'
  if word.endswith('cs') or word.endswith('ws'):
    return noun
  return noun + 's'


def ArticleCorrection(article, next_word):
  # Given an article and the following return cover 'A' to 'An' if necessary.
  if article == 'A' and next_word[0] in ['A', 'E', 'I', 'O', 'U']:
    return article + 'n'
  else:
    return article


def GetTrackTitle(track):
  # Given a track definition object, return the corresponding track title.
  title = ''
  noun = NumberToNoun(track['noun'])
  if noun:
    # Noun
    noun = noun.capitalize()
    adjective = NumberToAdjective(track['adjective'])
    if adjective:
      # Noun and Adjective
      adjective = adjective.capitalize()
      article = NumberToArticle(track['article'])
      if article:
        # Noun, Adjective & Article
        article = ArticleCorrection(article.capitalize(), adjective)
    else:
      # Noun and No Adjective
      article = NumberToArticle(track['article'])
      if article:
        # Noun, No Adjective & Article
        article = ArticleCorrection(article.capitalize(), noun)
  else:
    # No Noun
    adjective = NumberToAdjective(track['adjective'], 0.0).capitalize()
    article = 'The'

  probability_of_plural = 0.3
  if noun and track['plural'] < probability_of_plural and ((article and article[0] != 'A') or not article):
    noun = PluraliseNoun(noun)
  title_words = []
  if article:
    title_words.append(article)
  if adjective:
    title_words.append(adjective)
  if noun:
    title_words.append(noun)
  return ' '.join(title_words)


def GetCyclicDistance(a, b):
  # Given two numbers in a toral unit interval, return their minimum distance.
  return min(abs(a - b), abs(a - b - 1), abs(a - b + 1))


def GetDistance(v, w):
  # Given a pair of track definitions, return the distance between them.
  distance_sum = 0.0
  distance_sum += abs(v['colour'] - w['colour']) * 10
  distance_sum += abs(v['mood'] - w['mood']) * 8
  distance_sum += abs(v['tempo'] - w['tempo']) * 6
  distance_sum += GetCyclicDistance(v['key'], w['key']) * 5
  distance_sum += GetCyclicDistance(v['mode'], w['mode']) * 3
  distance_sum += abs(v['texture'] - w['texture']) * 2
  distance_sum += abs(v['length'] - w['length']) * 1
  distance_sum += abs(v['time'] - w['time']) * -1
  distance_sum += abs(v['plural'] - w['plural']) * -2
  distance_sum += abs(v['noun'] - w['noun']) * -3
  distance_sum += abs(v['adjective'] - w['adjective']) * -3
  distance_sum += abs(v['article'] - w['article']) * -5
  return distance_sum


def GetBestPermutation(tracks):
  # Given a list of tracks, return an ordering that approximately minimises the
  # sum of the distances between all adjacent tracks.
  best_score = 1000000.0
  best_track_list = None
  for index, track in enumerate(tracks):
    track_list = [track]
    track_set = set(range(len(tracks)))
    track_set.remove(index)
    current_index = index
    current_score = 0.0
    while track_set:
      best_next_score = 1000000.0
      best_index = None
      for inner_index in track_set:
        next_score = GetDistance(tracks[current_index], tracks[inner_index])
        if next_score < best_next_score:
          best_next_score = next_score
          best_index = inner_index
      current_index = best_index
      track_list.append(tracks[current_index])
      track_set.remove(current_index)
      current_score += best_next_score
    if current_score < best_score:
      best_score = current_score
      best_track_list = track_list
  return best_track_list


def AppendTrack(tracks, length):
  # Given a track list and length, generate and append a track of given length
  # to a track listing.
  tracks.append({
      'key': GetUniformRandom(),
      'tempo': GetGaussRandom(),
      'mode': GetUniformRandom(),
      'colour': GetUniformRandom(),
      'mood': GetUniformRandom(),
      'time': GetUniformRandom(),
      'length': length,
      'article': GetUniformRandom(),
      'adjective': GetUniformRandom(),
      'noun': GetUniformRandom(),
      'plural': GetUniformRandom(),
      'texture': GetUniformRandom(),
  })


def GenerateAlbum(track_count, album_length):
  # Given a track count or album length generate an album.
  tracks = []
  if track_count:
    for track in range(0, track_count):
      length = GetGaussRandom()
      AppendTrack(tracks, length)
  else:
    total_time = 0
    average_track_length = (args.max_length + args.min_length) / 4
    maximum_album_length = album_length - average_track_length
    if maximum_album_length < 1:
      maximum_album_length = 1
    while total_time < maximum_album_length:
      length = GetGaussRandom()
      total_time += NumberToLength(length)
      AppendTrack(tracks, length)
  return GetBestPermutation(tracks)


def GenerateAlbumCSVText(album):
  # Given a list of track objects (an album) return a corresponding CSV.
  output = ''
  rows = []
  rows.append(['track', 'title', 'tempo/bpm', 'time signature', 'length/s', 'key', 'mode', 'colour', 'mood', 'texture'])
  for index, track in enumerate(album):
    row = [
      str(index + 1),
      GetTrackTitle(track),
      str(NumberToBPM(track['tempo'])),
      NumberToTimeSignature(track['time']),
      str(NumberToLength(track['length'])),
      NumberToKey(track['key']),
      NumberToMode(track['mode']),
      NumberToColour(track['colour']),
      NumberToMood(track['mood']),
      NumberToTexture(track['texture']),
    ]
    rows.append(row)
  for row in rows:
    output += '"' + '","'.join(row) + '"\n'
  return output


def GenerateAlbumYAMLText(album):
  # Given a list of track objects (an album) return corresponding YAML.
  output = 'tracks:\n'
  for index, track in enumerate(album):
    output += '  - track_num: %s\n' % (index + 1)
    output += '    title: %s\n' % GetTrackTitle(track)
    output += '    tempo: %s\n' % NumberToBPM(track['tempo'])
    output += '    time: %s\n' % NumberToTimeSignature(track['time'])
    output += '    length: %s\n' % NumberToLength(track['length'])
    output += '    key: %s\n' % NumberToKey(track['key'])
    output += '    mode %s\n' % NumberToMode(track['mode'])
    output += '    colour %s\n' % NumberToColour(track['colour'])
    output += '    mood: %s\n' % NumberToMood(track['mood'])
    output += '    texture: %s\n' % NumberToTexture(track['texture'])
  return output


def GenerateAlbumHTMLText(album):
  # Given a list of track objects (an album) return corresponding HTML.
  output = '<html>\n'
  output += '  <head>\n'
  output += '    <title>Your Album Listing</title>\n'
  output += '  </head>\n'
  output += '  <body>\n'
  output += '    <h2>Album Listing</h2>\n'
  for index, track in enumerate(album):
    output += '    <h3>%s - %s (%s)</h2>\n' % (index + 1, GetTrackTitle(track), SecondsToMinutes(NumberToLength(track['length'])))
    output += '    <p>\n'
    output += '      A %s, %s, %s track in %s,<br>\n' % (NumberToTexture(track['texture']).capitalize(), NumberToColour(track['colour']).capitalize(), NumberToMood(track['mood']).capitalize(), NumberToTimeSignature(track['time']))
    output += '      The key of %s %s at %sbpm.\n' % (NumberToKey(track['key']), NumberToMode(track['mode']).capitalize(), NumberToBPM(track['tempo']))
    output += '    </p>\n'
  output += '  </body>\n'
  output += '</html>\n'
  return output


def GenerateAlbumWWWText(album):
  # Given a list of track objects (an album) return corresponding HTML with HTTP header.
  output = 'Content-Type: text/html\n\n'
  output += GenerateAlbumHTMLText(album)
  return output


def GenerateAlbumHumanText(album):
  # Given a list of track objects (an album) return corresponding human readable string.
  output = ''
  for index, track in enumerate(album):
    output += '%s - %s (%s)\n' % (index + 1, GetTrackTitle(track), SecondsToMinutes(NumberToLength(track['length'])))
    output += 'A %s, %s, %s track in %s,\n' % (NumberToTexture(track['texture']).capitalize(), NumberToColour(track['colour']).capitalize(), NumberToMood(track['mood']).capitalize(), NumberToTimeSignature(track['time']))
    output += 'The key of %s %s at %sbpm.\n' % (NumberToKey(track['key']), NumberToMode(track['mode']).capitalize(), NumberToBPM(track['tempo']))
    output += '\n'
  return output


def GenerateAlbumText(album, output_format):
  # Given a list of track objects (an album) and output format, return a
  # corresponding string.
  if output_format == 'www':
    return GenerateAlbumWWWText(album)
  if output_format == 'html':
    return GenerateAlbumHTMLText(album)
  if output_format == 'csv':
    return GenerateAlbumCSVText(album)
  if output_format == 'yaml':
    return GenerateAlbumYAMLText(album)
  if output_format == 'human':
    return GenerateAlbumHumanText(album)


def main(): 
  track_count = None
  album_length = None
  if args.track_count < 1 and args.album_length < 1:
    track_count = 12
  else:
    if args.track_count > 0:
      track_count = args.track_count
    else:
      album_length = args.album_length
  album = GenerateAlbum(track_count, album_length)
  print(GenerateAlbumText(album, args.output_format), end='')

if __name__ == '__main__':
  main()
