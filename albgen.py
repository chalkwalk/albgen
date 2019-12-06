#!/usr/bin/python3
"""A tool to generate a human readable brief for making an album. """

from random import gauss
from random import random

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


adjectives = [
  'adorable', 'adventurous', 'aggressive', 'agreeable', 'alert', 'alive',
  'amused', 'angry', 'annoyed', 'annoying', 'anxious', 'arrogant', 'ashamed',
  'attractive', 'average', 'awful', 'bad', 'beautiful', 'better', 'bewildered',
  'black', 'bloody', 'blue', 'Blue-eyed', 'blushing', 'bored', 'brainy',
  'brave', 'breakable', 'bright', 'brilliant', 'busy', 'calm', 'careful',
  'cautious', 'charming', 'cheerful', 'clean', 'clear', 'clever', 'cloudy',
  'clumsy', 'colorful', 'combative', 'comfortable', 'concerned', 'condemned',
  'confused', 'cooperative', 'courageous', 'crazy', 'creepy', 'crowded',
  'cruel', 'curious', 'cute', 'dangerous', 'dark', 'dead', 'defeated',
  'defiant', 'delightful', 'depressed', 'determined', 'different', 'difficult',
  'disgusted', 'distinct', 'disturbed', 'dizzy', 'doubtful', 'drab', 'dull',
  'eager', 'easy', 'elated', 'elegant', 'embarrassed', 'enchanting',
  'encouraging', 'energetic', 'enthusiastic', 'envious', 'evil', 'excited',
  'expensive', 'exuberant', 'fair', 'faithful', 'famous', 'fancy', 'fantastic',
  'fierce', 'filthy', 'fine', 'foolish', 'fragile', 'frail', 'frantic',
  'friendly', 'frightened', 'funny', 'gentle', 'gifted', 'glamorous',
  'gleaming', 'glorious', 'good', 'gorgeous', 'graceful', 'grieving',
  'grotesque', 'grumpy', 'handsome', 'happy', 'healthy', 'helpful', 'helpless',
  'hilarious', 'homeless', 'homely', 'horrible', 'hungry', 'hurt', 'ill',
  'important', 'impossible', 'inexpensive', 'innocent', 'inquisitive', 'itchy',
  'jealous', 'jittery', 'jolly', 'joyous', 'kind', 'lazy', 'light', 'lively',
  'lonely', 'long', 'lovely', 'lucky', 'magnificent', 'misty', 'modern',
  'motionless', 'muddy', 'mushy', 'mysterious', 'nasty', 'naughty', 'nervous',
  'nice', 'nonchalant', 'nutty', 'obedient', 'obnoxious', 'odd',
  'Old-fashioned', 'open', 'outrageous', 'outstanding', 'panicky', 'perfect',
  'plain', 'pleasant', 'poised', 'poor', 'powerful', 'precious', 'prickly',
  'proud', 'putrid', 'puzzled', 'quaint', 'real', 'relieved', 'repulsive',
  'rich', 'sad', 'scary', 'selfish', 'shiny', 'shy', 'silly', 'sleepy',
  'smiling', 'smoggy', 'sore', 'sparkling', 'splendid', 'spotless', 'stormy',
  'strange', 'stupid', 'successful', 'super', 'talented', 'tame', 'tasty',
  'tender', 'tense', 'terrible', 'thankful', 'thoughtful', 'thoughtless',
  'tired', 'tough', 'troubled', 'ugliest', 'ugly', 'uninterested', 'unsightly',
  'unusual', 'upset', 'uptight', 'victorious', 'vivacious', 'wandering',
  'weary', 'wicked', 'Wide-eyed', 'wild', 'witty', 'worried', 'worrisome',
  'wrong', 'zany', 'zealous'
]

