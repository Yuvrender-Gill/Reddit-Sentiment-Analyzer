import numpy as np
import sys
import argparse
import os
import json
import csv
import warnings

# define file names ==================================================
BGL_norm_path = "BristolNorms+GilhoolyLogie.csv"
W_norm_path = "Ratings_Warriner_et_al.csv"
right_feats_path = "/u/cs401/A1/feats/Right_IDs.txt"
left_feats_path = "/u/cs401/A1/feats/Left_IDs.txt"
center_feats_path = "/u/cs401/A1/feats/Center_IDs.txt"
alt_feats_path = "/u/cs401/A1/feats/Alt_IDs.txt"
right_array_path = "/u/cs401/A1/feats/Right_feats.dat.npy"
left_array_path = "/u/cs401/A1/feats/Left_feats.dat.npy"
center_array_path = "/u/cs401/A1/feats/Center_feats.dat.npy"
alt_array_path = "/u/cs401/A1/feats/Alt_feats.dat.npy"

# ======================================================================
# Open and read csv files


def extract1(comment):
    ''' This function extracts features from a single comment

    Parameters:
        comment : string, the body of a comment (after preprocessing)

    Returns:
        feats : numpy Array, a 173-length vector of floating point features (only the first 29 are expected
        to be filled, here)
    '''
    # Create a feature vector
    feats = np.zeros(174)
    # Token text list============================
    text_list = get_token_text(comment)
    tag_list = get_token_tag(comment)
    sentence_list = split_sentences(comment)
    # Open CSV file

    BGL_norm_file = open(BGL_norm_path)
    BGL_norm_reader = csv.reader(BGL_norm_file, delimiter=',')

    W_norm_file = open(W_norm_path)
    W_norm_reader = csv.reader(W_norm_file, delimiter=',')
    # 18-23 features==========================
    features_list1 = avg_BLG(text_list, BGL_norm_reader)
    features_list2 = feature_W(text_list, W_norm_reader)
    # Call the helpers to get features 1-29 in an array
    feats = np.array([first_person_pronouns(text_list), second_person_pronouns(text_list),
                      third_person_pronouns(text_list), coordinating_conjunctions(tag_list),
                      past_tense_verbs(tag_list), future_tense_verbs(text_list, tag_list),
                      commas(text_list), colons(text_list) + dashes(text_list) + parantheses(text_list) +
                      ellipses(text_list), common_nouns(tag_list), proper_nouns(tag_list),
                      adverbs(tag_list), wh_words(tag_list), slang_acronyms(text_list),
                      upper_case_words(text_list), sentence_length(sentence_list, text_list),
                      token_length(text_list), number_sentences(sentence_list),
                      features_list1[0], features_list1[1], features_list1[2], features_list1[3],
                      features_list1[4], features_list1[5], features_list2[0], features_list2[1],
                      features_list2[2], features_list2[3], features_list2[4], features_list2[5]])

    BGL_norm_file.close()
    W_norm_file.close()

    return feats


# ========================HELPER FUNCTIONS================================================


def get_token_text(comment):
    """
     Returns a list of the strings with each token split from the comment.
     The return list includes only the token text.
    :param comment:
    :return:
    """

    word_list = comment.split()
    return [x.split('/')[0] for x in word_list]


def get_token_tag(comment):
    """
    Returns a list of the strings with each token split from the comment.
    The return list includes only the token tag.
    :param comment:
    :return:
    """

    word_list = comment.split()
    return [x.split('/')[1] for x in word_list]


def split_sentences(comment):
    """
    Cleans each token with extending white space. Then finds the sentence in the token
    which is assumed to be separated by newline character '\n'
    :param comment
    :return:
    """
    return comment.split('\\n')


# Feature 1
def first_person_pronouns(token_list):
    """
    Returns the number of first person words used in the given comment.
    :param token_list
    :return:
    """
    first_person_words = ['i', 'me', 'my', 'mine', 'we', 'us', 'our', 'ours']
    count = 0
    for item in token_list:
        # Check all the cases 1. lower 2. title 3.Upper
        if ((item.title() in first_person_words) or
                (item.lower() in first_person_words) or
                (item in first_person_words) or
                (item.upper() in first_person_words)):
            count += 1
    return count


# Feature 2
def second_person_pronouns(token_list):
    """
    Returns the number of second person words used in the given comment.
    :param token_list
    :return:
    """

    second_person_words = ['you', 'your', 'yours', 'u', 'ur', 'urs']

    count = 0
    for item in token_list:
        # Check all the cases 1. lower 2. title 3.Upper
        if ((item.title() in second_person_words) or
                (item.lower() in second_person_words) or
                (item in second_person_words) or
                (item.upper() in second_person_words)):
            count += 1
    return count


# Feature 3
def third_person_pronouns(token_list):
    """
    Returns the number of third person words used in the given comment.
    :param token_list
    :return:
    """

    third_person_words = ['he', 'him', 'his', 'she', 'her', 'hers', 'it', 'its', 'they', 'them', 'their', 'theirs']
    count = 0
    for item in token_list:
        # Check all the cases 1. lower 2. title 3.Upper
        if ((item.title() in third_person_words) or
                (item.lower() in third_person_words) or
                (item in third_person_words) or
                (item.upper() in third_person_words)):
            count += 1
    return count


