import pandas as pd
import requests
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from bs4 import BeautifulSoup
import re
import nltk

import spacy
nltk.download('punkt')
nltk.download("stopwords")

#openeing extracted text file
with open("id-02.txt", "r") as myfile:
    string = myfile.read()
    words = string.split()  #
#negative dictionary
with open("negative-words.txt", "r") as myfile:
    negativestring = myfile.read()
    negativewords = negativestring.split()
#positive dictonary
with open("positive-words.txt", "r") as myfile:
    positivestring = myfile.read()
    positivewords = positivestring.split()



df = pd.read_excel('input.xlsx')
links = [x for x in df['URL']]
#print( links)
#textreport = []
##for url in links:
   # headers = {
      #  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
   # }
    #r = requests.get(url,headers=headers)
    #data = r.text
    #soup = BeautifulSoup(data, "html.parser")
    #textreport.append(soup.get_text())

#print(f'Total {len(textreport)} reports saved')

#print(textreport)##
def break_sentences(string):
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(string)
    return list(doc.sents)


print(break_sentences(string))

#loading stopwords
with open('stopwords.txt','r') as f:
    stop_words = f.read()
    stop_words = stop_words.split('\n')
print(f'Total number of Stop Words are {len(stop_words)}')
#creating positive and negative dictionary
positive_dictionary = [x for x in positivewords if x not in stop_words]
negative_dictionary = [x for x in negativewords if x not in stop_words]

def tokenize(string):
    string = re.sub(r'[^A-Za-z]', ' ', string.upper())
    tokenized_words = word_tokenize(string)
    return tokenized_words



print("\t\t\t SENTIMENTAL ANALYSIS")
#tokenizing
string = re.sub(r'[^A-Za-z]',' ',string.upper())
tokenized_words = word_tokenize(string)

#removing stop words
def remove_stopwords(words, stop_words):
    # define punctuation
    punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
    return [x for x in words if x not in stop_words  ]
words = remove_stopwords(tokenized_words, stop_words)
num_words = len(words)
print('Total no of words after cleaning:',num_words)

#calculatting word count
number_of_words = len(tokenize(string))


#creating positive and negative dictionary:
positive_dictionary = [x for x in positivewords if x not in stop_words]
negative_dictionary = [x for x in negativewords if x not in stop_words]
#required methods for variables:
def countscore(store, cleanwords):
    score= 0
    for x in cleanwords:
        if(x in store):
            score = score +1
    return score
def clean_text(store, stop_words):
    cleaned_text= []
    for x in store:
        if(x not in stop_words):
            cleaned_text.append(x)
    return cleaned_text
#extracting the derived variables:

#1.)positive score:
positive_score=countscore(positive_dictionary,clean_text(tokenize(string),stop_words))
print('The positive score is:',positive_score)

#2.)Negative score:
negative_score=countscore(negative_dictionary,clean_text(tokenize(string),stop_words))
print('The negative score is:',negative_score)

#3.)polarity score:
#function to find polarity score
def polarity(positive_score, negative_score):
    return (positive_score - negative_score)/((positive_score + negative_score)+ 0.000001)
polarity_score=polarity(positive_score,negative_score)
print('The polarity score is:',polarity_score)

#4.)subjectivity score:
#To find subjectivity score
def subjectivity(positive_score, negative_score, num_words):
    return (positive_score+negative_score)/(num_words+ 0.000001)
print('Subjectivity score is:',subjectivity(positive_score,negative_score,num_words))

#NEXT SECTION

print('\t\t\t ANALYSIS OF READABILITY')
#1.)Average sentence length:
def word_count(string):
    sentences = break_sentences(string)
    words = 0
    for sentence in sentences:
        words += len([token for token in sentence])
    return words



# Returns the number of sentences in the text
def sentence_count(string):
    sentences = break_sentences(string)
    return len(sentences)
print('Number of sentences',sentence_count(string))


# Returns average sentence length
def avg_sentence_length(string):
    words = word_count(string)
    sentences = sentence_count(string)
    average_sentence_length = float(words / sentences)
    return average_sentence_length
print('The average sentence length is:',avg_sentence_length(string))

#2.)percentage of complex words
#to find complex word
def syllable_morethan2(word):
    if (len(word) > 2 and (word[-2:] == 'es' or word[-2:] == 'ed')):
        return False

    count = 0
    vowels = ['a', 'e', 'i', 'o', 'u']
    for i in word:
        if (i.lower() in vowels):
            count = count + 1

    if (count > 2):
        return True
    else:
        return False
num_complexword=0
for word in words:
    if (syllable_morethan2(word)):
        num_complexword = num_complexword + 1

#to find percentage of complex words:
percentage_complexwords = num_complexword/num_words
print('The percentage of complex words in text are:',percentage_complexwords)

#3.)to find fog index:
#to find fog index:
def fog_index_cal(average_sentence_length, percentage_complexwords):
    return 0.4*(average_sentence_length + percentage_complexwords)
fog_index = fog_index_cal(avg_sentence_length(string), percentage_complexwords)
print('The fog index of given text file is:',fog_index)

# Next section
print('\t\t\t AVERAGE NUMBER OF WORDS PER SENTENCE')
def avg_number_of_words(text):
 final_sentence = text.split(".") #split the text into a list of sentences.
 final_words = text.split(" ") #split the input text into a list of separate word
 return len(final_words)/len(final_sentence)
print(avg_number_of_words(string))
#Next Section
print('\t\t\tCOMPLEX WORD COUNT')
print('Total number complex words are:',num_complexword)

#Next Section
print('\t\t\tWord COUNT')
def word_count(words, stop_words):
    # define punctuation
    punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
    return [x for x in words if x not in stop_words and x for x in words if x not in punctuations]
words = word_count(tokenized_words, stop_words)
count = len(words)
print('Total no of words before cleaning are:',number_of_words)
print('Total no of words after cleaning:',count)

# Next Section
print('\t\t\t Syllable count per word')
def syllable_count(word):
    if(word[-2:]=='es' or word[-2:]=='ed'):
        return False
    count=0
    vowels = ['a','e','i','o','u']
    for i in word:
        if(i.lower() in vowels):
            count = count +1
            return count
Syllable_count=0
for word in words:
    if (syllable_count(word)):
        Syllable_count = Syllable_count + 1
print(Syllable_count)

#Next section
print('\t\t\tPersonal Pronouns')
pronouns =['I','WE','we','my','MY','OURS','our','us','i']
def score(store, dictonary):
    score= 0
    for x in dictonary:
        if(x in store):
            score = score +1
    return score
print('Number of personal pronouns in text are:',score(string,pronouns))

#Next Section
print('\t\t\tAverage Word Length')

f = open("id-02.txt", "r")  # Step 1
data = f.read()  # Step 2
avg_word = data.split()  # Step 3 and 4
avg_number_of_words = avg_word # Step 5
average = sum(len(word) for word in avg_number_of_words) / len(avg_number_of_words)

print('The Average word length is:',average)