nouns = [
  'ability', 'abroad', 'abuse', 'access', 'accident', 'account', 'act',
  'action', 'activity', 'actor', 'ad', 'addition', 'address', 'administration',
  'adult', 'advance', 'advantage', 'advertising', 'advice', 'affair', 'affect',
  'afternoon', 'age', 'agency', 'agent', 'agreement', 'air', 'airline',
  'airport', 'alarm', 'alcohol', 'alternative', 'ambition', 'amount',
  'analysis', 'analyst', 'anger', 'angle', 'animal', 'annual', 'answer',
  'anxiety', 'anybody', 'anything', 'anywhere', 'apartment', 'appeal',
  'appearance', 'apple', 'application', 'appointment', 'area', 'argument',
  'arm', 'army', 'arrival', 'art', 'article', 'aside', 'ask', 'aspect',
  'assignment', 'assist', 'assistance', 'assistant', 'associate', 'association',
  'assumption', 'atmosphere', 'attack', 'attempt', 'attention', 'attitude',
  'audience', 'author', 'average', 'award', 'awareness', 'baby', 'back',
  'background', 'bad', 'bag', 'bake', 'balance', 'ball', 'band', 'bank', 'bar',
  'base', 'baseball', 'basis', 'basket', 'bat', 'bath', 'bathroom', 'battle',
  'beach', 'bear', 'beat', 'beautiful', 'bed', 'bedroom', 'beer', 'beginning',
  'being', 'bell', 'belt', 'bench', 'bend', 'benefit', 'bet', 'beyond',
  'bicycle', 'bid', 'big', 'bike', 'bill', 'bird', 'birth', 'birthday', 'bit',
  'bite', 'bitter', 'black', 'blame', 'blank', 'blind', 'block', 'blood',
  'blow', 'blue', 'board', 'boat', 'body', 'bone', 'bonus', 'book', 'boot',
  'border', 'boss', 'bother', 'bottle', 'bottom', 'bowl', 'box', 'boy',
  'boyfriend', 'brain', 'branch', 'brave', 'bread', 'break', 'breakfast',
  'breast', 'breath', 'brick', 'bridge', 'brief', 'broad', 'brother', 'brown',
  'brush', 'buddy', 'budget', 'bug', 'building', 'bunch', 'burn', 'bus',
  'business', 'button', 'buy', 'buyer', 'cabinet', 'cable', 'cake', 'calendar',
  'call', 'calm', 'camera', 'camp', 'campaign', 'can', 'cancel', 'cancer',
  'candidate', 'candle', 'candy', 'cap', 'capital', 'car', 'card', 'care',
  'career', 'carpet', 'carry', 'case', 'cash', 'cat', 'catch', 'category',
  'cause', 'celebration', 'cell', 'chain', 'chair', 'challenge', 'champion',
  'championship', 'chance', 'change', 'channel', 'chapter', 'character',
  'charge', 'charity', 'chart', 'check', 'cheek', 'chemical', 'chemistry',
  'chest', 'chicken', 'child', 'childhood', 'chip', 'chocolate', 'choice',
  'church', 'cigarette', 'city', 'claim', 'class', 'classic', 'classroom',
  'clerk', 'click', 'client', 'climate', 'clock', 'closet', 'clothes', 'cloud',
  'club', 'clue', 'coach', 'coast', 'coat', 'code', 'coffee', 'cold', 'collar',
  'collection', 'college', 'combination', 'combine', 'comfort', 'command',
  'comment', 'commercial', 'commission', 'committee', 'common', 'communication',
  'community', 'company', 'comparison', 'competition', 'complaint', 'complex',
  'computer', 'concentrate', 'concept', 'concern', 'concert', 'conclusion',
  'condition', 'conference', 'confidence', 'conflict', 'confusion',
  'connection', 'consequence', 'consideration', 'consist', 'constant',
  'construction', 'contact', 'contest', 'context', 'contract', 'contribution',
  'control', 'conversation', 'convert', 'cook', 'cookie', 'copy', 'corner',
  'cost', 'count', 'counter', 'country', 'county', 'couple', 'courage',
  'course', 'court', 'cousin', 'cover', 'cow', 'crack', 'craft', 'crash',
  'crazy', 'cream', 'creative', 'credit', 'crew', 'criticism', 'cross', 'cry',
  'culture', 'cup', 'currency', 'current', 'curve', 'customer', 'cut', 'cycle',
  'damage', 'dance', 'dare', 'dark', 'data', 'database', 'date', 'daughter',
  'day', 'dead', 'deal', 'dealer', 'dear', 'death', 'debate', 'debt',
  'decision', 'deep', 'definition', 'degree', 'delay', 'delivery', 'demand',
  'department', 'departure', 'dependent', 'deposit', 'depression', 'depth',
  'description', 'design', 'designer', 'desire', 'desk', 'detail',
  'development', 'device', 'devil', 'diamond', 'diet', 'difference',
  'difficulty', 'dig', 'dimension', 'dinner', 'direction', 'director', 'dirt',
  'disaster', 'discipline', 'discount', 'discussion', 'disease', 'dish', 'disk',
  'display', 'distance', 'distribution', 'district', 'divide', 'doctor',
  'document', 'dog', 'door', 'dot', 'double', 'doubt', 'draft', 'drag', 'drama',
  'draw', 'drawer', 'drawing', 'dream', 'dress', 'drink', 'drive', 'driver',
  'drop', 'drunk', 'due', 'dump', 'dust', 'duty', 'ear', 'earth', 'ease',
  'east', 'eat', 'economics', 'economy', 'edge', 'editor', 'education',
  'effect', 'efficiency', 'effort', 'egg', 'election', 'elevator', 'emergency',
  'emotion', 'emphasis', 'employ', 'employee', 'employer', 'employment', 'end',
  'energy', 'engine', 'engineer', 'engineering', 'entertainment', 'enthusiasm',
  'entrance', 'entry', 'environment', 'equal', 'equipment', 'equivalent',
  'error', 'escape', 'essay', 'establishment', 'estate', 'estimate', 'evening',
  'event', 'evidence', 'exam', 'examination', 'example', 'exchange',
  'excitement', 'excuse', 'exercise', 'exit', 'experience', 'expert',
  'explanation', 'expression', 'extension', 'extent', 'external', 'extreme',
  'eye', 'face', 'fact', 'factor', 'fail', 'failure', 'fall', 'familiar',
  'family', 'fan', 'farm', 'farmer', 'fat', 'father', 'fault', 'fear',
  'feature', 'fee', 'feed', 'feedback', 'feel', 'feeling', 'female', 'few',
  'field', 'fight', 'figure', 'file', 'fill', 'film', 'final', 'finance',
  'finding', 'finger', 'finish', 'fire', 'fish', 'fishing', 'fix', 'flight',
  'floor', 'flow', 'flower', 'fly', 'focus', 'fold', 'following', 'food',
  'foot', 'football', 'force', 'forever', 'form', 'formal', 'fortune',
  'foundation', 'frame', 'freedom', 'friend', 'friendship', 'front', 'fruit',
  'fuel', 'fun', 'function', 'funeral', 'funny', 'future', 'gain', 'game',
  'gap', 'garage', 'garbage', 'garden', 'gas', 'gate', 'gather', 'gear', 'gene',
  'general', 'gift', 'girl', 'girlfriend', 'give', 'glad', 'glass', 'glove',
  'go', 'goal', 'god', 'gold', 'golf', 'good', 'government', 'grab', 'grade',
  'grand', 'grandfather', 'grandmother', 'grass', 'great', 'green', 'grocery',
  'ground', 'group', 'growth', 'guarantee', 'guard', 'guess', 'guest',
  'guidance', 'guide', 'guitar', 'guy', 'habit', 'hair', 'half', 'hall', 'hand',
  'handle', 'hang', 'harm', 'hat', 'hate', 'head', 'health', 'hearing', 'heart',
  'heat', 'heavy', 'height', 'hell', 'hello', 'help', 'hide', 'high',
  'highlight', 'highway', 'hire', 'historian', 'history', 'hit', 'hold', 'hole',
  'holiday', 'home', 'homework', 'honey', 'hook', 'hope', 'horror', 'horse',
  'hospital', 'host', 'hotel', 'hour', 'house', 'housing', 'human', 'hunt',
  'hurry', 'hurt', 'husband', 'ice', 'idea', 'ideal', 'if', 'illegal', 'image',
  'imagination', 'impact', 'implement', 'importance', 'impression',
  'improvement', 'incident', 'income', 'increase', 'independence',
  'independent', 'indication', 'individual', 'industry', 'inflation',
  'influence', 'information', 'initial', 'initiative', 'injury', 'insect',
  'inside', 'inspection', 'inspector', 'instance', 'instruction', 'insurance',
  'intention', 'interaction', 'interest', 'internal', 'international',
  'internet', 'interview', 'introduction', 'investment', 'invite', 'iron',
  'island', 'issue', 'it', 'item', 'jacket', 'job', 'join', 'joint', 'joke',
  'judge', 'judgment', 'juice', 'jump', 'junior', 'jury', 'keep', 'key', 'kick',
  'kid', 'kill', 'kind', 'king', 'kiss', 'kitchen', 'knee', 'knife',
  'knowledge', 'lab', 'lack', 'ladder', 'lady', 'lake', 'land', 'landscape',
  'language', 'laugh', 'law', 'lawyer', 'lay', 'layer', 'lead', 'leader',
  'leadership', 'leading', 'league', 'leather', 'leave', 'lecture', 'leg',
  'length', 'lesson', 'let', 'letter', 'level', 'library', 'lie', 'life',
  'lift', 'light', 'limit', 'line', 'link', 'lip', 'list', 'listen',
  'literature', 'living', 'load', 'loan', 'local', 'location', 'lock', 'log',
  'long', 'look', 'loss', 'love', 'low', 'luck', 'lunch', 'machine', 'magazine',
  'mail', 'main', 'maintenance', 'major', 'make', 'male', 'mall', 'man',
  'management', 'manager', 'manner', 'manufacturer', 'many', 'map', 'march',
  'mark', 'market', 'marketing', 'marriage', 'master', 'match', 'mate',
  'material', 'math', 'matter', 'maximum', 'maybe', 'meal', 'meaning',
  'measurement', 'meat', 'media', 'medicine', 'medium', 'meeting', 'member',
  'membership', 'memory', 'mention', 'menu', 'mess', 'message', 'metal',
  'method', 'middle', 'midnight', 'might', 'milk', 'mind', 'mine', 'minimum',
  'minor', 'minute', 'mirror', 'miss', 'mission', 'mistake', 'mix', 'mixture',
  'mobile', 'mode', 'model', 'mom', 'moment', 'money', 'monitor', 'month',
  'mood', 'morning', 'mortgage', 'most', 'mother', 'motor', 'mountain', 'mouse',
  'mouth', 'move', 'movie', 'mud', 'muscle', 'music', 'nail', 'name', 'nasty',
  'nation', 'national', 'native', 'natural', 'nature', 'neck', 'negative',
  'negotiation', 'nerve', 'net', 'network', 'news', 'newspaper', 'night',
  'nobody', 'noise', 'normal', 'north', 'nose', 'note', 'nothing', 'notice',
  'novel', 'number', 'nurse', 'object', 'objective', 'obligation', 'occasion',
  'offer', 'office', 'officer', 'official', 'oil', 'opening', 'operation',
  'opinion', 'opportunity', 'opposite', 'option', 'orange', 'order', 'ordinary',
  'organization', 'original', 'other', 'outcome', 'outside', 'oven', 'owner',
  'pace', 'pack', 'package', 'page', 'pain', 'paint', 'painting', 'pair',
  'panic', 'paper', 'parent', 'park', 'parking', 'part', 'particular',
  'partner', 'party', 'pass', 'passage', 'passenger', 'passion', 'past', 'path',
  'patience', 'patient', 'pattern', 'pause', 'pay', 'payment', 'peace', 'peak',
  'pen', 'penalty', 'pension', 'people', 'percentage', 'perception',
  'performance', 'period', 'permission', 'permit', 'person', 'personality',
  'perspective', 'phase', 'philosophy', 'phone', 'photo', 'phrase', 'physical',
  'physics', 'piano', 'pick', 'picture', 'pie', 'piece', 'pin', 'pipe', 'pitch',
  'pizza', 'place', 'plan', 'plane', 'plant', 'plastic', 'plate', 'platform',
  'play', 'player', 'pleasure', 'plenty', 'poem', 'poet', 'poetry', 'point',
  'police', 'policy', 'politics', 'pollution', 'pool', 'pop', 'population',
  'position', 'positive', 'possession', 'possibility', 'post', 'pot', 'potato',
  'potential', 'pound', 'power', 'practice', 'preference', 'preparation',
  'presence', 'present', 'presentation', 'president', 'press', 'pressure',
  'price', 'pride', 'priest', 'primary', 'principle', 'print', 'prior',
  'priority', 'private', 'prize', 'problem', 'procedure', 'process', 'produce',
  'product', 'profession', 'professional', 'professor', 'profile', 'profit',
  'program', 'progress', 'project', 'promise', 'promotion', 'prompt', 'proof',
  'property', 'proposal', 'protection', 'psychology', 'public', 'pull', 'punch',
  'purchase', 'purple', 'purpose', 'push', 'quality', 'quantity', 'quarter',
  'queen', 'question', 'quiet', 'quote', 'race', 'radio', 'rain', 'raise',
  'range', 'rate', 'ratio', 'raw', 'reach', 'reaction', 'read', 'reading',
  'reality', 'reason', 'reception', 'recipe', 'recognition', 'recommendation',
  'record', 'recording', 'recover', 'red', 'reference', 'reflection',
  'refrigerator', 'refuse', 'region', 'register', 'regret', 'regular',
  'relation', 'relationship', 'relative', 'release', 'relief', 'remote',
  'remove', 'rent', 'repair', 'repeat', 'replacement', 'reply', 'report',
  'representative', 'republic', 'reputation', 'request', 'requirement',
  'research', 'reserve', 'resident', 'resolution', 'resolve', 'resort',
  'resource', 'respect', 'response', 'responsibility', 'rest', 'restaurant',
  'result', 'return', 'reveal', 'revenue', 'review', 'revolution', 'reward',
  'rice', 'rich', 'ride', 'ring', 'rip', 'rise', 'risk', 'river', 'road',
  'rock', 'role', 'roll', 'roof', 'room', 'rope', 'round', 'routine', 'row',
  'royal', 'rub', 'ruin', 'rule', 'run', 'rush', 'safe', 'safety', 'sail',
  'salad', 'salary', 'sale', 'salt', 'sample', 'sand', 'sandwich',
  'satisfaction', 'save', 'savings', 'scale', 'scene', 'schedule', 'scheme',
  'school', 'science', 'score', 'scratch', 'screen', 'screw', 'script', 'sea',
  'search', 'season', 'seat', 'second', 'secret', 'secretary', 'section',
  'sector', 'security', 'selection', 'self', 'senior', 'sense', 'sensitive',
  'sentence', 'series', 'serve', 'service', 'session', 'set', 'setting', 'sex',
  'shake', 'shame', 'shape', 'share', 'she', 'shelter', 'shift', 'shine',
 'ship', 'shirt', 'shock', 'shoe', 'shoot', 'shop', 'shopping', 'shot',
  'shoulder', 'show', 'shower', 'side', 'sign', 'signal', 'signature',
  'significance', 'silly', 'silver', 'simple', 'sing', 'singer', 'single',
  'sink', 'sir', 'sister', 'site', 'situation', 'size', 'skill', 'skin',
  'skirt', 'sky', 'sleep', 'slice', 'slide', 'slip', 'smell', 'smile', 'smoke',
  'snow', 'society', 'sock', 'soft', 'software', 'soil', 'solid', 'solution',
  'somewhere', 'son', 'song', 'sort', 'sound', 'soup', 'source', 'south',
  'space', 'spare', 'speaker', 'special', 'specialist', 'specific', 'speech',
  'speed', 'spell', 'spend', 'spirit', 'spiritual', 'spite', 'split', 'sport',
  'spot', 'spray', 'spread', 'spring', 'square', 'stable', 'staff', 'stage',
  'stand', 'standard', 'star', 'start', 'state', 'statement', 'station',
  'status', 'stay', 'steak', 'steal', 'step', 'stick', 'still', 'stock',
  'stomach', 'stop', 'storage', 'store', 'storm', 'story', 'strain', 'stranger',
  'strategy', 'street', 'strength', 'stress', 'stretch', 'strike', 'string',
  'strip', 'stroke', 'structure', 'struggle', 'student', 'studio', 'study',
  'stuff', 'stupid', 'style', 'subject', 'substance', 'success', 'sugar',
  'suggestion', 'suit', 'summer', 'sun', 'supermarket', 'support', 'surgery',
  'surprise', 'surround', 'survey', 'suspect', 'sweet', 'swim', 'swimming',
  'swing', 'switch', 'sympathy', 'system', 'table', 'tackle', 'tale', 'talk',
  'tank', 'tap', 'target', 'task', 'taste', 'tax', 'tea', 'teach', 'teacher',
  'teaching', 'team', 'tear', 'technology', 'telephone', 'television', 'tell',
  'temperature', 'tennis', 'tension', 'term', 'test', 'text', 'thanks', 'theme',
  'theory', 'thing', 'thought', 'throat', 'ticket', 'tie', 'till', 'time',
  'tip', 'title', 'today', 'toe', 'tomorrow', 'tone', 'tongue', 'tonight',
  'tool', 'tooth', 'top', 'topic', 'total', 'touch', 'tour', 'tourist',
  'towel', 'tower', 'town', 'track', 'trade', 'tradition', 'traffic', 'train',
  'trainer', 'training', 'transition', 'transportation', 'trash', 'travel',
  'treat', 'tree', 'trick', 'trip', 'trouble', 'truck', 'trust', 'truth', 'try',
  'tune', 'turn', 'twist', 'type', 'uncle', 'understanding', 'union', 'unique',
  'unit', 'university', 'upper', 'upstairs', 'use', 'user', 'usual', 'vacation',
  'valuable', 'value', 'variation', 'variety', 'vast', 'vegetable', 'vehicle',
  'version', 'video', 'view', 'village', 'virus', 'visit', 'visual', 'voice',
  'volume', 'wait', 'wake', 'walk', 'wall', 'war', 'warning', 'wash', 'watch',
  'water', 'wave', 'way', 'weakness', 'wealth', 'wear', 'weather', 'web',
  'wedding', 'week', 'weekend', 'weight', 'weird', 'welcome', 'west', 'western',
  'wheel', 'whereas', 'white', 'whole', 'wife', 'will', 'win', 'wind', 'window',
  'wine', 'wing', 'winner', 'winter', 'wish', 'witness', 'woman', 'wonder',
  'wood', 'word', 'work', 'worker', 'working', 'world', 'worry', 'worth',
  'wrap', 'writer', 'writing', 'yard', 'year', 'yellow', 'yesterday', 'you',
  'young', 'youth', 'zone'
]


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
