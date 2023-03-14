# -*- coding: utf-8 -*-
"""GPT_2_token_level_final.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1DjKawqWr6O6UlWgDCVHoFFU8Uzj-2_h0
"""

#import pacakges 
!pip install transformers
from transformers import GPT2Tokenizer, GPT2LMHeadModel
import os
import re
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
import numpy as np
import tensorflow as tf
import torch
from torch import nn
from scipy.stats import gmean
from sklearn.metrics import f1_score
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_curve, auc
from matplotlib import pyplot

#load coll-14 dataset and preprocessing
with open('conll14st-preprocessed_copy.m2', encoding='utf8') as f:
    eval_data_letter=[]
    eval_data_token=[]  
    label=[]
    pre_line='B'
    sentence_character='S '
    anomaly_character='A ' 
    running=0
    label_array=[]
    for curr_line in f:
        m = re.search(r"http",curr_line)
        n = re.search(r"www",curr_line)
        r = re.search(r"References\n",curr_line)
        if m != None: 
            running=1
            pre_line=curr_line
        elif curr_line.isupper():
            pre_line=curr_line 
        elif n != None: 
            running=1
            pre_line=curr_line  
        elif '( ' in curr_line: 
            running=1
            pre_line=curr_line   
        elif '[ ' in curr_line: 
            running=1
            pre_line=curr_line      
        elif len(curr_line)<30:
            pre_line=curr_line  
        elif curr_line[0]==sentence_character[0]:
            label.append(label_array) 
            label_array=[]
            running=0
            curr_line=curr_line.replace('\n', "")
            curr_line=curr_line.replace(sentence_character, "")
            eval_data_letter.append(curr_line)
            curr_line=tokenizer.encode(curr_line)
            eval_data_token.append(curr_line)
            label_array=[0]*(len(curr_line))
            pre_line=curr_line
        elif curr_line[0]==anomaly_character[0]: 
            if running==0:
              numbers=curr_line[2:10]
              first_number=numbers[:numbers.index(" ")]
              second_number=numbers[numbers.index(" "):numbers.index("|")]
              second_number=second_number[1:3]
              if int(first_number) == int(second_number):
                label_array[int(first_number)-1]=1
              else:  
                label_array[int(first_number):int(second_number)]=[1]*(int(second_number)-int(first_number))               
              pre_line=curr_line
            else:
              continue  
        elif r != None: 
            running=1    
        elif running==1:
            if len(curr_line)>30:
                running=0
                curr_line=curr_line.replace('\n', "")
                curr_line=curr_line.replace(sentence_character, "")
                eval_data_letter.append(curr_line)
                curr_line=tokenizer.encode(curr_line)
                print(curr_line)
                eval_data_token.append(curr_line)
                label_array=[0]*len(curr_line)
                label.append(label_array)
                label_array=[]
                pre_line=curr_line           
            else:
                continue                   
        else : 
            pre_line=curr_line    
del(label[0])       
del(eval_data_token[-1])  
del(eval_data_letter[-1])  
#eval_data, label = shuffle(eval_data, label)
eval_data_short=eval_data_letter[0:10000]
label_short=label[0:10000]

