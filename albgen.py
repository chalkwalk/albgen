#!/usr/bin/python3
"""A tool to generate a human readable brief for making an album. """

from random import gauss
from random import random

import os
import argparse

modes = ['lydian', 'ionian', 'mixolydian', 'dorian', 'aeolian', 'phrygian',
        'locrian']

parser = argparse.ArgumentParser(description='Generate an album listing.')

parser.add_argument('--track_count', '-t', metavar='COUNT', type=int, default=12, help='Show many tracks the album will have.')
parser.add_argument('--max_bpm', '-m', type=int, default=150, help='The fastest BPM to suggest.')
parser.add_argument('--min_bpm', '-i', type=int, default=70, help='The slowest BPM to suggest.')
parser.add_argument('--exclude_mode', '-e', metavar='MODE', action='append', default=[], choices=modes, type=lambda s: s.lower(), help='(Repeated) A musical mode to exclude.')
parser.add_argument('--max_length', '-a', metavar='MAX_LEN', type=int, default=150, help='The longest track to suggest in seconds.')
parser.add_argument('--min_length', '-n', metavar='MIN_LEN', type=int, default=70, help='The shortest track to suggest in seconds.')
parser.add_argument('--output_format', '-o', metavar='TYPE', type=lambda s: s.lower(), choices=['human', 'yaml', 'csv'], default='human', help='The format to output the album listing.')
args = parser.parse_args()


def PathCanonicalize(filename):
  if os.path.isabs(filename):
    return filename
  else:
    return os.path.join(os.path.dirname(__file__), filename)


def LoadWordList(filename):
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
  bpm_range = args.max_bpm - args.min_bpm
  return round(args.min_bpm + bpm_range * number)

def ListNumberToString(words, number):
  index = int(number * len(words))
  if index < 0: index = 0
  if index >= len(words): index = len(words) - 1
  return words[index]

def NumberToKey(number):
  return ListNumberToString([
      'C', 'C', 'C#', 'Db', 'D', 'D', 'D#', 'Eb', 'E', 'E', 'F', 'F', 'F#',
      'Gb', 'G', 'G', 'G#', 'Ab', 'A', 'A', 'A#', 'Bb', 'B', 'B'
  ], number)


def NumberToMode(number):
  return ListNumberToString(
          [x for x in modes if x not in args.exclude_mode], number)


def NumberToColour(number):
  return ListNumberToString([
      'brilliant', 'bright', 'neutral', 'dull', 'dark'
  ], number)


def NumberToMood(number):
  return ListNumberToString([
      'ecstatic', 'happy', 'calm', 'mellow', 'melancholy', 'sad', 'devastated'
  ], number)


def NumberToTimeSignature(number):
  return ListNumberToString(['2/4', '3/4', '4/4', '7/8', '5/4'], number)


def NumberToTexture(number):
  return ListNumberToString(['gritty', 'rough', 'natural', 'smooth'], number)


def SecondsToMinutes(seconds):
  return '%d:%02d' % (seconds/60, seconds % 60)


def NumberToLength(number):
  length_range = args.max_length - args.min_length
  length_in_seconds = round(args.min_length + length_range * number)
  return length_in_seconds


def NumberToArticle(number):
  return ListNumberToString([
      'my', 'your', 'his', 'her', 'our', 'their', 'the', 'the', 'the', 'a', 'a',
      'a', None, None, None, None
  ], number)


def NumberToAdjective(number):
  return ListNumberToString(adjectives, number)


def NumberToNoun(number):
  return ListNumberToString(nouns, number)


def NumberToNoun(number):
  return ListNumberToString(nouns, number)


def PluraliseNoun(noun):
  word = noun.lower()
  if word.endswith('fe'):
    return noun[:-2] + 'ves'
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
  if word.endswith('ay'):
    return noun + 's'
  if word.endswith('y'):
    return noun[:-1] + 'ies'
  if word.endswith('cs') or word.endswith('ws'):
    return noun
  return noun + 's'


def GetTrackTitle(track):
    title = ''
    article = NumberToArticle(track['article'])
    adjective = NumberToAdjective(track['adjective']).capitalize()
    noun = NumberToNoun(track['noun']).capitalize()
    if article:
      article = article.capitalize()
      if article == 'A' and adjective[0] in ['A', 'E', 'I', 'O', 'U']:
        title = article + 'n '
      else:
        title = article + ' '
    title += adjective + ' '
    probability_of_plural = 0.3
    if track['plural'] < probability_of_plural and article != 'A':
      title += PluraliseNoun(noun)
    else:
      title += noun
    return title


def GetCyclicDistance(a, b):
  return min(abs(a - b), abs(a - b - 1), abs(a - b + 1))


def GetDistance(v, w):
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


def GenerateAlbum(track_count):
  tracks = []
  for track in range(0, track_count):
    tracks.append({
        'key': GetUniformRandom(),
        'tempo': GetGaussRandom(),
        'mode': GetUniformRandom(),
        'colour': GetUniformRandom(),
        'mood': GetUniformRandom(),
        'time': GetGaussRandom(),
        'length': GetGaussRandom(),
        'article': GetUniformRandom(),
        'adjective': GetUniformRandom(),
        'noun': GetUniformRandom(),
        'plural': GetUniformRandom(),
        'texture': GetUniformRandom(),
    })
  return GetBestPermutation(tracks)


def GenerateAlbumCSVText(album):
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


def GenerateAlbumHumanText(album):
  output = ''
  for index, track in enumerate(album):
    output += '%s - %s (%s)\n' % (index + 1, GetTrackTitle(track), SecondsToMinutes(NumberToLength(track['length'])))
    output += 'A %s, %s, %s track in %s,\n' % (NumberToTexture(track['texture']).capitalize(), NumberToColour(track['colour']).capitalize(), NumberToMood(track['mood']).capitalize(), NumberToTimeSignature(track['time']))
    output += 'The key of %s %s at %sbpm.\n' % (NumberToKey(track['key']), NumberToMode(track['mode']).capitalize(), NumberToBPM(track['tempo']))
    output += '\n'
  return output


def GenerateAlbumText(album, output_format):
  if output_format == 'csv':
    return GenerateAlbumCSVText(album)
  if output_format == 'yaml':
    return GenerateAlbumYAMLText(album)
  if output_format == 'human':
    return GenerateAlbumHumanText(album)


def main():
  album = GenerateAlbum(args.track_count)
  print(GenerateAlbumText(album, args.output_format), end='')

if __name__ == '__main__':
  main()
