import re

#first permet de recupere le nombres données
def first(s):
    return(re.findall("\d+\.\d+|\d+", s))

#last permet de séparer le texte 
def last(s):
    return(re.split('(\d+)', s)[-1])