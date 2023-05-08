# Import the regular expression module
import re

# Define the Rule function
# It takes an output string and one or more patterns as input
# It returns a tuple containing the output string and a list of regular expressions created from the input patterns
# The name_group function is called for each input pattern to convert curly braces in the input pattern to named groups in the regular expression
def Rule(output, *patterns): 
    return (output, [name_group(pat) + '$' for pat in patterns])

# Define the name_group function
# It takes a string pattern as input and replaces curly braces in the pattern with named groups in a regular expression
# For example, it replaces "{P}" with "(?P<P>.+?)" which means 'match 1 or more characters, and call it P'.
def name_group(pat):
    return re.sub('{(.)}', r'(?P<\1>.+?)', pat)

# Define the word function
# It takes a string as input and returns a regular expression that matches the given string as a complete word
# It adds '\b' (word boundary) at the start and end of the word to ensure that it matches only complete words and not just a substring
def word(w):
    return r'\b' + w + r'\b' # '\b' matches at word boundary

# Define a list of rules
# Each rule is defined using the Rule function
# It specifies an output string and one or more patterns to match against the input sentence
rules = [
    Rule('{P} ⇒ {Q}',         'if {P} then {Q}', 'if {P}, {Q}'),
    Rule('{P} ⋁ {Q}',          'either {P} or else {Q}', 'either {P} or {Q}'),
    Rule('{P} ⋀ {Q}',          'both {P} and {Q}'),
    Rule('～{P} ⋀ ～{Q}',       'neither {P} nor {Q}'),
    Rule('～{A}{P} ⋀ ～{A}{Q}', '{A} neither {P} nor {Q}'), 
    Rule('～{Q} ⇒ {P}',        '{P} unless {Q}'),
    Rule('{P} ⇒ {Q}',          '{Q} provided that {P}', '{Q} whenever {P}', 
                               '{P} implies {Q}', '{P} therefore {Q}', 
                               '{Q}, if {P}', '{Q} if {P}', '{P} only if {Q}'),
    Rule('{P} ⋀ {Q}',          '{P} and {Q}', '{P} but {Q}'),
    Rule('{P} ⋁ {Q}',          '{P} or else {Q}', '{P} or {Q}'),
]

# Define a list of negations
# Each negation is a tuple containing a regular expression to match the negation and a string to replace it with (to handle negations)
negations = [
    (word("not"), ""),
    (word("cannot"), "can"),
    (word("can't"), "can"),
    (word("won't"), "will"),
    (word("ain't"), "is"),
    ("n't", ""), # matches as part of a word: didn't, couldn't, etc.
]

# Define the match_rules function
# It takes a natural language sentence, a set of rules, and a dictionary of definitions as input
# It applies each rule to the sentence in turn and returns a tuple containing the logical expression and the updated definitions dictionary
# If no rule matches, it calls the match_literal function to add the proposition to the definitions dictionary and handle negations
def match_rules(sentence, rules, defs):
    sentence = clean(sentence)
    for rule in rules:
        result = match_rule(sentence, rule, defs)
        if result: 
            return result
    return match_literal(sentence, negations, defs)
 
# Define the match_rule function
# It takes a natural language sentence, a rule, and a dictionary of definitions as input
# It applies the rule to the sentence and returns a tuple containing the logical expression and the updated definitions dictionary
# It uses the regular expressions generated from the input patterns in the rule to match against the sentence
# If the pattern matches, it recursively applies the match_rules function to each matching group to generate the logical expression
def match_rule(sentence, rule, defs):
    output, patterns = rule
    for pat in patterns:
        match = re.match(pat, sentence, flags=re.I)
        if match:
            groups = match.groupdict()
            for P in sorted(groups): # Recursively apply rules to each of the matching groups
                groups[P] = match_rules(groups[P], rules, defs)[0]
            return '(' + output.format(**groups) + ')', defs

# Define the match_literal function
# It takes a natural language sentence, a set of negations, and a dictionary of definitions as input
# It handles negations in the sentence and adds the proposition to the definitions dictionary
# It returns a tuple containing the logical expression and the updated definitions dictionary
def match_literal(sentence, negations, defs):
    polarity = ''
    for (neg, pos) in negations:
        (sentence, n) = re.subn(neg, pos, sentence, flags=re.I)
        polarity += n * '～'
    sentence = clean(sentence)
    P = proposition_name(sentence, defs)
    defs[P] = sentence
    return polarity + P, defs

# Define the proposition_name function
# It takes a natural language sentence, a dictionary of definitions, and a string of names as input
# It returns a unique name for the proposition based on the sentence
# If the sentence has been encountered before, it returns the previously used name
# Otherwise, it returns a new unused name
def proposition_name(sentence, defs, names='PQRSTUVWXYZBCDEFGHJKLMN'):
    sentence = clean(sentence)
    for key, value in defs.items():
        if sentence == value:
            return key
    for name in names:
        if name not in defs:
            return name
    raise Exception("Too many propositions")

# Define the clean function
# It takes a string as input and removes redundant whitespace, converts curly apostrophes to straight apostrophes, and removes trailing commas and periods
def clean(text):
    return re.sub(r"\s+", " ", text.strip().replace('’', "'").replace('‘', "'")).rstrip('.,!?')

# Define the logic function
# It takes a list of natural language sentences and a maximum width as input
# It loops over each sentence in the list, applies the match_rules function to each sentence, and prints the original sentence, the logical expression, and the associated definitions
def logic(sentences, width=80):
    defs = {}
    for s in sentences:
        (logical, defs) = match_rules(s, rules, defs)
        print(f"{s:{width}} -> {logical:{width}} : {defs}")