#load FCE-test dataset and preprocessing
with open('fce.test.gold.bea19.m2', encoding='utf8') as f:
    fce_letter=[]
    fce_token=[]  
    fce_label=[]
    pre_line='B'
    sentence_character='S '
    anomaly_character='A ' 
    running=0
    label_array=[]
    #regex=r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    for curr_line in f:
        m = re.search(r"http",curr_line)
        n = re.search(r"www",curr_line)
        r = re.search(r"References\n",curr_line)
        if m != None: 
            running=1
            pre_line=curr_line
        elif n != None: 
            running=1
            pre_line=curr_line  
        elif '( ' in curr_line: 
            running=1
            pre_line=curr_line   
        elif '[ ' in curr_line: 
            running=1
            pre_line=curr_line      
        elif len(curr_line)<30:
            pre_line=curr_line  
        elif curr_line[0]==sentence_character[0]:
            fce_label.append(label_array) 
            label_array=[]
            running=0
            curr_line=curr_line.replace('\n', "")
            curr_line=curr_line.replace(sentence_character, "")
            fce_letter.append(curr_line)
            curr_line=tokenizer.encode(curr_line)
            fce_token.append(curr_line)
            label_array=[0]*(len(curr_line))
            pre_line=curr_line
        elif curr_line[0]==anomaly_character[0]:        
            if running==0:
              numbers=curr_line[2:10]
              first_number=numbers[:numbers.index(" ")]
              if int(first_number)==-1:
                  pre_line=curr_line
              else:    
                  second_number=numbers[numbers.index(" "):numbers.index("|")]
                  second_number=second_number[1:3]
                  if int(first_number) == int(second_number):
                      label_array[int(first_number)-1]=1
                  else:  
                      label_array[int(first_number):int(second_number)]=[1]*(int(second_number)-int(first_number))               
                  pre_line=curr_line
            else:
                continue  
        elif r != None: 
            running=1    
        elif running==1:
            if len(curr_line)>30:
                running=0
                curr_line=curr_line.replace('\n', "")
                curr_line=curr_line.replace(sentence_character, "")
                fce_letter.append(curr_line)
                curr_line=tokenizer.encode(curr_line)
                print(curr_line)
                fce_token.append(curr_line)
                label_array=[0]*len(curr_line)
                label.append(label_array)
                label_array=[]
                pre_line=curr_line           
            else:
                continue                   
        else : 
            pre_line=curr_line 
        #print(line.strip())     
del(fce_label[0])       
del(fce_token[-1])  
del(fce_letter[-1])

#load bea-19 dev set and preprocessing
with open('ABCN.dev.gold.bea19.m2', encoding='utf8') as f:
    bea19_letter=[]
    bea19_token=[]  
    bea19_label=[]
    pre_line='B'
    sentence_character='S '
    anomaly_character='A ' 
    running=0
    label_array=[]
    #regex=r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    for curr_line in f:
        m = re.search(r"http",curr_line)
        n = re.search(r"www",curr_line)
        r = re.search(r"References\n",curr_line)
        if m != None: 
            running=1
        elif n != None: 
            running=1
            pre_line=curr_line  
        elif '( ' in curr_line: 
            running=1
            pre_line=curr_line   
        elif '[ ' in curr_line: 
            running=1
            pre_line=curr_line      
        elif len(curr_line)<30:
            pre_line=curr_line  
        elif curr_line[0]==sentence_character[0]:
            bea19_label.append(label_array) 
            label_array=[]
            running=0
            curr_line=curr_line.replace('\n', "")
            curr_line=curr_line.replace(sentence_character, "")
            bea19_letter.append(curr_line)
            curr_line=tokenizer.encode(curr_line)
            bea19_token.append(curr_line)
            label_array=[0]*(len(curr_line))
            pre_line=curr_line
        elif curr_line[0]==anomaly_character[0]:        
            if running==0:
              numbers=curr_line[2:10]
              first_number=numbers[:numbers.index(" ")]
              if int(first_number)==-1:
                  pre_line=curr_line
              else:    
                  second_number=numbers[numbers.index(" "):numbers.index("|")]
                  second_number=second_number[1:3]
                  if int(first_number) == int(second_number):
                      label_array[int(first_number)-1]=1
                  else:  
                      label_array[int(first_number):int(second_number)]=[1]*(int(second_number)-int(first_number))               
                  pre_line=curr_line
            else:
                continue  
        elif r != None: 
            running=1    
        elif running==1:
            if len(curr_line)>30:
                running=0
                curr_line=curr_line.replace('\n', "")
                curr_line=curr_line.replace(sentence_character, "")
                bea19_letter.append(curr_line)
                curr_line=tokenizer.encode(curr_line)
                print(curr_line)
                bea19_token.append(curr_line)
                label_array=[0]*len(curr_line)
                label.append(label_array)
                label_array=[]
                pre_line=curr_line           
            else:
                continue                   
        else : 
            pre_line=curr_line     
