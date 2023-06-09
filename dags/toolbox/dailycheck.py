import os

def check_files(path):
    names = [c for a,b,c in os.walk(path)]
    if ("Answers.csv" in names[0]) & ("Questions.csv" in names[0]):
        return f'End'
    else:
        return f'ClearFile'
