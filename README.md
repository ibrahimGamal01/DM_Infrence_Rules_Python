# DM_Infrence_Rules_Python

Sure! Here's a possible README file:

# English to Logic Translator

This program translates English sentences into logical statements using a set of predefined rules. It is implemented in Python, and uses regular expressions to match the input sentences against the rules.

## Usage

To use the program, you can import the module and call the `match_rules` function with a sentence, a list of rules, and an optional dictionary of definitions. The function will return a tuple containing the logical statement and the definitions.

```Python
import english_to_logic as etl

# Define some rules
rules = [
    etl.Rule('{P} ⇒ {Q}', 'if {P} then {Q}'),
    etl.Rule('{P} ⋁ {Q}', 'either {P} or else {Q}'),
    ...
]

# Translate a sentence
sentence = 'If today is Tuesday, I have a test in English'
logic, defs = etl.match_rules(sentence, rules)

print('English:', sentence)
print('Logic:', logic)
print('Definitions:', defs)
```

Alternatively, you can use the `logic` function to translate a list of sentences and print the results.

```Python
import english_to_logic as etl

# Define some sentences
sentences = [
    'If today is Tuesday, I have a test in English.',
    'It is Tuesday.',
    ...
]

# Translate and print the sentences
etl.logic(sentences)
```

## Rules

The program comes with a set of predefined rules that cover some common sentence structures. Each rule is defined as a tuple containing an output and one or more patterns. The patterns are regular expressions that match the input sentences, and the output is a template string that defines the logical statement.

For example, the rule `{P} ⇒ {Q}` translates the English sentence "If P, then Q" into the logical statement "P implies Q". The rule has two patterns: "if {P} then {Q}" and "if {P}, {Q}". These patterns match the sentence "If today is Tuesday, I have a test in English" and extract the variables "today is Tuesday" and "I have a test in English".

## Negations

The program also handles negations by replacing them with their positive counterparts. For example, the word "not" is negated to an empty string, and the word "cannot" is negated to "can". The list of negations is defined in the `negations` variable, and can be modified or extended as needed.

## Definitions

The program keeps track of the propositions used in the logical statements by assigning them unique names. The names are generated automatically using a list of letters, and are stored in a dictionary along with their English definitions. The definitions are used to provide context for the propositions, and can be printed along with the logical statements.

Continuing from the previous points:

13. The code then calls the "match_rule" function to test a single sentence against a specific rule and prints the result.

```Python
import english_to_logic as etl

# Define a rule
rule = etl.Rule('{P} ⇒ {Q}', 'if {P} then {Q}')

# Test a sentence
sentence = 'If today is Tuesday, I have a test in English'
logic, defs = etl.match_rule(sentence, rule)

print('English:', sentence)
print('Logic:', logic)
print('Definitions:', defs)
```

14. The "sentences" variable contains a string of several English sentences separated by periods, which can be split into a list of individual sentences using the `split()` method.

```Python
import english_to_logic as etl

# Define some sentences
sentences = 'If today is Tuesday, I have a test in English. It is Tuesday.'

# Split the sentences and remove any empty strings
sentences = [s.strip() for s in sentences.split('.') if s.strip()]

# Translate and print the sentences
etl.logic(sentences)
```

15. The "logic" function takes a list of sentences and a width parameter, which determines the maximum width of the output lines. For each sentence, it calls the "match_rules" function to match the sentence against the rules and generate a logical statement. It then prints the English sentence, the logical statement, and the definitions using the `wrap()` method to format the output.

```Python
import english_to_logic as etl

# Define some sentences
sentences = [
    'If today is Tuesday, I have a test in English.',
    'It is Tuesday.'
]

# Translate and print the sentences
etl.logic(sentences, width=80)
```

The `width` parameter is optional and defaults to 80. If set to None or a negative value, the output lines will not be wrapped.


## License

This program is released under the MIT License. Feel free to use, modify, and distribute it as needed.