# Feature 4
def coordinating_conjunctions(token_tag_list):
    """
    Returns the number of coordinating conjunctions in the given comment.
    The function counts coordinating conjunctions by counting the token tags.
    :param token_tag_list:
    :return:
    """
    candidate_words = ['CC']
    return [x in candidate_words for x in token_tag_list].count(True)


# Feature 5
def past_tense_verbs(token_tag_list):
    """
    Returns the number of past tense verbs in the given comment.
    The function counts past tense verbs by counting the token tags.
    :param token_tag_list:
    :return:
    """
    candidate_words = ['VBD']
    return [x in candidate_words for x in token_tag_list].count(True)


# Feature 6
def future_tense_verbs(token_list, token_tag_list):
    """
    Returns the number of future tense verbs in the given comment.
    The function counts future tense verbs by counting the token tags.
    :param token_list:
    :param token_tag_list:
    :return:
    """
    future_tense_words = ["'ll", 'will', 'gonna']
    # get the words in token list
    count = [x.lower() in future_tense_words for x in token_list].count(True)

    # We also want to count sequences of going+to+VB
    count += [
        token_list[i].lower() == 'going' and token_list[i + 1][0].lower() == 'to' and token_tag_list[i + 2][1] == 'VB'
        for i in range(len(token_list) - 2)].count(True)
    return count


# Feature 7
def commas(token_list):
    """
    Returns the number of '.' tokens in the token list.
    :param token_list:
    :return:
    """
    candidate_words = [',']
    return [x in candidate_words for x in token_list].count(True)


# Feature 8
def colons(token_list):
    """
    Returns the number of ':' and ';' tokens in the token list.
    :param token_list:
    :return:
    """
    candidate_words = [':', ';']
    return [x in candidate_words for x in token_list].count(True)


# Feature 8
def dashes(token_list):
    """
    Returns the number of '-' tokens in the token list.
    :param token_list:
    :return:
    """
    candidate_words = ['-']
    return [x in candidate_words for x in token_list].count(True)


# Feature 8
def parantheses(token_list):
    """
    Returns the number of '(' and ')' tokens in the token list.
    :param token_list:
    :return:
    """
    candidate_words = ['(', ')']
    return [x in candidate_words for x in token_list].count(True)


# Feature 8
def ellipses(token_list):
    """
    Returns the number of '...' tokens in the token list.
    :param token_list:
    :return:
    """
    candidate_words = ['...']
    return [x in candidate_words for x in token_list].count(True)


# Feature 9
def common_nouns(token_tag_list):
    """
    Returns the count of common nouns.
    :param token_tag_list:
    :return:
    """
    tag_list = ['NN', 'NNS']
    return [x in tag_list for x in token_tag_list].count(True)


# Feature 10
def proper_nouns(token_tag_list):
    """
    Returns the count of proper nouns.
    :param token_tag_list:
    :return:
    """
    tag_list = ['NNP', 'NNPS']
    return [x in tag_list for x in token_tag_list].count(True)


# Feature 11
def adverbs(token_tag_list):
    """
    Returns the count of adverbs.
    :param token_tag_list:
    :return:
    """

    tag_list = ['RB', 'RBR', 'RBS']
    return [x in tag_list for x in token_tag_list].count(True)


# Feature 12
def wh_words(token_tag_list):
    """
    Returns the count of wh words.
    :param token_tag_list:
    :return:
    """
    tag_list = ['WDT', 'WP', 'WP$', 'WRB']
    return [x in tag_list for x in token_tag_list].count(True)


# Feature 13
def slang_acronyms(token_list):
    """
    Returns the number of slang acronyms in the given token text list.
    :param token_list:
    :return:
    """
    slang_list = ['smh', 'fwb', 'lmfao', 'lmao', 'lms', 'tbh', 'rofl', 'wtf',
                  'bff', 'wyd', 'lylc', 'brb', 'atm', 'imao', 'sml', 'btw',
                  'bw', 'imho', 'fyi', 'ppl', 'sob', 'ttyl', 'imo', 'ltr',
                  'thx', 'kk', 'omg', 'ttys', 'afn', 'bbs', 'cya', 'ez',
                  'f2f', 'gtr', 'ic', 'jk', 'k', 'ly', 'ya', 'nm', 'np',
                  'plz', 'ru', 'so', 'tc', 'tmi', 'ym', 'ur', 'u', 'sol']
    return [x.lower() in slang_list for x in token_list].count(True)


# Feature 14
def upper_case_words(token_list):
    """
    Returns the number of upper case words in the token list.
    :param token_list:
    :return:
    """
    return [x.isupper() and len(x[0]) > 1 for x in token_list].count(True)


# Feature 15
def sentence_length(sentences, token_list):
    """
    Returns the average number of tokens in a given comment. That is
    number of tokens / number of sentences.
    :param sentences:
    :param token_list:
    :return:
    """
    if len(sentences) == 0:
        return 0
    return len(token_list) / float(len(sentences))


