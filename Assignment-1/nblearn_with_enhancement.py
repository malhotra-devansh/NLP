import sys
import os
import json
import math

directory_path = sys.argv[1]
# directory_path = "/home/devansh/Desktop/NLP/SpamOrHam/train"
# directory_path = "/home/devansh/Desktop/NLP/SpamOrHam/train/1"

# ham_directory_path = os.path.join(directory_path, "ham")
# spam_directory_path = os.path.join(directory_path, "spam")
vocabulary = {}
output = {}
op = {}
mail_count = 0
ham_count = 0
spam_count = 0
total_words_in_ham = 0
total_words_in_spam = 0

for root, dirs, files in os.walk(directory_path, topdown=False):
    for name in files:
        #print(os.path.join(root,name))
        class_ = root.split('/')[-1]
        #print(class_)
        if class_ == 'ham':
            file_path = os.path.join(root,name)
            # file_path = ham_directory_path + "/" + filename
            with open(file_path, "r", encoding="latin1") as f:
                mail_count = mail_count + 1
                ham_count = ham_count + 1
                for word in f.read().split():
                    token = word.lower()
                    if token in vocabulary.keys():
                        vocabulary[token][0] = vocabulary[token][0] + 1
                        vocabulary[token][1] = vocabulary[token][1] + 1
                    else:
                        vocabulary[token] = [1]
                        vocabulary[token].append(1)
                        vocabulary[token].append(0)
                        # print(word.lower())
        elif class_ == 'spam':
            file_path = os.path.join(root,name)
            # file_path = ham_directory_path + "/" + filename
            with open(file_path, "r", encoding="latin1") as f:
                mail_count = mail_count + 1
                spam_count = spam_count + 1
                for word in f.read().split():
                    token = word.lower()
                    if token in vocabulary.keys():
                        vocabulary[token][0] = vocabulary[token][0] + 1
                        vocabulary[token][2] = vocabulary[token][2] + 1
                    else:
                        vocabulary[token] = [1]
                        vocabulary[token].append(0)
                        vocabulary[token].append(1)
                        # print(word.lower())


                        #print(root+dirs[0])
        #print(root+dirs[1])
        #print("\n" + path)
    # print("\n" + str(root))
    # print dirs
    # for name in files:
    #     if name not in ['.DS_Store', 'LICENSE', 'README.md', 'README.txt']:
    #         print("\n" + str(name))
    #         # totalFiles += 1
    #         # parentDirs = root.split('/')[1:3]

'''
# Compiling data for ham
for filename in os.listdir(ham_directory_path):
    file_path = os.path.join(ham_directory_path, filename)
    # file_path = ham_directory_path + "/" + filename
    with open(file_path, "r", encoding = "latin1") as f:
        mail_count = mail_count + 1
        ham_count = ham_count + 1
        for word in f.read().split():
            token = word.lower()
            if token in vocabulary.keys():
                vocabulary[token][0] = vocabulary[token][0] + 1
                vocabulary[token][1] = vocabulary[token][1] + 1
            else:
                vocabulary[token] = [1]
                vocabulary[token].append(1)
                vocabulary[token].append(0)
            # print(word.lower())

# Compiling data for spam
for filename in os.listdir(spam_directory_path):
    file_path = os.path.join(spam_directory_path, filename)
    # file_path = ham_directory_path + "/" + filename
    with open(file_path, "r", encoding="latin1") as f:
        mail_count = mail_count + 1
        spam_count = spam_count + 1
        for word in f.read().split():
            token = word.lower()
            if token in vocabulary.keys():
                vocabulary[token][0] = vocabulary[token][0] + 1
                vocabulary[token][2] = vocabulary[token][2] + 1
            else:
                vocabulary[token] = [1]
                vocabulary[token].append(0)
                vocabulary[token].append(1)
            # print(word.lower())
'''

vocabulary_length = len(vocabulary)

# Computing total words in ham and spam respectively
for key, value in vocabulary.items():
    total_words_in_ham = total_words_in_ham + value[1]
    total_words_in_spam = total_words_in_spam + value[2]
    # print(key , " : ", value)

ham_probability = ham_count / mail_count
spam_probability = spam_count / mail_count

with open("nbmodel.txt" , "w") as f:
    output["Vocabulary_Size"] = vocabulary_length
    output["Words_in_Ham"] = total_words_in_ham
    output["Words_in_Spam"] = total_words_in_spam
    output["Ham_Probability"] = ham_probability
    output["Spam_Probability"] = spam_probability
    output["Number_Of_Hams"] = ham_count
    output["Number_Of_Spams"] = spam_count
    output["Number_Of_Mails"] = mail_count
    # json.dump(output, f, sort_keys=True, indent=4, separators=(',', ': '))

# print("\nTotal number of mails = " + str(mail_count))
# print("\nTotal number of ham mails = " + str(ham_count))
# print("\nTotal number of spam mails = " + str(spam_count))
# print("\nProbability of ham mails = " + str(ham_probability))
# print("\nProbability of spam mails = " + str(spam_probability))
# print("\nSize of Vocabulary = " + str(vocabulary_length))
# print("\nTotal words in ham = " + str(total_words_in_ham))
# print("\nTotal words in spam = " + str(total_words_in_spam))

with open("nbmodel.txt" , "a") as f:
    # Computing conditional probabilities of each token with smoothing
    for key, value in vocabulary.items():
        op[key] = {}
        conditional_probabilities_for_word = {}
        conditional_probabilities_for_word["Ham_Appearance"] = value[1]
        conditional_probabilities_for_word["CP_With_Ham"] = (value[1] + 1) / (total_words_in_ham + vocabulary_length)
        conditional_probabilities_for_word["Spam_Appearance"] = value[2]
        conditional_probabilities_for_word["CP_With_Spam"] = (value[2] + 1) / (total_words_in_spam + vocabulary_length)
        op[key] = conditional_probabilities_for_word
        output["Tokens"] = op
    json.dump(output, f, sort_keys=True, indent=4, separators=(',', ': '))