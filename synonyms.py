'''Semantic Similarity: starter code

Author: Michael Guerzhoy. Last modified: Nov. 14, 2016.
'''

import math

def norm(vec):
    '''Return the norm of a vector stored as a dictionary,
    as described in the handout for Project 3.
    '''
    
    sum_of_squares = 0.0  
    for x in vec:
        sum_of_squares += vec[x] * vec[x]
    
    return math.sqrt(sum_of_squares)



def sim_euc (v1, v2):
    for key1 in v1:
        if key1 not in v2:
            v2 [key1] = 0
        
    for key2 in v2:
        if key2 not in v1:
            v1 [key2] = 0
    
    temp = []
    for key in v1:
        temp.append (v1[key] - v2[key])
    
    sum = 0
    for i in temp:
        sum += i*i
    return (-1)*math.sqrt(sum)
        
    
def sim_euc_norm (v1, v2):
    for key1 in v1:
        if key1 not in v2:
            v2 [key1] = 0
        
    for key2 in v2:
        if key2 not in v1:
            v1 [key2] = 0
            
    sum = 0
    for i in v1:    
        sum += v1[i]**2
    new_v1 = {}
    sum = math.sqrt (sum)
    for i in v1:
        new_v1 [i] = (v1[i]/sum)
     
    sum = 0 
    for i in v2:
        sum += v2[i]**2
    new_v2 = {}
    sum = math.sqrt (sum)
    for i in v2:
        new_v2[i] = (v2[i]/sum)
        
    temp = []
    for key in new_v1:
        temp.append (new_v1[key] - new_v2[key])
    
    sum = 0
    for i in temp:
        sum += i*i
    
    return (-1)*math.sqrt(sum)
                
    

def cosine_similarity(vec1, vec2):
    num = 0
    for key in vec1:
        if key in vec2:
            num+= vec1[key]*vec2[key]
    den1 = 0
    for key in vec1:
        den1 += vec1 [key]**2 
    den2 = 0
    for key in vec2:
        den2 += vec2[key]**2
    return (num / math.sqrt(den1*den2))


def build_semantic_descriptors(sentences):
    semantic_descriptors = {}
    for sentence in sentences:
        for key in sentence:
            if key not in semantic_descriptors:
                semantic_descriptors [key] = {}
            for word in sentence:
                if word != key:
                    if word in semantic_descriptors [key]:
                        semantic_descriptors [key] [word] +=1
                    else:
                        semantic_descriptors [key] [word] = 1
    return semantic_descriptors


def sentence_sep (sentence):
    sentence = sentence.replace (",", "")
    sentence = sentence.replace ("-", "")
    sentence = sentence.replace (":", "")
    sentence = sentence.replace (";", "")
    sentence = sentence.replace ("'s", "")
    return (sentence.split (" "))
    
    

def build_semantic_descriptors_from_files(filenames):
    text = ""
    for i in range (len (filenames)):
        text += (open(filenames[i], "r", encoding="latin1")).read()
    text = text.lower()
    
    text.replace ("!", ".")
    text.replace ("?", ".")
    text.replace ("\n", " ")
    sentences = text.split (". ")
    L = []
    for sentence in sentences:
        L.append (sentence_sep(sentence))
    return build_semantic_descriptors (L)
    

def most_similar_word(word, choices, semantic_descriptors, similarity_fn):
    most_similar_word = ""
    max_similarity = -100000
    if word in semantic_descriptors:
        vec1 = semantic_descriptors [word]
        for choice in choices:
            if choice in semantic_descriptors:
                if max_similarity < similarity_fn (vec1, semantic_descriptors[choice]):
                    max_similarity = similarity_fn (vec1, semantic_descriptors[choice])
                    most_similar_word = choice
    return most_similar_word
    

def run_similarity_test(filename, semantic_descriptors, similarity_fn):
    text= open(filename,"r",encoding="latin1").read()
    questions = text.split ("\n")
    correct = 0
    for i in range (len(questions)):
        L = questions [i].split (" ")
        if (len(L) > 3):
            if L [1] == most_similar_word(L[0], L[2:], semantic_descriptors, similarity_fn):
                correct += 1
        
    return correct/ len(questions)


if __name__ == '__main__':
     filenames = ["text1.txt", "text2.txt"]
     semantic_descriptors = build_semantic_descriptors_from_files(filenames)
     filename = "testtext.txt"
     #similarity_fn = cosine_similarity
     #similarity_fn = sim_euc
     similarity_fn = sim_euc_norm
     print (run_similarity_test(filename, semantic_descriptors, similarity_fn))
    