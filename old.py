















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