del(bea19_label[0])       
del(bea19_token[-1])  
del(bea19_letter[-1])

# remove escape sequence from the data
def data_cleaner (eval_data):
    clean_data=[]
    for line in eval_data:
        line=line.replace('\n', "")      
        clean_data.append(line)
    return clean_data     
      
# Compute the optimal threshold using Yoden's index
def get_threshold (y_true, y_pred):
    from sklearn.metrics import roc_curve, auc
    from matplotlib import pyplot
    y_pred = list(np.concatenate(y_pred).flat)
    y_true = list(np.concatenate(y_true). flat)
    fpr, tpr, thresholds =roc_curve(y_true, y_pred)
    gmeans = np.sqrt(tpr * (1-fpr))
    ix = np.argmax(gmeans)
    print('Best Threshold=', thresholds[ix])
    pyplot.plot(fpr, tpr, marker='.')
    # axis labels
    pyplot.xlabel('False Positive Rate')
    pyplot.ylabel('True Positive Rate')
    # show the legend
    pyplot.legend()
    # show the plot
    pyplot.show()
    return thresholds[ix+1]

# function for counting occurrence in frequency method
def count_occurance (data):
    newlist = [item for items in data for item in items]
    return newlist

# baseline method (3.1)
def detect_anamoly_baseline_token(dataset, best_probability): 
    result=[] 
    word_probability=[] 
    #import GPT-2
    model = GPT2LMHeadModel.from_pretrained('gpt2')
    #import tokenizer
    tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
    data_converted=[]    
    sentence_probability=[]
    # import softmax layer
    m = nn.Softmax(dim=1)
    # iterate through all the sentences in the evaluation set 
    for index, eval_sentence in enumerate(dataset): 
        # tokenize words in sentences to evaluate
        inputs = tokenizer(eval_sentence, return_tensors="pt")
        # get next-word probabilities of words in a evaluation sentence
        tokens_tensor=tokenizer.encode(eval_sentence, add_special_tokens=False, max_length=1020, truncation=True)
        outputs = model(**inputs, labels=inputs["input_ids"]) 
        entire_sentence_word_p=[0]
        # generate the probabilties of words in evaluation sentence using the relevant next-word probabilities of GPT-2
        for i in range(1, len(tokens_tensor)): 
            # get the current token and the previous token to examine
            pre_word=tokens_tensor[i-1] 
            curr_word=tokens_tensor[i] 
            softmax_output = m(outputs[1][:,i-1,:])
            # get the next-word probability of the current word
            word_probability=softmax_output[0][curr_word]
            word_probability=word_probability.detach().numpy() 
            # if the next-word probabilty is lower than the given threshold, the word is seen as anomalous
            if word_probability < best_probability: 
                word_probability=1
            else: 
                word_probability=0   
            # append all the sentences in a corpus to a list     
            entire_sentence_word_p.append(word_probability) 
    return sentence_probability

