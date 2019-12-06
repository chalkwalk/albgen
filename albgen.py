#!/usr/bin/python3
"""A tool to generate a human readable brief for making an album. """

from random import gauss
from random import random

import argparse

parser = argparse.ArgumentParser(description='Generate an album listing.')

parser.add_argument('--track_count', type=int, default=12, help='How many tracks the album will have.')
parser.add_argument('--max_bpm', type=int, default=150, help='The fastest BPM to suggest.')
parser.add_argument('--min_bpm', type=int, default=70, help='The slowest BPM to suggest.')
parser.add_argument('--excluded_modes', action='append', default=[], type=str, help='A list of key modes to exclude.')
parser.add_argument('--max_length', type=int, default=150, help='The longest track to suggest in seconds.')
parser.add_argument('--min_length', type=int, default=70, help='The shortest track to suggest in seconds.')
parser.add_argument('--output_format', type=str, choices=['human', 'yaml', 'csv'], default='human', help='The format to output the album listing')
args = parser.parse_args()


adjectives = [
  'Adorable', 'Adventurous', 'Aggressive', 'Agreeable', 'Alert', 'Alive',
  'Amused', 'Angry', 'Annoyed', 'Annoying', 'Anxious', 'Arrogant', 'Ashamed',
  'Attractive', 'Average', 'Awful', 'Bad', 'Beautiful', 'Better', 'Bewildered',
  'Black', 'Bloody', 'Blue', 'Blue-eyed', 'Blushing', 'Bored', 'Brainy',
  'Brave', 'Breakable', 'Bright', 'Brilliant', 'Busy', 'Calm', 'Careful',
  'Cautious', 'Charming', 'Cheerful', 'Clean', 'Clear', 'Clever', 'Cloudy',
  'Clumsy', 'Colorful', 'Combative', 'Comfortable', 'Concerned', 'Condemned',
  'Confused', 'Cooperative', 'Courageous', 'Crazy', 'Creepy', 'Crowded',
  'Cruel', 'Curious', 'Cute', 'Dangerous', 'Dark', 'Dead', 'Defeated',
  'Defiant', 'Delightful', 'Depressed', 'Determined', 'Different', 'Difficult',
  'Disgusted', 'Distinct', 'Disturbed', 'Dizzy', 'Doubtful', 'Drab', 'Dull',
  'Eager', 'Easy', 'Elated', 'Elegant', 'Embarrassed', 'Enchanting',
  'Encouraging', 'Energetic', 'Enthusiastic', 'Envious', 'Evil', 'Excited',
  'Expensive', 'Exuberant', 'Fair', 'Faithful', 'Famous', 'Fancy', 'Fantastic',
  'Fierce', 'Filthy', 'Fine', 'Foolish', 'Fragile', 'Frail', 'Frantic',
  'Friendly', 'Frightened', 'Funny', 'Gentle', 'Gifted', 'Glamorous',
  'Gleaming', 'Glorious', 'Good', 'Gorgeous', 'Graceful', 'Grieving',
  'Grotesque', 'Grumpy', 'Handsome', 'Happy', 'Healthy', 'Helpful', 'Helpless',
  'Hilarious', 'Homeless', 'Homely', 'Horrible', 'Hungry', 'Hurt', 'Ill',
  'Important', 'Impossible', 'Inexpensive', 'Innocent', 'Inquisitive', 'Itchy',
  'Jealous', 'Jittery', 'Jolly', 'Joyous', 'Kind', 'Lazy', 'Light', 'Lively',
  'Lonely', 'Long', 'Lovely', 'Lucky', 'Magnificent', 'Misty', 'Modern',
  'Motionless', 'Muddy', 'Mushy', 'Mysterious', 'Nasty', 'Naughty', 'Nervous',
  'Nice', 'Nonchalant', 'Nutty', 'Obedient', 'Obnoxious', 'Odd',
  'Old-fashioned', 'Open', 'Outrageous', 'Outstanding', 'Panicky', 'Perfect',
  'Plain', 'Pleasant', 'Poised', 'Poor', 'Powerful', 'Precious', 'Prickly',
  'Proud', 'Putrid', 'Puzzled', 'Quaint', 'Real', 'Relieved', 'Repulsive',
  'Rich', 'Sad', 'Scary', 'Selfish', 'Shiny', 'Shy', 'Silly', 'Sleepy',
  'Smiling', 'Smoggy', 'Sore', 'Sparkling', 'Splendid', 'Spotless', 'Stormy',
  'Strange', 'Stupid', 'Successful', 'Super', 'Talented', 'Tame', 'Tasty',
  'Tender', 'Tense', 'Terrible', 'Thankful', 'Thoughtful', 'Thoughtless',
  'Tired', 'Tough', 'Troubled', 'Ugliest', 'Ugly', 'Uninterested', 'Unsightly',
  'Unusual', 'Upset', 'Uptight', 'Victorious', 'Vivacious', 'Wandering',
  'Weary', 'Wicked', 'Wide-eyed', 'Wild', 'Witty', 'Worried', 'Worrisome',
  'Wrong', 'Zany', 'Zealous'
]

