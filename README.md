# DM_Infrence_Rules_Python

# English to Logic Translator

This is a Python program that translates simple English sentences into logical statements using a set of predefined rules.

## Overview

The program consists of several functions that define the rules and handle the translation process. Here is an overview of each function:

- `Rule`: Takes an output and one or more patterns and returns a tuple containing the output and a list of patterns, where each pattern has been modified by the `name_group` function.

- `name_group`: Replaces "{Q}" in the input pattern with "(?P<Q>.+?)", which means "match 1 or more characters, and call it Q".

- `word`: Returns a regular expression that matches "w" as a complete word, not just as a sequence of letters.

- `rules`: A list of several examples of rules that map English sentences to logical statements.

- `negations`: A list of pairs of words, where the first word is a negation and the second word is its positive counterpart.

- `match_rules`: Takes a sentence, a list of rules, and a dictionary of definitions. It first cleans the sentence by removing redundant whitespace, and then tries to match the sentence against each rule in the list using the `match_rule` function. If a match is found, it returns the logical statement and the definitions. If no match is found, it calls the `match_literal` function to handle negations and add new propositions to the dictionary.

- `match_rule`: Takes a sentence, a rule, and a dictionary of definitions. It tries to match the sentence against each pattern in the rule using regular expressions. If a match is found, it returns the output with the matched groups replaced by their corresponding logical statements, and the definitions. If no match is found, it returns None.

- `match_literal`: Takes a sentence, a list of negations, and a dictionary of definitions. It first handles negations by replacing them with their positive counterparts, and then creates a new proposition name for the sentence using the `proposition_name` function. It adds the proposition to the definitions dictionary and returns the logical statement and the definitions.

- `proposition_name`: Takes a sentence, a dictionary of definitions, and a list of proposition names. It checks if the sentence has been used before and returns its old name if it has, or a new unused name if it hasn't.

- `clean`: Takes a text and cleans it by removing redundant whitespace, replacing curly apostrophes with straight ones, and removing trailing commas and periods.

- `logic`: Takes a list of English sentences and an optional width parameter. It splits the sentences into individual sentences using the `split` method, cleans each sentence using the `clean` function, and then calls the `match_rules` function to translate each sentence into a logical statement. It then prints the English sentence, the logical statement, and the definitions using the `textwrap` module to format the output.

## Usage

To use the program, you need to import the `english_to_logic` module and call the `logic` function with a list of English sentences. Here is an example:

```Python
import english_to_logic as etl

sentences = [
    'If today is Tuesday, I have a test in English.',
    'It is Tuesday.'
]

etl.logic(sentences)
```

This will output:

```
English: If today is Tuesday, I have a test in English.

Logic: (P ⇒ Q)
P: today is Tuesday
Q: I have a test in English

English: It is Tuesday.

Logic: Q
Q: It is Tuesday
```

You can also specify the maximum width of the output lines using the `width` parameter:

```Python
etl.logic(sentences, width=50)
```

This will output:

```
English: If today is Tuesday, I have a test in
         English.

Logic: (P ⇒ Q)
P: today is Tuesday
Q: I have a test in English

English: It is Tuesday.

Logic: Q
Q: It is Tuesday
```

## License

This program is released under the MIT License. Feel free to use, modify, and distribute it as needed.