# frequency-conditioned method (3.2)
def detect_anamoly_frequency_token_threshold(dataset, corpus, y_test, best_probability): 
    result=[] 
    word_probability=[] 
    #import GPT-2
    model = GPT2LMHeadModel.from_pretrained('gpt2')
    #import tokenizer
    tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
    data_converted=[]    
    sentence_probability=[]
    # import softmax layer
    m = nn.Softmax(dim=1)
    # import BROWN corpus
    brown_data_tokenized=tokenizer(corpus)
     # count the occurence of all the words in the corpus
    temp_count_list=count_occurance(brown_data_tokenized['input_ids'])
    unique, counts = np.unique(temp_count_list, return_counts=True)
    temp_count_list=np.array(temp_count_list)
    # iterate through all the sentences in the evaluation set 
    for index, eval_sentence in enumerate(dataset): 
        # tokenize words in sentences to evaluate
        inputs = tokenizer(eval_sentence, return_tensors="pt")
        # get next-word probabilities of words in a evaluation sentence
        tokens_tensor=tokenizer.encode(eval_sentence, add_special_tokens=False, max_length=1020, truncation=True)
        outputs = model(**inputs, labels=inputs["input_ids"])    
        entire_sentence_word_p=[0]
         # generate the probabilties of words in evaluation sentence using the relevant next-word probabilities of GPT-2
        for i in range(1, len(tokens_tensor)): 
            # get the current token and the previous token to examine
            pre_word=tokens_tensor[i-1] 
            curr_word=tokens_tensor[i] 
            softmax_output = m(outputs[1][:,i-1,:])
            # get the next-word probability of the current word
            word_probability=softmax_output[0][curr_word]
            word_probability=word_probability.detach().numpy()
            softmax_output=softmax_output.detach().numpy()
            # compute the wordcounts of the current word
            word_count = temp_count_list[temp_count_list==curr_word].shape[0]
            all_count=np.sum(counts)
            # get the frequency of the current word
            frequency_p=word_count/all_count 
            # avoid denominator to be zero and normalize the probability of the current word
            if frequency_p==0:
                word_p=word_probability
            else: 
                word_p=word_probability/frequency_p
            # append the normalized next-word probability to a sentence list     
            entire_sentence_word_p.append(word_p)
        # append all the sentences in a corpus to a list    
        sentence_probability.append(entire_sentence_word_p)
    # Use Yoden's Index to find an optimal threshold     
    threshold=get_threshold(y_test, sentence_probability)
    sentence_probability=list(np.concatenate(sentence_probability).flat)
    # use the optimal threshold to detect the anomalous word in a corpus
    result=[1 if word<threshold else 0 for word in sentence_probability]  
    return result

# frequency-conditioned method (3.2)
def detect_anamoly_frequency_token(dataset, corpus, best_probability): 
    result=[] 
    word_probability=[] 
    #import GPT-2
    model = GPT2LMHeadModel.from_pretrained('gpt2')
    #import tokenizer
    tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
    data_converted=[]    
    sentence_probability=[]
    # import softmax layer
    m = nn.Softmax(dim=1)
    # import BROWN corpus
    brown_data_tokenized=tokenizer(corpus)
    # count the occurence of all the words in the corpus
    temp_count_list=count_occurance(brown_data_tokenized['input_ids'])
    unique, counts = np.unique(temp_count_list, return_counts=True)
    temp_count_list=np.array(temp_count_list)
    # iterate through all the sentences in the evaluation set
    for index, eval_sentence in enumerate(dataset): 
        # tokenize words in sentences to evaluate
        inputs = tokenizer(eval_sentence, return_tensors="pt")
        tokens_tensor=tokenizer.encode(eval_sentence, add_special_tokens=False, max_length=1020, truncation=True)
        # get next-word probabilities of words in a evaluation sentence
        outputs = model(**inputs, labels=inputs["input_ids"])    
        entire_sentence_word_p=[0]
        # generate the probabilties of words in a evaluation sentence using the relevant next-word probabilities of GPT-2
        for i in range(1, len(tokens_tensor)):
            # get the current token and the previous token to examine 
            pre_word=tokens_tensor[i-1] 
            curr_word=tokens_tensor[i] 
            softmax_output = m(outputs[1][:,i-1,:])
            # get the next-word probability of the current word
            word_probability=softmax_output[0][curr_word]
            word_probability=word_probability.detach().numpy()
            softmax_output=softmax_output.detach().numpy()
            # compute the wordcounts of the current word
            word_count = temp_count_list[temp_count_list==curr_word].shape[0]
            all_count=np.sum(counts)
            # get the frequency of the current word
            frequency_p=word_count/all_count 
            # avoid denominator to be zero and normalize the probability of the current word
            if frequency_p==0:
                word_p=word_probability
            else: 
                word_p=word_probability/frequency_p
            # if the next-word probabilty is lower than the given threshold, the word is seen as anomalous    
            if word_p < best_probability:
                word_p=1
            else:
                word_p=0
            entire_sentence_word_p.append(word_p)
        # append all the sentences in a corpus to a list    
        sentence_probability.append(entire_sentence_word_p)
    return sentence_probability