nouns = [
  'Ability', 'Abroad', 'Abuse', 'Access', 'Accident', 'Account', 'Act',
  'Action', 'Activity', 'Actor', 'Ad', 'Addition', 'Address', 'Administration',
  'Adult', 'Advance', 'Advantage', 'Advertising', 'Advice', 'Affair', 'Affect',
  'Afternoon', 'Age', 'Agency', 'Agent', 'Agreement', 'Air', 'Airline',
  'Airport', 'Alarm', 'Alcohol', 'Alternative', 'Ambition', 'Amount',
  'Analysis', 'Analyst', 'Anger', 'Angle', 'Animal', 'Annual', 'Answer',
  'Anxiety', 'Anybody', 'Anything', 'Anywhere', 'Apartment', 'Appeal',
  'Appearance', 'Apple', 'Application', 'Appointment', 'Area', 'Argument',
  'Arm', 'Army', 'Arrival', 'Art', 'Article', 'Aside', 'Ask', 'Aspect',
  'Assignment', 'Assist', 'Assistance', 'Assistant', 'Associate', 'Association',
  'Assumption', 'Atmosphere', 'Attack', 'Attempt', 'Attention', 'Attitude',
  'Audience', 'Author', 'Average', 'Award', 'Awareness', 'Baby', 'Back',
  'Background', 'Bad', 'Bag', 'Bake', 'Balance', 'Ball', 'Band', 'Bank', 'Bar',
  'Base', 'Baseball', 'Basis', 'Basket', 'Bat', 'Bath', 'Bathroom', 'Battle',
  'Beach', 'Bear', 'Beat', 'Beautiful', 'Bed', 'Bedroom', 'Beer', 'Beginning',
  'Being', 'Bell', 'Belt', 'Bench', 'Bend', 'Benefit', 'Bet', 'Beyond',
  'Bicycle', 'Bid', 'Big', 'Bike', 'Bill', 'Bird', 'Birth', 'Birthday', 'Bit',
  'Bite', 'Bitter', 'Black', 'Blame', 'Blank', 'Blind', 'Block', 'Blood',
  'Blow', 'Blue', 'Board', 'Boat', 'Body', 'Bone', 'Bonus', 'Book', 'Boot',
  'Border', 'Boss', 'Bother', 'Bottle', 'Bottom', 'Bowl', 'Box', 'Boy',
  'Boyfriend', 'Brain', 'Branch', 'Brave', 'Bread', 'Break', 'Breakfast',
  'Breast', 'Breath', 'Brick', 'Bridge', 'Brief', 'Broad', 'Brother', 'Brown',
  'Brush', 'Buddy', 'Budget', 'Bug', 'Building', 'Bunch', 'Burn', 'Bus',
  'Business', 'Button', 'Buy', 'Buyer', 'Cabinet', 'Cable', 'Cake', 'Calendar',
  'Call', 'Calm', 'Camera', 'Camp', 'Campaign', 'Can', 'Cancel', 'Cancer',
  'Candidate', 'Candle', 'Candy', 'Cap', 'Capital', 'Car', 'Card', 'Care',
  'Career', 'Carpet', 'Carry', 'Case', 'Cash', 'Cat', 'Catch', 'Category',
  'Cause', 'Celebration', 'Cell', 'Chain', 'Chair', 'Challenge', 'Champion',
  'Championship', 'Chance', 'Change', 'Channel', 'Chapter', 'Character',
  'Charge', 'Charity', 'Chart', 'Check', 'Cheek', 'Chemical', 'Chemistry',
  'Chest', 'Chicken', 'Child', 'Childhood', 'Chip', 'Chocolate', 'Choice',
  'Church', 'Cigarette', 'City', 'Claim', 'Class', 'Classic', 'Classroom',
  'Clerk', 'Click', 'Client', 'Climate', 'Clock', 'Closet', 'Clothes', 'Cloud',
  'Club', 'Clue', 'Coach', 'Coast', 'Coat', 'Code', 'Coffee', 'Cold', 'Collar',
  'Collection', 'College', 'Combination', 'Combine', 'Comfort', 'Command',
  'Comment', 'Commercial', 'Commission', 'Committee', 'Common', 'Communication',
  'Community', 'Company', 'Comparison', 'Competition', 'Complaint', 'Complex',
  'Computer', 'Concentrate', 'Concept', 'Concern', 'Concert', 'Conclusion',
  'Condition', 'Conference', 'Confidence', 'Conflict', 'Confusion',
  'Connection', 'Consequence', 'Consideration', 'Consist', 'Constant',
  'Construction', 'Contact', 'Contest', 'Context', 'Contract', 'Contribution',
  'Control', 'Conversation', 'Convert', 'Cook', 'Cookie', 'Copy', 'Corner',
  'Cost', 'Count', 'Counter', 'Country', 'County', 'Couple', 'Courage',
  'Course', 'Court', 'Cousin', 'Cover', 'Cow', 'Crack', 'Craft', 'Crash',
  'Crazy', 'Cream', 'Creative', 'Credit', 'Crew', 'Criticism', 'Cross', 'Cry',
  'Culture', 'Cup', 'Currency', 'Current', 'Curve', 'Customer', 'Cut', 'Cycle',
  'Damage', 'Dance', 'Dare', 'Dark', 'Data', 'Database', 'Date', 'Daughter',
  'Day', 'Dead', 'Deal', 'Dealer', 'Dear', 'Death', 'Debate', 'Debt',
  'Decision', 'Deep', 'Definition', 'Degree', 'Delay', 'Delivery', 'Demand',
  'Department', 'Departure', 'Dependent', 'Deposit', 'Depression', 'Depth',
  'Description', 'Design', 'Designer', 'Desire', 'Desk', 'Detail',
  'Development', 'Device', 'Devil', 'Diamond', 'Diet', 'Difference',
  'Difficulty', 'Dig', 'Dimension', 'Dinner', 'Direction', 'Director', 'Dirt',
  'Disaster', 'Discipline', 'Discount', 'Discussion', 'Disease', 'Dish', 'Disk',
  'Display', 'Distance', 'Distribution', 'District', 'Divide', 'Doctor',
  'Document', 'Dog', 'Door', 'Dot', 'Double', 'Doubt', 'Draft', 'Drag', 'Drama',
  'Draw', 'Drawer', 'Drawing', 'Dream', 'Dress', 'Drink', 'Drive', 'Driver',
  'Drop', 'Drunk', 'Due', 'Dump', 'Dust', 'Duty', 'Ear', 'Earth', 'Ease',
  'East', 'Eat', 'Economics', 'Economy', 'Edge', 'Editor', 'Education',
  'Effect', 'Efficiency', 'Effort', 'Egg', 'Election', 'Elevator', 'Emergency',
  'Emotion', 'Emphasis', 'Employ', 'Employee', 'Employer', 'Employment', 'End',
  'Energy', 'Engine', 'Engineer', 'Engineering', 'Entertainment', 'Enthusiasm',
  'Entrance', 'Entry', 'Environment', 'Equal', 'Equipment', 'Equivalent',
  'Error', 'Escape', 'Essay', 'Establishment', 'Estate', 'Estimate', 'Evening',
  'Event', 'Evidence', 'Exam', 'Examination', 'Example', 'Exchange',
  'Excitement', 'Excuse', 'Exercise', 'Exit', 'Experience', 'Expert',
  'Explanation', 'Expression', 'Extension', 'Extent', 'External', 'Extreme',
  'Eye', 'Face', 'Fact', 'Factor', 'Fail', 'Failure', 'Fall', 'Familiar',
  'Family', 'Fan', 'Farm', 'Farmer', 'Fat', 'Father', 'Fault', 'Fear',
  'Feature', 'Fee', 'Feed', 'Feedback', 'Feel', 'Feeling', 'Female', 'Few',
  'Field', 'Fight', 'Figure', 'File', 'Fill', 'Film', 'Final', 'Finance',
  'Finding', 'Finger', 'Finish', 'Fire', 'Fish', 'Fishing', 'Fix', 'Flight',
  'Floor', 'Flow', 'Flower', 'Fly', 'Focus', 'Fold', 'Following', 'Food',
  'Foot', 'Football', 'Force', 'Forever', 'Form', 'Formal', 'Fortune',
  'Foundation', 'Frame', 'Freedom', 'Friend', 'Friendship', 'Front', 'Fruit',
  'Fuel', 'Fun', 'Function', 'Funeral', 'Funny', 'Future', 'Gain', 'Game',
  'Gap', 'Garage', 'Garbage', 'Garden', 'Gas', 'Gate', 'Gather', 'Gear', 'Gene',
  'General', 'Gift', 'Girl', 'Girlfriend', 'Give', 'Glad', 'Glass', 'Glove',
  'Go', 'Goal', 'God', 'Gold', 'Golf', 'Good', 'Government', 'Grab', 'Grade',
  'Grand', 'Grandfather', 'Grandmother', 'Grass', 'Great', 'Green', 'Grocery',
  'Ground', 'Group', 'Growth', 'Guarantee', 'Guard', 'Guess', 'Guest',
  'Guidance', 'Guide', 'Guitar', 'Guy', 'Habit', 'Hair', 'Half', 'Hall', 'Hand',
  'Handle', 'Hang', 'Harm', 'Hat', 'Hate', 'Head', 'Health', 'Hearing', 'Heart',
  'Heat', 'Heavy', 'Height', 'Hell', 'Hello', 'Help', 'Hide', 'High',
  'Highlight', 'Highway', 'Hire', 'Historian', 'History', 'Hit', 'Hold', 'Hole',
  'Holiday', 'Home', 'Homework', 'Honey', 'Hook', 'Hope', 'Horror', 'Horse',
  'Hospital', 'Host', 'Hotel', 'Hour', 'House', 'Housing', 'Human', 'Hunt',
  'Hurry', 'Hurt', 'Husband', 'Ice', 'Idea', 'Ideal', 'If', 'Illegal', 'Image',
  'Imagination', 'Impact', 'Implement', 'Importance', 'Impression',
  'Improvement', 'Incident', 'Income', 'Increase', 'Independence',
  'Independent', 'Indication', 'Individual', 'Industry', 'Inflation',
  'Influence', 'Information', 'Initial', 'Initiative', 'Injury', 'Insect',
  'Inside', 'Inspection', 'Inspector', 'Instance', 'Instruction', 'Insurance',
  'Intention', 'Interaction', 'Interest', 'Internal', 'International',
  'Internet', 'Interview', 'Introduction', 'Investment', 'Invite', 'Iron',
  'Island', 'Issue', 'It', 'Item', 'Jacket', 'Job', 'Join', 'Joint', 'Joke',
  'Judge', 'Judgment', 'Juice', 'Jump', 'Junior', 'Jury', 'Keep', 'Key', 'Kick',
  'Kid', 'Kill', 'Kind', 'King', 'Kiss', 'Kitchen', 'Knee', 'Knife',
  'Knowledge', 'Lab', 'Lack', 'Ladder', 'Lady', 'Lake', 'Land', 'Landscape',
  'Language', 'Laugh', 'Law', 'Lawyer', 'Lay', 'Layer', 'Lead', 'Leader',
  'Leadership', 'Leading', 'League', 'Leather', 'Leave', 'Lecture', 'Leg',
  'Length', 'Lesson', 'Let', 'Letter', 'Level', 'Library', 'Lie', 'Life',
  'Lift', 'Light', 'Limit', 'Line', 'Link', 'Lip', 'List', 'Listen',
  'Literature', 'Living', 'Load', 'Loan', 'Local', 'Location', 'Lock', 'Log',
  'Long', 'Look', 'Loss', 'Love', 'Low', 'Luck', 'Lunch', 'Machine', 'Magazine',
  'Mail', 'Main', 'Maintenance', 'Major', 'Make', 'Male', 'Mall', 'Man',
  'Management', 'Manager', 'Manner', 'Manufacturer', 'Many', 'Map', 'March',
  'Mark', 'Market', 'Marketing', 'Marriage', 'Master', 'Match', 'Mate',
  'Material', 'Math', 'Matter', 'Maximum', 'Maybe', 'Meal', 'Meaning',
  'Measurement', 'Meat', 'Media', 'Medicine', 'Medium', 'Meeting', 'Member',
  'Membership', 'Memory', 'Mention', 'Menu', 'Mess', 'Message', 'Metal',
  'Method', 'Middle', 'Midnight', 'Might', 'Milk', 'Mind', 'Mine', 'Minimum',
  'Minor', 'Minute', 'Mirror', 'Miss', 'Mission', 'Mistake', 'Mix', 'Mixture',
  'Mobile', 'Mode', 'Model', 'Mom', 'Moment', 'Money', 'Monitor', 'Month',
  'Mood', 'Morning', 'Mortgage', 'Most', 'Mother', 'Motor', 'Mountain', 'Mouse',
  'Mouth', 'Move', 'Movie', 'Mud', 'Muscle', 'Music', 'Nail', 'Name', 'Nasty',
  'Nation', 'National', 'Native', 'Natural', 'Nature', 'Neck', 'Negative',
  'Negotiation', 'Nerve', 'Net', 'Network', 'News', 'Newspaper', 'Night',
  'Nobody', 'Noise', 'Normal', 'North', 'Nose', 'Note', 'Nothing', 'Notice',
  'Novel', 'Number', 'Nurse', 'Object', 'Objective', 'Obligation', 'Occasion',
  'Offer', 'Office', 'Officer', 'Official', 'Oil', 'Opening', 'Operation',
  'Opinion', 'Opportunity', 'Opposite', 'Option', 'Orange', 'Order', 'Ordinary',
  'Organization', 'Original', 'Other', 'Outcome', 'Outside', 'Oven', 'Owner',
  'Pace', 'Pack', 'Package', 'Page', 'Pain', 'Paint', 'Painting', 'Pair',
  'Panic', 'Paper', 'Parent', 'Park', 'Parking', 'Part', 'Particular',
  'Partner', 'Party', 'Pass', 'Passage', 'Passenger', 'Passion', 'Past', 'Path',
  'Patience', 'Patient', 'Pattern', 'Pause', 'Pay', 'Payment', 'Peace', 'Peak',
  'Pen', 'Penalty', 'Pension', 'People', 'Percentage', 'Perception',
  'Performance', 'Period', 'Permission', 'Permit', 'Person', 'Personality',
  'Perspective', 'Phase', 'Philosophy', 'Phone', 'Photo', 'Phrase', 'Physical',
  'Physics', 'Piano', 'Pick', 'Picture', 'Pie', 'Piece', 'Pin', 'Pipe', 'Pitch',
  'Pizza', 'Place', 'Plan', 'Plane', 'Plant', 'Plastic', 'Plate', 'Platform',
  'Play', 'Player', 'Pleasure', 'Plenty', 'Poem', 'Poet', 'Poetry', 'Point',
  'Police', 'Policy', 'Politics', 'Pollution', 'Pool', 'Pop', 'Population',
  'Position', 'Positive', 'Possession', 'Possibility', 'Post', 'Pot', 'Potato',
  'Potential', 'Pound', 'Power', 'Practice', 'Preference', 'Preparation',
  'Presence', 'Present', 'Presentation', 'President', 'Press', 'Pressure',
  'Price', 'Pride', 'Priest', 'Primary', 'Principle', 'Print', 'Prior',
  'Priority', 'Private', 'Prize', 'Problem', 'Procedure', 'Process', 'Produce',
  'Product', 'Profession', 'Professional', 'Professor', 'Profile', 'Profit',
  'Program', 'Progress', 'Project', 'Promise', 'Promotion', 'Prompt', 'Proof',
  'Property', 'Proposal', 'Protection', 'Psychology', 'Public', 'Pull', 'Punch',
  'Purchase', 'Purple', 'Purpose', 'Push', 'Quality', 'Quantity', 'Quarter',
  'Queen', 'Question', 'Quiet', 'Quote', 'Race', 'Radio', 'Rain', 'Raise',
  'Range', 'Rate', 'Ratio', 'Raw', 'Reach', 'Reaction', 'Read', 'Reading',
  'Reality', 'Reason', 'Reception', 'Recipe', 'Recognition', 'Recommendation',
  'Record', 'Recording', 'Recover', 'Red', 'Reference', 'Reflection',
  'Refrigerator', 'Refuse', 'Region', 'Register', 'Regret', 'Regular',
  'Relation', 'Relationship', 'Relative', 'Release', 'Relief', 'Remote',
  'Remove', 'Rent', 'Repair', 'Repeat', 'Replacement', 'Reply', 'Report',
  'Representative', 'Republic', 'Reputation', 'Request', 'Requirement',
  'Research', 'Reserve', 'Resident', 'Resolution', 'Resolve', 'Resort',
  'Resource', 'Respect', 'Response', 'Responsibility', 'Rest', 'Restaurant',
  'Result', 'Return', 'Reveal', 'Revenue', 'Review', 'Revolution', 'Reward',
  'Rice', 'Rich', 'Ride', 'Ring', 'Rip', 'Rise', 'Risk', 'River', 'Road',
  'Rock', 'Role', 'Roll', 'Roof', 'Room', 'Rope', 'Round', 'Routine', 'Row',
  'Royal', 'Rub', 'Ruin', 'Rule', 'Run', 'Rush', 'Safe', 'Safety', 'Sail',
  'Salad', 'Salary', 'Sale', 'Salt', 'Sample', 'Sand', 'Sandwich',
  'Satisfaction', 'Save', 'Savings', 'Scale', 'Scene', 'Schedule', 'Scheme',
  'School', 'Science', 'Score', 'Scratch', 'Screen', 'Screw', 'Script', 'Sea',
  'Search', 'Season', 'Seat', 'Second', 'Secret', 'Secretary', 'Section',
  'Sector', 'Security', 'Selection', 'Self', 'Senior', 'Sense', 'Sensitive',
  'Sentence', 'Series', 'Serve', 'Service', 'Session', 'Set', 'Setting', 'Sex',
  'Shake', 'Shame', 'Shape', 'Share', 'She', 'Shelter', 'Shift', 'Shine',
 'Ship', 'Shirt', 'Shock', 'Shoe', 'Shoot', 'Shop', 'Shopping', 'Shot',
  'Shoulder', 'Show', 'Shower', 'Side', 'Sign', 'Signal', 'Signature',
  'Significance', 'Silly', 'Silver', 'Simple', 'Sing', 'Singer', 'Single',
  'Sink', 'Sir', 'Sister', 'Site', 'Situation', 'Size', 'Skill', 'Skin',
  'Skirt', 'Sky', 'Sleep', 'Slice', 'Slide', 'Slip', 'Smell', 'Smile', 'Smoke',
  'Snow', 'Society', 'Sock', 'Soft', 'Software', 'Soil', 'Solid', 'Solution',
  'Somewhere', 'Son', 'Song', 'Sort', 'Sound', 'Soup', 'Source', 'South',
  'Space', 'Spare', 'Speaker', 'Special', 'Specialist', 'Specific', 'Speech',
  'Speed', 'Spell', 'Spend', 'Spirit', 'Spiritual', 'Spite', 'Split', 'Sport',
  'Spot', 'Spray', 'Spread', 'Spring', 'Square', 'Stable', 'Staff', 'Stage',
  'Stand', 'Standard', 'Star', 'Start', 'State', 'Statement', 'Station',
  'Status', 'Stay', 'Steak', 'Steal', 'Step', 'Stick', 'Still', 'Stock',
  'Stomach', 'Stop', 'Storage', 'Store', 'Storm', 'Story', 'Strain', 'Stranger',
  'Strategy', 'Street', 'Strength', 'Stress', 'Stretch', 'Strike', 'String',
  'Strip', 'Stroke', 'Structure', 'Struggle', 'Student', 'Studio', 'Study',
  'Stuff', 'Stupid', 'Style', 'Subject', 'Substance', 'Success', 'Sugar',
  'Suggestion', 'Suit', 'Summer', 'Sun', 'Supermarket', 'Support', 'Surgery',
  'Surprise', 'Surround', 'Survey', 'Suspect', 'Sweet', 'Swim', 'Swimming',
  'Swing', 'Switch', 'Sympathy', 'System', 'Table', 'Tackle', 'Tale', 'Talk',
  'Tank', 'Tap', 'Target', 'Task', 'Taste', 'Tax', 'Tea', 'Teach', 'Teacher',
  'Teaching', 'Team', 'Tear', 'Technology', 'Telephone', 'Television', 'Tell',
  'Temperature', 'Tennis', 'Tension', 'Term', 'Test', 'Text', 'Thanks', 'Theme',
  'Theory', 'Thing', 'Thought', 'Throat', 'Ticket', 'Tie', 'Till', 'Time',
  'Tip', 'Title', 'Today', 'Toe', 'Tomorrow', 'Tone', 'Tongue', 'Tonight',
  'Tool', 'Tooth', 'Top', 'Topic', 'Total', 'Touch', 'Tour', 'Tourist',
  'Towel', 'Tower', 'Town', 'Track', 'Trade', 'Tradition', 'Traffic', 'Train',
  'Trainer', 'Training', 'Transition', 'Transportation', 'Trash', 'Travel',
  'Treat', 'Tree', 'Trick', 'Trip', 'Trouble', 'Truck', 'Trust', 'Truth', 'Try',
  'Tune', 'Turn', 'Twist', 'Type', 'Uncle', 'Understanding', 'Union', 'Unique',
  'Unit', 'University', 'Upper', 'Upstairs', 'Use', 'User', 'Usual', 'Vacation',
  'Valuable', 'Value', 'Variation', 'Variety', 'Vast', 'Vegetable', 'Vehicle',
  'Version', 'Video', 'View', 'Village', 'Virus', 'Visit', 'Visual', 'Voice',
  'Volume', 'Wait', 'Wake', 'Walk', 'Wall', 'War', 'Warning', 'Wash', 'Watch',
  'Water', 'Wave', 'Way', 'Weakness', 'Wealth', 'Wear', 'Weather', 'Web',
  'Wedding', 'Week', 'Weekend', 'Weight', 'Weird', 'Welcome', 'West', 'Western',
  'Wheel', 'Whereas', 'White', 'Whole', 'Wife', 'Will', 'Win', 'Wind', 'Window',
  'Wine', 'Wing', 'Winner', 'Winter', 'Wish', 'Witness', 'Woman', 'Wonder',
  'Wood', 'Word', 'Work', 'Worker', 'Working', 'World', 'Worry', 'Worth',
  'Wrap', 'Writer', 'Writing', 'Yard', 'Year', 'Yellow', 'Yesterday', 'You',
  'Young', 'Youth', 'Zone'
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
  return ListNumberToString([x for x in [
      'Lydian', 'Ionian', 'Mixolydian', 'Dorian', 'Aeolean', 'Phrygian',
      'Locrian'
  ] if x not in args.excluded_modes], number)


def NumberToColour(number):
  return ListNumberToString([
      'Brilliant', 'Bright', 'Neutral', 'Dull', 'Dark'
  ], number)


def NumberToMood(number):
  return ListNumberToString([
      'Ecstatic', 'Happy', 'Calm', 'Mellow', 'Melancholy', 'Sad', 'Devastated'
  ], number)


def NumberToTimeSignature(number):
  return ListNumberToString(['2/4', '3/4', '4/4', '7/8', '5/4'], number)


def NumberToTexture(number):
  return ListNumberToString(['Gritty', 'Rough', 'Natural', 'Smooth'], number)


def SecondsToMinutes(seconds):
  return '%d:%02d' % (seconds/60, seconds % 60)


def NumberToLength(number):
  length_range = args.max_length - args.min_length
  length_in_seconds = round(args.min_length + length_range * number)
  return length_in_seconds


def NumberToArticle(number):
  return ListNumberToString([
      'My', 'Your', 'His', 'Her', 'Our', 'Their', 'The', 'The', 'The', 'A', 'A',
      'A', None, None, None, None
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
    adjective = NumberToAdjective(track['adjective'])
    noun = NumberToNoun(track['noun'])
    if article:
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
  rows.append(['Track', 'Title', 'Tempo/BPM', 'Time Signature', 'Length/s', 'Key', 'Mode', 'Colour', 'Mood', 'Texture'])
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
    output += 'A %s, %s, %s track in %s,\n' % (NumberToTexture(track['texture']), NumberToColour(track['colour']), NumberToMood(track['mood']), NumberToTimeSignature(track['time']))
    output += 'The key of %s %s at %sbpm.\n' % (NumberToKey(track['key']), NumberToMode(track['mode']), NumberToBPM(track['tempo']))
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
  print(GenerateAlbumText(album, args.output_format))

if __name__ == '__main__':
  main()
