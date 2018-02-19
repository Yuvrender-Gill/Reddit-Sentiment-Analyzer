import numpy as np
import sys
import argparse
import os
import json

# define file names
BGL_norm_path = "/u/cs401/Wordlists/BristolNorms+GilhoolyLogie.csv"
W_norm_path = "/u/cs401/Wordlists/Ratings_Warriner_et_al.csv"


def extract1( comment ):
    ''' This function extracts features from a single comment

    Parameters:
        comment : string, the body of a comment (after preprocessing)

    Returns:
        feats : numpy Array, a 173-length vector of floating point features (only the first 29 are expected to be filled, here)
    '''
    # Create a feature vector
    feats = np.zeros(174)
    # Token text list============================
    text_list = get_token_text(comment)
    tag_list = get_token_tag(comment)
    sentence_list = split_sentences(comment)
    # First 17 features==========================
    feats = np.array([first_person_pronouns(text_list), second_person_pronouns(text_list),
                      third_person_pronouns(text_list), coordinating_conjunctions(tag_list),
                      past_tense_verbs(tag_list), future_tense_verbs(text_list, tag_list),
                      commas(text_list), colons(text_list) + dashes(text_list) + parantheses(text_list) +
                      ellipses(text_list), common_nouns(tag_list), proper_nouns(tag_list),
                      adverbs(tag_list), wh_words(tag_list), slang_acronyms(text_list),
                      upper_case_words(text_list), sentence_length(sentence_list, text_list),
                      token_length(text_list), number_sentences(sentence_list)])
    print(feats)
    return feats


#========================HELPER FUNCTIONS================================================


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
    return sum(token_lengths) / float(len(token_lengths))


# Feature 17 
def number_sentences(sentences):
    """
    Returns the number of sentences in the comment.
    :param sentences:
    :return:
    """
    return len(sentences)


def main( args ):

    data = json.load(open(args.input))
    feats = np.zeros( (len(data), 173+1))
    for i in range(len(data)):
        line = json.loads(data[i])
        if ("body" in line):
            new = extract1(line["body"])
            for j in range(new.size):
                feats[i][j] = new[j]
                print(feats[i][j])
        if ("cat" in line):
            if (line["cat"] == "Right"):
                feats[i][173] = 2
            if (line["cat"] == "Left"):
                feats[i][173] = 0
            if (line["cat"] == "Alt"):
                feats[i][173] = 3
            if (line["cat"] == "Center"):
                feats[i][173] = 1

    print(feats)
    # TODO: your code here

    np.savez_compressed( args.output, feats)


if __name__ == "__main__": 

    parser = argparse.ArgumentParser(description='Process each .')
    parser.add_argument("-o", "--output", help="Directs the output to a filename of your choice", required=True)
    parser.add_argument("-i", "--input", help="The input JSON file, preprocessed as in Task 1", required=True)
    args = parser.parse_args()
                 

    main(args)

