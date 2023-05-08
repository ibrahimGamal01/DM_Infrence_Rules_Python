


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












# def implication_rule(premise1, premise2):
#     """
#     If premise1 implies premise2, and premise1 is true, then premise2 must be true.
#     """
#     if premise1["value"] is True and premise2["type"] == "or":
#         return premise2
#     else:
#         return None


# def modus_tollens_rule(premise1, premise2):
#     """
#     If premise1 implies premise2, and premise2 is false, then premise1 must be false.
#     """
#     if premise2["value"] is False and premise1["type"] == "not":
#         return not_operator(premise1["prop"])
#     else:
#         return None


# def modus_ponens_rule(premise1, premise2):
#     """
#     If premise1 is true, and premise2 is the conclusion of an implication where premise1 is the premise,
#     then premise2 must be true.
#     """
#     if premise1["value"] is True and premise2["type"] == "or":
#         left_prop = premise2["left"]
#         right_prop = premise2["right"]
#         if left_prop["type"] == "not" and left_prop["prop"]["name"] == premise1["name"]:
#             return not_operator(right_prop)
#         elif right_prop["type"] == "not" and right_prop["prop"]["name"] == premise1["name"]:
#             return not_operator(left_prop)
#     return None


# def disjunctive_syllogism_rule(premise1, premise2):
#     """
#     If premise1 is a disjunction and one of its disjuncts is false, and premise2 is the other disjunct,
#     then premise2 must be true.
#     """
#     if premise1["type"] == "or":
#         left_prop = premise1["left"]
#         right_prop = premise1["right"]
#         if left_prop["value"] is False and right_prop["name"] == premise2["name"]:
#             return right_prop
#         elif right_prop["value"] is False and left_prop["name"] == premise2["name"]:
#             return left_prop
#     return None


# def conjunction_rule(premise1, premise2):
#     """
#     If premise1 and premise2 are true, then the conjunction of premise1 and premise2 is true.
#     """
#     if premise1["value"] is True and premise2["value"] is True:
#         return and_operator(premise1, premise2)
#     else:
#         return None


# def simplification_rule(premise):
#     """
#     If a conjunction is true, then its conjuncts are true.
#     """
#     if premise["type"] == "and" and premise["left"]["value"] is True and premise["right"]["value"] is True:
#         return [premise["left"], premise["right"]]
#     else:
#         return None


# def addition_rule(premise):
#     """
#     If a proposition is true, then its disjunction with any other proposition is true.
#     """
#     if premise["value"] is True:
#         return or_operator(premise, proposition("P"))
#     else:
#         return None


# def double_negation_rule(premise):
#     """
#     If a proposition is true, then the double negation of that proposition is true.
#     """
#     if premise["value"] is True:
#         return not_operator(not_operator(premise["prop"]))
#     else:
#         return None


# def hypothetical_syllogism_rule(premise1, premise2):
#     """
#     If premise1 implies premise2, and premise2 implies premise3, then premise1 implies premise3.
#     """
#     if premise1["type"] == "or" and premise2["type"] == "or":
#         left_prop1 = premise1["left"]
#         right_prop1 = premise1["right"]
#         left_prop2 = premise2["left"]
#         right_prop2 = premise2["right"]
#         if left_prop1["type"] == "not" and left_prop1["prop"]["name"] == left_prop2["name"]:
#             return implication_operator(right_prop1, right_prop2)
#         elif right_prop1["type"] == "not" and right_prop1["prop"]["name"] == left_prop2["name"]:
#             return implication_operator(left_prop1, right_prop2)
#         elif left_prop1["type"] == "not" and left_prop1["prop"]["name"] == right_prop2["name"]:
#             return implication_operator(right_prop1, left_prop2)
#         elif right_prop1["type"] == "not" and right_prop1["prop"]["name"] == right_prop2["name"]:
#             return implication_operator(left_prop1, left_prop2)
#     return None


# def exportation_rule(premise):
#     """
#     If a proposition is a conjunction, then it can be replaced by an implication where the left conjunct implies
#     a proposition that is a conjunction of the right conjunct and the original consequent.
#     """
#     if premise["type"] == "and":
#         left_prop = premise["left"]
#         right_prop = premise["right"]
#         consequent = proposition("Q")
#         antecedent = and_operator(right_prop, consequent)
#         return implication_operator(left_prop, antecedent)
#     else:
#         return None


# def solve_inference_rules(knowledge_base, premises):

#     result = None
#     for premise_name in premises:
#         premise = get_proposition(knowledge_base, premise_name)

#         # Apply modus ponens
#         if result is None:
#             result = modus_ponens_rule(premise, premise)
#             if result is not None:
#                 break

#         # Apply modus tollens
#         if result is None:
#             result = modus_tollens_rule(premise, premise)
#             if result is not None:
#                 break

#         # Apply disjunctive syllogism
#         if result is None:
#             result = disjunctive_syllogism_rule(premise, premise)
#             if result is not None:
#                 break

#         # Apply conjunction
#         if result is None:
#             for premise2_name in premises:
#                 if premise_name == premise2_name:
#                     continue
#                 premise2 = get_proposition(knowledge_base, premise2_name)
#                 result = conjunction_rule(premise, premise2)
#                 if result is not None:
#                     break
#             if result is not None:
#                 break

#         # Apply simplification
#         if result is None:
#             result = simplification_rule(premise)
#             if result is not None:
#                 break

#         # Apply addition
#         if result is None:
#             result = addition_rule(premise)
#             if result is not None:
#                 break

#         # Apply double negation
#         if result is None:
#             result = double_negation_rule(premise)
#             if result is not None:
#                 break

#         # Apply hypothetical syllogism
#         if result is None:
#             for premise2_name in premises:
#                 if premise_name == premise2_name:
#                     continue
#                 premise2 = get_proposition(knowledge_base, premise2_name)
#                 result = hypothetical_syllogism_rule(premise, premise2)
#                 if result is not None:
#                     break
#             if result is not None:
#                 break

#         # Apply exportation
#         if result is None:
#             result = exportation_rule(premise)
#             if result is not None:
#                 break

#     return result


# if __name__ == "__main__":
#     # Define the premises
#     premises = ["T", "-E", "T^A", "E|S"]

#     # Define the knowledge base
#     knowledge_base = {
#         "T": proposition("T"),
#         "E": proposition("E"),
#         "S": proposition("S"),
#         "-E": not_operator(proposition("E")),
#         "T^A": and_operator(proposition("T"), not_operator(proposition("E"))),
#         "E|S": or_operator(proposition("E"), proposition("S")),
#     }

#     # Solve the inference rules problem
#     steps = [
#         (3, 4, "simplification"),
#         (4, 6, "modus ponens"),
#         (5, 2, "modus tollens"),
#         (6, 7, "disjunctive syllogism"),
#     ]
#     for step in steps:
#         premise1 = knowledge_base[premises[step[0]-1]]
#         premise2 = knowledge_base[premises[step[1]-1]]
#         conclusion = solve_inference_rules(knowledge_base, [premise1["name"], premise2["name"]])
#         knowledge_base[conclusion["name"]] = conclusion
#         print(f"From {step[0]} and {step[1]} we get {step[2]}. {conclusion['name']}")
