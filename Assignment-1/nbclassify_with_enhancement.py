import os
import json
import math
import sys

with open("nbmodel.txt", "r") as f:
    nbmodel_data = json.loads(f.read())

directory_path = sys.argv[1]
# directory_path = "/home/devansh/Desktop/NLP/SpamOrHam/dev"

# ham_directory_path = os.path.join(directory_path, "ham")
# spam_directory_path = os.path.join(directory_path, "spam")

ham_probability = nbmodel_data["Ham_Probability"]
spam_probability = nbmodel_data["Spam_Probability"]

vocabulary = nbmodel_data["Tokens"]
result = {}



count = 0

with open("nboutput.txt", "w") as out:
    # Compiling data for ham
    #for filename in os.listdir(ham_directory_path):
    for root, dirs, files in os.walk(directory_path, topdown=False):
        for name in files:
            file_path = os.path.join(root,name)
            spam_cp_product = 0
            ham_cp_product = 0
            # file_path = ham_directory_path + "/" + filename
            with open(file_path, "r", encoding = "latin1") as f:
                for word in f.read().split():
                    token = word.lower()
                    if token in vocabulary:
                        # print(token)
                        count = count + 1
                        # print(str(vocabulary[token]["CP_With_Spam"]))
                        # spam_cp_product = spam_cp_product * vocabulary[token]["CP_With_Spam"]
                        spam_cp_product = spam_cp_product + math.log(vocabulary[token]["CP_With_Spam"])
                        # print(str(spam_cp_product))
                        # print(str(vocabulary[token]["CP_With_Ham"]))
                        # ham_cp_product = ham_cp_product * vocabulary[token]["CP_With_Ham"]
                        ham_cp_product = ham_cp_product + math.log(vocabulary[token]["CP_With_Ham"])
                        # print(str(ham_cp_product) + "\n")
                    else:
                        continue
                # print(str(count))
                # probability_of_mail_bein_spam = spam_probability * spam_cp_product
                probability_of_mail_bein_spam = math.log(spam_probability) + spam_cp_product
                # print(spam_probability)
                # print(probability_of_mail_bein_spam)
                # probability_of_mail_bein_ham = ham_probability * ham_cp_product
                probability_of_mail_bein_ham = math.log(ham_probability) + ham_cp_product
                # print(ham_probability)
                # print(probability_of_mail_bein_ham)

                if(probability_of_mail_bein_spam > probability_of_mail_bein_ham):
                    out.write("spam " + os.path.abspath(name) + '\n')

                else:
                    out.write("ham " + os.path.abspath(name) + '\n')

