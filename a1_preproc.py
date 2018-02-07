 
import sys
import argparse
import os
import json
import re
from os.path import basename

import spacy
#import csv
#import itertools

from html.parser import HTMLParser
import html 
import string


#===========================================================
'''GLOBAL VARIABLES'''#=====================================
indir = '/u/cs401/A1/data/';

nlp = spacy.load('en', disable=['parser', 'ner'])

stop_words_file = open('/u/cs401/Wordlists/StopWords')
stop_words_list = stop_words_file.readlines()

#abbrivaition_file = open('u/cs401/Wordlists/abbrev.english', 'rb')
#abber_list = abbriviation_file.readlines()
#=================================================================
#=================================================================

def preproc1( comment , steps=range(1,11)):
    ''' This function pre-processes a single comment

    Parameters:                                                                      
        comment : string, the body of a comment
        steps   : list of ints, each entry in this list corresponds to a preprocessing step  

    Returns:
        modComm : string, the modified comment 
    '''
     
    # The modified comment after removing the noise from the comment. 
    # Noise is specifically mentioned in the below mentioned steps. 
    modComm = ''
    modComm = remove_json_special(comment)
    #modComm = convert_HTML_char(modComm)
    modComm = remove_urls(modComm)
    modComm = pun_tokenizer(modComm)
    modComm = split_clitics(modComm)
    modComm = POS_tagging(modComm)
    modComm = remove_stop_words(modComm)
    modComm = lemmatize(modComm)
    modComm = lower(modComm)
    # if 2 in steps:
       # print('TODO')
   # if 3 in steps:
       # print('TODO')
   # if 4 in steps:
       # print('TODO')
   # if 5 in steps:
       # print('TODO')
   # if 6 in steps:
      #  print('TODO')
   # if 7 in steps:
     #   print('TODO')
   # if 8 in steps:
    #    print('TODO')
   # if 9 in steps:
   #     print('TODO')
   # if 10 in steps:
  #      print('TODO')
    
        
    return modComm 


## Helper Functions for specific tasks

#1 To remove the newline characters from the comment.

def remove_json_special(comment):
    ''' Returns a string with all newline characters removed from it.
    
    @param String comment: a String to remove newline character from.
    @rtype: String
    >>> comment = "\nHel\nlo how\n \n are you?\n"
    >>> remove_newline(comment)
    >>> 'Hello how are you?'
    
    '''
    
    #Remove the newline character, carnage return and tab character
    #remove the corner cases specific to the data
    modified_comment = comment.replace("\n", "")
    modified_comment = modified_comment.replace("\\n", "")
    modified_comment = modified_comment.replace("\\b", "")
    modified_comment = modified_comment.replace("\\t", "")
    modified_comment = modified_comment.replace("\\r", "")
        
    return modified_comment

#2 Convert the HTML Character to their ascii values. 

def convert_HTML_char(comment):
    ''' Returns a string with all HTML characters replaced with their corresponding 
    ascii values.
    
    @param String comment: a String to replace HTML characters from
    @rtype: String
    >>> comment = "\nHel\nlo how\n \n are you?\n"
    >>> convert_HTML_char(comment)
    >>> 'Hello how are you?'
    
    '''
    # Removes all the HTML tags from the comment.
    modified_comment = re.sub('<[^>]+>', '', comment)
    #Create a parser object
    
    #Get all the printable strings from the comment
    
    modified_comment = html.unescape(modified_comment).encode('ascii', 'ignore')
    
    return modified_comment

#3 Remove the urls from the data 

def remove_urls(comment):
    '''
    Removes any urls that appear in a comment. URLS typpically start with 
    tokens 'http' and 'www'. 
    @param String comment: a String to replace URLS from 
    @rtype: String
  
    
    '''
    modified_comment = re.sub(r"http\S+", "", str(comment))
    #one special case
    modified_comment = re.sub(r"Http\S+", "", str(modified_comment))
    modified_comment = re.sub(r"www\S+", "", str(modified_comment))
    # One special case
    modified_comment = re.sub(r"Www\S+", "", str(modified_comment))
   
    return modified_comment

#4 Tokenize punctuation

def pun_tokenizer(comment):
    '''
    Returns a string with all its punctuation tokenized.
    @param String comment: a String to tokenize punctuation from
    @rtype: String
    '''
    
    abbr_list = ['Capt', 'Col.', 'Dr.','Drs.', 'Fig.', 'Figs.', 'Gen.',
                 'Gov.', 'HON.', 'Mr.', 'MRS.', 'Miss.', 'Messrs.', 'Miss.',
                 'MR.', 'Mrs.', 'Ref.', 'Rep.', 'Reps.', 'Sen.', 'fig.',
                 'figs.', 'vs.', 'Lt.', 'e.g.', 'i.e.'] 
    lst_str = comment.split()
    modified_comment = ""
    
    for item in lst_str:
        if (not (item in abbr_list)):
            modified_comment += ' '.join([re.sub(r"((["+ '!"#$%&\()*+,-./:;<=>?@[\\]^_`{|}~' + "])\\2*)", r" \1  ", item)]) + ' '
        else:
            modified_comment += ' ' + item + ' ' 
    modified_comment = ' '.join(modified_comment.split('  '))
    modified_comment = re.sub(r"(') ([A-Za-z] )", r"\1\2", modified_comment).strip()
    return modified_comment

