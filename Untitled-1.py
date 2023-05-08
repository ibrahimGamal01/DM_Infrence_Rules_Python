# %%
#module have funs to search a str for match
import re

# %%
#produce output if the input matches any pattern
def Rule(output, *patterns): 
    return (output, [name_group(pat) + '$' for pat in patterns])

#Replace '{Q}' with '(?P<Q>.+?)', which means 'match 1 or more characters, and call it Q'
def name_group(pat):
    return re.sub('{(.)}', r'(?P<\1>.+?)', pat)

#Return a regex that matches w as a complete word not letters             
def word(w):
    return r'\b' + w + r'\b' # '\b' matches at word boundary

# %%
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

# %%
##Match sentence against all the rules
#return the logic translation and  english def
def match_rules(sentence, rules, defs):
    sentence = clean(sentence)
    for rule in rules:
        result = match_rule(sentence, rule, defs)
        if result: 
            return result
    return match_literal(sentence, negations, defs)

# %%
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


# %%
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


# %%
#Return the old name for this sentence, if used before, or a new, unused name
def proposition_name(sentence, defs, names='PQRSTUVWXYZBCDEFGHJKLMN'):
    inverted = {defs[P]: P for P in defs}
    if sentence in inverted:
        return inverted[sentence]                      # Find previously-used name
    else:
        return next(P for P in names if P not in defs) # Use a new unused name


# %%
#Remove redundant whitespace; handle curly apostrophe and trailing comma/period    
def clean(text): 
    return ' '.join(text.split()).replace("’", "'").rstrip('.').rstrip(',')
match_rule("If today is Tuesday, I have a test in english",
           Rule('{P} ⇒ {Q}', 'if {P}, {Q}'),
           {})

sentences = ''' if today is Tuesday, I have a test in english, it is Tuesday'''.split('.')


# %%
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

# %% [markdown]
# # --------------------------------------------------------------------------

# %%
def match_rule(sentence, output, patterns, defs):
    key = (output, tuple(patterns))  # Use a tuple of (output, tuple(patterns)) as the cache key
    if key in match_rule.cache:
        return match_rule.cache[key]
    pattern_str = r'\b' + '|'.join([f'(?P<P{i+len(patterns)}>{p})' for i, p in enumerate(output.split())] + [f'(?P<P{i}>{p})' for i, p in enumerate(patterns)]) + r'\b'  # Use unique group names for each variable in output and patterns
    groups = re.match(pattern_str, sentence)
    if groups:
        groups = groups.groupdict()
        for i, P in enumerate(output.split()):
            if f'P{i+len(patterns)}' in groups and P not in patterns:
                groups[f'P{i+len(patterns)}'], defs = match_rule(sentence, output, patterns + [groups[f'P{i+len(patterns)}']], defs)
        result = '(' + output.format(**groups) + ')', defs
    else:
        result = '', defs
    match_rule.cache[key] = result
    return result
match_rule.cache = {}  # Initialize the cache as an empty dictionary

def match_rules(sentence, rules, defs={}):
    key = str((tuple(rules), defs))  # Use a string representation of (tuple(rules), defs) as the cache key
    if key in match_rules.cache:
        return match_rules.cache[key]
    sentence = clean(sentence)
    for rule in rules:
        result, defs = match_rule(sentence, *rule, defs)
        if result: 
            match_rules.cache[key] = result, defs
            return result, defs
    match_rules.cache[key] = None, defs
    return None, defs
match_rules.cache = {}  # Initialize the cache as an empty dictionary

# %%
def modus_ponens(P_Q, P):
    P_Q = P_Q.strip('()')
    P, Q = P_Q.split('⇒')
    if P.strip() == P and Q.strip() == Q:
        if P.strip() == P_Q.strip():
            return Q.strip()
    return None

# %%
def hypothetical_syllogism(P_Q, Q_R):
    P_Q = P_Q.strip('()')
    Q_R = Q_R.strip('()')
    P, Q = P_Q.split('⇒')
    Q, R = Q_R.split('⇒')
    if P.strip() == P and Q.strip() == Q and R.strip() == R:
        if Q.strip() == Q_R.strip().split('⇒')[0].strip():
            return P.strip() + ' ⇒ ' + R.strip()
    return None

# %%
def simplification(P_and_Q):
    P_and_Q = P_and_Q.strip('()')
    P, Q = P_and_Q.split('⋀')
    return P.strip() or Q.strip()

# %%
def conjunction(P, Q):
    return P.strip() + ' ⋀ ' + Q.strip()

# %%
def modus_tollens(P_Q, not_Q):
    P_Q = P_Q.strip('()')
    P, Q = P_Q.split('⇒')
    if P.strip() == P and Q.strip() == Q:
        if '～' + Q.strip() == not_Q.strip():
            return '～' + P.strip()
    return None

def disjunctive_syllogism(P_or_Q, not_P):
    P_or_Q = P_or_Q.strip('()')
    P, Q = P_or_Q.split('⋁')
    if '～' + P.strip() == not_P.strip():
        return Q.strip()
    elif '～' + Q.strip() == not_P.strip():
        return P.strip()
    return None

def resolution(P, not_P):
    if P.strip() == '～' + not_P.strip():
        return ''
    return None

# %%
def test_inference_rules(propositions):
    for i, P in enumerate(propositions):
        for j, Q in enumerate(propositions):
            if i != j:
                P_Q = match_rules(P + ' ⇒ ' + Q, rules, {})[0]
                not_Q = '～' + Q.strip()
                if P_Q and not_Q in propositions:
                    # Modus Ponens
                    result = modus_ponens(P_Q, P)
                    if result:
                        return result
                    
                Q_R = match_rules(Q + ' ⇒ ' + P, rules, {})[0]
                if P_Q and Q_R:
                    # Hypothetical Syllogism
                    result = hypothetical_syllogism(P_Q, Q_R)
                    if result:
                        return result
                    
                if '⋁' in P:
                    # Disjunctive Syllogism
                    result = disjunctive_syllogism(P, not_Q)
                    if result:
                        return result
                    
                if '⋁' in Q:
                    # Disjunctive Syllogism
                    result = disjunctive_syllogism(Q, not_P=P)
                    if result:
                        return result
                    
                if '⋀' in P and '⋀' in Q:
                    # Simplification
                    result = simplification(P + ' ⋀ ' + Q)
                    if result:
                        return result
                    
                    # Conjunction
                    result = conjunction(P, Q)
                    if result:
                        return result
                    
                not_P = '～' + P.strip()
                if not_P in propositions:
                    # Modus Tollens
                    result = modus_tollens(Q_R, not_P)
                    if result:
                        return result
                    
                    # Disjunctive Syllogism
                    result = disjunctive_syllogism(P, not_P=not_P)
                    if result:
                        return result
                    
                    # Resolution
                    result = resolution(P, not_P)
                    if result:
                        return result
                    
    return None

# %%
propositions = ['today is Tuesday', 'I have a test in english, it is Tuesday']
result = test_inference_rules(propositions)
print(result)

# %%