# Word Embeddings Cosine Similarity method (3.3)
def detect_anamoly_cosine_token(dataset, best_probability, cosine_threshold, k): 
    result=[] 
    word_probability=[] 
    #import GPT-2
    model = GPT2LMHeadModel.from_pretrained('gpt2')
    #import tokenizer
    tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
    # import cosine similairty loss function
    cosine_loss=tf.keras.losses.CosineSimilarity(axis=-1, name='cosine_similarity')
    data_converted=[]    
    sentence_probability=[]
    # import word-embeddings in GPT-2
    weights = model.transformer.wte.weight
    weights = weights.detach().numpy()
    # import softmax layer
    m = nn.Softmax(dim=1)
    # iterate through all the sentences in the evaluation set 
    for index, eval_sentence in enumerate(dataset): 
        # tokenize words in sentences to evaluate
        inputs = tokenizer(eval_sentence, return_tensors="pt")
        # get next-word probabilities of words in a evaluation sentence
        tokens_tensor=tokenizer.encode(eval_sentence, add_special_tokens=False)
        outputs = model(**inputs, labels=inputs["input_ids"])
        entire_sentence_word_p=[0]
        # generate the probabilties of words in a evaluation sentence using the relevant next-word probabilities of GPT-2
        for i in range(1, len(tokens_tensor)):
            # get the current token and the previous token to examine 
            pre_word=tokens_tensor[i-1] 
            softmax_output = m(outputs[1][:,i-1,:])
            # get the next-word probability of the current word
            word_probability=softmax_output[0][curr_word]
            word_probability=word_probability.detach().numpy()
            softmax_output=softmax_output.detach().numpy()
            # if the next-word probability of the current word is lower than a threshold, compute k most probable words of the previous word 
            if word_probability < best_probability: 
                        append_number=1
                        idx = (outputs[1][:,i-1,:]).argsort()[0][k:]
                        # iterate through k most probable words
                        for best_word in idx:  
                             # compute the cosine similarity loss between the current word and k most probable words
                            loss=cosine_loss(weights[curr_word], weights[best_word]).numpy() 
                            # if the cosine similarity loss is lower than the threshold, current word and most probable word have similar meaning, and should not be a anomalous word 
                            if loss<cosine_threshold:
                                append_number=0
                                break
                            # otherwise keep iterating through next most probable word in k     
                            else:                            
                                continue
                        entire_sentence_word_p.append(append_number)   
            # if no next-word probabilty is found in GPT-2, the word is seen as anomalous                                   
            elif word_probability==None:
                entire_sentence_word_p.append(1)
            # if the next-word probability of the current word is higher than a threshold, append the original next-word probability    
            else:
                entire_sentence_word_p.append(0)
         # append all the sentences in a corpus to a list       
        sentence_probability.append(entire_sentence_word_p)
    return sentence_probability