#5 Spliting Clitics using white space

def split_clitics(comment):
    '''
    Returns a string with clitics split from the comment.
    @param String comment: a String to split clitics from
    @rtype: String
    '''
    modified_comment = ' '.join([re.sub(r"((["+ "'" + "]))", r" \1", comment)])
    modified_comment = ' '.join(modified_comment.split('  '))
    modified_comment = re.sub(r"(') ([A-Za-z] )", r"\1\2", modified_comment).strip()
    return modified_comment

#6 Part of speech tagging of tokens and lemmatization. 

def POS_tagging(comment):
    '''
    Returns with all the tokens (words) in it tagged with their part of speech.
    The function uses spacy library's part of speech tagger. 
    @param String comment: a String to tag the tokens from. 
    @rtype: String
    '''
    utt = nlp(comment)
    return ' '.join([(token.text+'/'+token.tag_) for token in utt])

#7 Remove the stop words.

def remove_stop_words(comment):
    '''
    Returns a sub-string of comment with all the stop words removed from it and
    white space removed from the ends if any due to removal of the stop words.
    @param String comment: a String to remove the stop words from. 
    @rtype: String
    '''
    word_list = comment.split()
    
    for item in word_list:
        #Check all the cases 1. lower 2. title 3.Upper 
        if (((item.split('/')[0].title() + '\n')  in stop_words_list) or 
            ((item.split('/')[0].lower() + '\n') in stop_words_list) or 
            ((item.split('/')[0] + '\n') in stop_words_list) or
            ((item.split('/')[0].upper() + '\n') in stop_words_list)):
            word_list[word_list.index(item)] = ""
    return ' '.join(word_list).strip()

#8 Lemmatization of the tokens

def lemmatize(comment):
    
    '''
    Returns a a string with all the tokens in the comment lemmatized.
    @param String comment: a String to lemmatize the tokens from 
    @rtype: String
    '''
    word_list = comment.split()
    
    for item in word_list:
        new_list = item.split('/')
        # Convert the token from the token with tag to spacy readable object
        utt = nlp(item.split('/')[0])
        # utt is a list with one object and get the lemmatized token from it
        lemmatized_token = ' '.join([(token.lemma_) for token in utt])
        # replace the token text with token lemma
        new_list[0] = lemmatized_token
        # concatinate the modifieed string again
        word_list[word_list.index(item)] = ''.join(new_list)
        #concatinate the body of post and return it 
    return ' '.join(word_list).strip()

    
#10 lower case

def lower(comment):
    word_list = comment.split()
    for item in word_list:
        new_list = item.split('/')
        lower = new_list[0].lower()
        new_list[0] = lower
        word_list[word_list.index(item)] = ''.join(new_list)
    return ' '.join(word_list).strip()    
    
def main( args ):
    count = 0;
    allOutput = []
    for subdir, dirs, files in os.walk(indir):
        for file in files:
            fullFile = os.path.join(subdir, file)
            print("Processing " + fullFile)
    
            
            data = json.load(open(fullFile))
            
            for i in range(10000,10200):
                line = json.loads(data[i])
                          
                line2 = {}
                
                if ('id' in line):
                    line2['id']= line['id']
                else:
                    line2['id'] = 'null'
                if ("body" in line):
                    line2["body"] = preproc1(line["body"])
                else:
                    line2["body"] = "null"
                if ('ups' in line):
                    line2['ups'] =  line['ups']
                else:
                    line2['ups'] = 'null'
                if ('downs' in line):
                    line2['downs'] = line['downs']
                else:
                    line2['downs'] = 'null'
                if ('score' in line):
                    line2['score'] =line['score']
                else:
                    line2['score'] = 'null'
                if ('controversiality' in line):
                    line2['controversiality'] =line['controversiality']
                else:
                    line2['controversiality'] = 'null'
                if ('author' in line):
                    line2['author'] =line['author']
                else:
                    line2['author'] = 'null'
                if ('subreddit' in line):
                    line2['subreddit'] = line['subreddit']
                else:
                    if ('subreddit_id' in line):
                        line2['subreddit'] = line['subreddit_id']
                    else:
                        line2['subreddit'] = 'null'
                line2['cat'] = basename(fullFile)
                json_data = json.dumps(line2)  
                allOutput.append(json_data)
                count += 1          
            

            # TODO: select appropriate args.max lines
            # TODO: read those lines with something like `j = json.loads(line)`
            # TODO: choose to retain fields from those lines that are relevant to you
            # TODO: add a field to each selected line called 'cat' with the value of 'file' (e.g., 'Alt', 'Right', ...) 
            # TODO: process the body field (j['body']) with preproc1(...) using default for `steps` argument
            # TODO: replace the 'body' field with the processed text
            # TODO: append the result to 'allOutput'
    print(count)       
    fout = open(args.output, 'w')
    fout.write(json.dumps(allOutput))
    fout.close()
    
    
    
    
    

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Process each .')
    parser.add_argument('ID', metavar='N', type=int, nargs=1,
                        help='your student ID')
    parser.add_argument("-o", "--output", help="Directs the output to a filename of your choice", required=True)
    parser.add_argument("--max", help="The maximum number of comments to read from each file", default=10000)
    args = parser.parse_args()

    if (args.max > 200272):
        print("Error: If you want to read more than 200,272 comments per file, you have to read them all.")
        sys.exit(1)
        
    main(args)
