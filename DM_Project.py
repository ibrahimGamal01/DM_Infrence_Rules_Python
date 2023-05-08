#module have funs to search a str for match
import re

#produce output if the input matches any pattern
def Rule(output, *patterns): 
    return (output, [name_group(pat) + '$' for pat in patterns])

#Replace '{Q}' with '(?P<Q>.+?)', which means 'match 1 or more characters, and call it Q'
def name_group(pat):
    return re.sub('{(.)}', r'(?P<\1>.+?)', pat)

#Return a regex that matches w as a complete word not letters             
def word(w):
    return r'\b' + w + r'\b' # '\b' matches at word boundary


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

negations = [
    (word("not"), ""),
    (word("cannot"), "can"),
    (word("can't"), "can"),
    (word("won't"), "will"),
    (word("ain't"), "is"),
    ("n't", ""), # matches as part of a word: didn't, couldn't, etc.
    ]

##Match sentence against all the rules
#return the logic translation and  english def
def match_rules(sentence, rules, defs):
    sentence = clean(sentence)
    for rule in rules:
        result = match_rule(sentence, rule, defs)
        if result: 
            return result
    return match_literal(sentence, negations, defs)
 
 #return logic transition and the dict of def if the match succed  
 ##if match success return logic translation     
def match_rule(sentence, rule, defs):
    output, patterns = rule
    for pat in patterns:
        match = re.match(pat, sentence, flags=re.I)
        if match:
            groups = match.groupdict()
            for P in sorted(groups): # Recursively apply rules to each of the matching groups
                groups[P] = match_rules(groups[P], rules, defs)[0]
            return '(' + output.format(**groups) + ')', defs

#if No rule matched;  Add new proposition to defs. Handle negation.        
def match_literal(sentence, negations, defs):
    polarity = ''
    for (neg, pos) in negations:
        (sentence, n) = re.subn(neg, pos, sentence, flags=re.I)
        polarity += n * '～'
    sentence = clean(sentence)
    P = proposition_name(sentence, defs)
    defs[P] = sentence
    return polarity + P, defs

#Return the old name for this sentence, if used before, or a new, unused name
def proposition_name(sentence, defs, names='PQRSTUVWXYZBCDEFGHJKLMN'):
    inverted = {defs[P]: P for P in defs}
    if sentence in inverted:
        return inverted[sentence]                      # Find previously-used name
    else:
        return next(P for P in names if P not in defs) # Use a new unused name

#Remove redundant whitespace; handle curly apostrophe and trailing comma/period    
def clean(text): 
    return ' '.join(text.split()).replace("’", "'").rstrip('.').rstrip(',')
match_rule("If today is Tuesday, I have a test in english",
           Rule('{P} ⇒ {Q}', 'if {P}, {Q}'),
           {})

sentences = ''' if today is Tuesday, I have a test in english, it is Tuesday'''.split('.')

#to make sure every str (input) at most width
import textwrap
#match rules against each sentence in txt and print result
def logic(sentences, width=80): 
    for s in map(clean, sentences):
        logic, defs = match_rules(s, rules, {})
        print('\n' + textwrap.fill('English: ' + s +'.', width), '\n\nLogic:', logic)
        for P in sorted(defs):
            print('{}: {}'.format(P, defs[P]))
            
logic(sentences)