# Feature 16
def token_length(token_list):
    """
    Returns the average length of all the tokens in a comment, excluding the punctuation list.
    :param token_list:
    :return:
    """
    punctuation_list = ['#', '$', '.', ',', ':', '(', ')', '"', 'POS']
    token_lengths = [len(x) for x in token_list if x not in punctuation_list]
    if len(token_lengths) == 0:
        return 0
    return sum(token_lengths) / float(len(token_lengths))


# Feature 17 
def number_sentences(sentences):
    """
    Returns the number of sentences in the comment.
    :param sentences:
    :return:
    """
    return len(sentences)


# Feature 18 - 23
def avg_BLG(token_list, csv_reader):
    """
    Returns the average of the AOA norm for the words that appear in the token list.

    :param token_list:
    :param csv_reader:
    :return:
    """
    count = 0
    avg_AOA = []
    avg_IMG = []
    avg_FAM = []

    for row in csv_reader:
        if (count > 0):
            if row[1] in token_list:
                if (row[3] == ""):
                    break
                avg_AOA.append(float(row[3]))
                avg_IMG.append(float(row[4]))
                avg_FAM.append(float(row[5]))
        count += 1
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=RuntimeWarning)
        features_list = [np.mean(avg_AOA), np.mean(avg_IMG), np.mean(avg_FAM),
                         np.std(avg_AOA), np.std(avg_IMG), np.std(avg_FAM)]
    return features_list


# Feature 24 - 29
def feature_W(token_tag_list, csv_reader):
    """
    Returns the average and standard deviation of the AOA norm for the words that
    appear in the token list.

    :param token_list:
    :param csv_reader:
    :return:
    """

    count = 0
    avg_VMean = []
    avg_AMean = []
    avg_DMean = []

    for row in csv_reader:
        if (count > 0):
            if row[1] in token_tag_list:
                if (row[3] == ""):
                    break
                avg_VMean.append(float(row[2]))
                avg_AMean.append(float(row[5]))
                avg_DMean.append(float(row[8]))
        count += 1
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=RuntimeWarning)
        features_list = [np.mean(avg_VMean), np.mean(avg_AMean), np.mean(avg_DMean),
                         np.std(avg_VMean), np.std(avg_AMean), np.std(avg_DMean)]
    return features_list


# Feature 30 -173
def LISP_features(npy_path, txt_path):
    """

    :param npy_path:
    :param txt_path:
    :return:
    """

    array = np.load(npy_path)
    file = open(txt_path, "r")




def main(args):
    """
    Main function which calls all the functions in the library and extracts the
    features from the input json file and stores them to a numpy array and then
    compress the numpy array to a npz file for the program output.

    :param args:
    :return:

    """
    # Open and store id files
    right_ids = open(right_feats_path).readlines()
    left_ids = open(left_feats_path).readlines()
    center_ids = open(center_feats_path).readlines()
    alt_ids = open(alt_feats_path).readlines()
    # open feat arrays
    right_array = np.load(right_array_path)
    left_array = np.load(left_array_path)
    center_array = np.load(center_array_path)
    alt_array = np.load(alt_array_path)
    check = 0
    data = json.load(open(args.input))
    feats = np.zeros((len(data), 173 + 1))
    # Features 1-29
    for i in range(len(data)):
        line = json.loads(data[i])
        if "id" in line:
            if "cat" in line:
                if line["cat"] == "Right":
                    id_index = right_ids.index(line["id"]+"\n")
                    features_array = right_array[id_index]
                    for j in range(features_array.size):
                        feats[i][j + 29] = features_array[j]
                if line["cat"] == "Left":
                    id_index = left_ids.index(line["id"] + "\n")
                    features_array = left_array[id_index]
                    for j in range(features_array.size):
                        feats[i][j + 29] = features_array[j]
                if line["cat"] == "Alt":
                    id_index = alt_ids.index(line["id"] + "\n")
                    features_array = alt_array[id_index]
                    for j in range(features_array.size):
                        feats[i][j + 29] = features_array[j]
                if line["cat"] == "Center":
                    id_index = center_ids.index(line["id"] + "\n")
                    features_array = center_array[id_index]
                    for j in range(features_array.size):
                        feats[i][j + 29] = features_array[j]
        if "body" in line:
            new = extract1(line["body"])
            for j in range(new.size):
                feats[i][j] = new[j]
        if "cat" in line:
            if line["cat"] == "Right":
                feats[i][173] = 2
            if line["cat"] == "Left":
                feats[i][173] = 0
            if line["cat"] == "Alt":
                feats[i][173] = 3
            if line["cat"] == "Center":
                feats[i][173] = 1

    np.savez_compressed(args.output, F=feats)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process each .')
    parser.add_argument("-o", "--output", help="Directs the output to a filename of your choice", required=True)
    parser.add_argument("-i", "--input", help="The input JSON file, preprocessed as in Task 1", required=True)
    args = parser.parse_args()

    main(args)
