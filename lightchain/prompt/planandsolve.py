from dataclasses import dataclass

@dataclass
class PlanAndSolve:
    ENTRY = "Let's first understand the problem and devise a plan to solve the problem. \n Then, let's carry out the plan and solve the problem step by step"
    VARIABLES = r"extract relevant variables and their corresponding numerals"
    CALCULATE = r"calculate intermediate results (pay attention to calculation and commonsense)"