# Position probability conditioned method (3.4)
def detect_anamoly_position_token(dataset, best_probability): 
    result=[] 
    word_probability=[] 
    #import GPT-2 
    model = GPT2LMHeadModel.from_pretrained('gpt2')
    #import tokenizer
    tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
    data_converted=[]    
    sentence_probability=[]
    # import softmax layer
    m = nn.Softmax(dim=1)
    # iterate through all the sentences in the evaluation set
    for eval_sentence in dataset: 
        # tokenize words in sentences to evaluate
        inputs = tokenizer(eval_sentence, return_tensors="pt")
        # get next-word probabilities of words in a evaluation sentence
        tokens_tensor=tokenizer.encode(eval_sentence, add_special_tokens=False, max_length=1020, truncation=True)
        outputs = model(**inputs, labels=inputs["input_ids"])    
        entire_sentence_word_p=[0]
        # generate the probabilties of words in a evaluation sentence using the relevant next-word probabilities of GPT-2
        for i in range(1, len(tokens_tensor)): 
            # get the current token and the previous token to examine
            pre_word=tokens_tensor[i-1] 
            curr_word=tokens_tensor[i] 
            # get the next-word probability of the current word
            softmax_output = m(outputs[1][:,i-1,:])
            word_probability=softmax_output[0][curr_word]
            word_probability=word_probability.detach().numpy()  
            # generate position probability of the current word 
            entire_position_probability=m(outputs[1][:, :,curr_word])
            position_probability=entire_position_probability[0][i-1]
            position_probability=position_probability.detach().numpy()
            word_position_probability=position_probability/1
            # take log to avoid an overflow of digits
            word_probability=np.log(word_probability)
            # if probabiltiy is not zero, substract position probability (condition probabilty on position probability)
            if word_position_probability != 0.0:
               # take log to avoid an overflow of digits
              word_position_probability=np.log(word_position_probability)
            word_probability_conditioned_position=word_probability-word_position_probability
            # if the next-word probability of the current word is higher than a threshold, the word is anomalous 
            if word_probability_conditioned_position > best_probability: 
                word_probability_conditioned_position=1
            else:
                word_probability_conditioned_position=0 
            # append the result of each word onto a list
            entire_sentence_word_p.append(word_probability_conditioned_position)
        # append all the sentences in a corpus to a list   
        sentence_probability.append(entire_sentence_word_p)          
    return sentence_probability

# Position probability conditioned method (3.4)
def detect_anamoly_position_token_threshold(dataset, best_probability, y_test): 
    result=[] 
    word_probability=[] 
    #import GPT-2
    model = GPT2LMHeadModel.from_pretrained('gpt2')
    #import tokenizer
    tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
    data_converted=[]    
    sentence_probability=[]
    # import softmax layer
    m = nn.Softmax(dim=1)
    # iterate through all the sentences in the evaluation set 
    for index, eval_sentence in enumerate(dataset): 
        # tokenize words in sentences to evaluate
        inputs = tokenizer(eval_sentence, return_tensors="pt")
        # get next-word probabilities of words in a evaluation sentence
        tokens_tensor=tokenizer.encode(eval_sentence, add_special_tokens=False, max_length=1020, truncation=True)
        outputs = model(**inputs, labels=inputs["input_ids"])    
        entire_sentence_word_p=[0]
        # generate the probabilties of words in a evaluation sentence using the relevant next-word probabilities of GPT-2
        for i in range(1, len(tokens_tensor)): 
            # get the current token and the previous token to examine
            pre_word=tokens_tensor[i-1] 
            curr_word=tokens_tensor[i] 
            softmax_output = m(outputs[1][:,i-1,:])
            # get the next-word probability of the current word
            word_probability=softmax_output[0][curr_word]
            word_probability=word_probability.detach().numpy()  
            # generate position probability of the current word
            entire_position_probability=m(outputs[1][:, :,curr_word])
            position_probability=entire_position_probability[0][i-1]
            position_probability=position_probability.detach().numpy()
            word_position_probability=position_probability/1
            # take log to avoid an overflow of digits
            word_probability=np.log(word_probability)
            # if probabiltiy is not zero, substract position probability (condition probabilty on position probability)
            if word_position_probability != 0.0:
              # take log to avoid an overflow of digits
              word_position_probability=np.log(word_position_probability)
            word_probability_conditioned_position=word_probability-word_position_probability
            # append word probabiltiy onto a list 
            entire_sentence_word_p.append(word_probability_conditioned_position)
        # append all the sentences in a corpus to a list     
        sentence_probability.append(entire_sentence_word_p) 
    # Use Yoden's Index to find an optimal threshold          
    threshold=get_threshold(y_test, sentence_probability)
    sentence_probability=list(np.concatenate(sentence_probability).flat)
    # use the optimal threshold to detect the anomalous word in a corpus
    result=[1 if word>threshold else 0 for word in sentence_probability]         
    return result