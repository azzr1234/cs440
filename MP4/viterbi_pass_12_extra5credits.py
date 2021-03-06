"""
This is the main entry point for MP4. You should only modify code
within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""
from collections import defaultdict
from collections import Counter
from collections import deque
import math
import numpy as np

#python mp4.py --train data/brown-training.txt --test data/brown-dev.txt
def statistics_on_word(each_word,dict1):#used to set up a Counter and return the word with the most frequent tag of the word
    #17:16 version overtime
    Tag_Counter=Counter(dict1[each_word])
    Tag=Tag_Counter.most_common(1)[0][0]
    return Tag
    
def baseline(train, test):
    '''
    TODO: implement the baseline algorithm. This function has time out limitation of 1 minute.
    input:  training data (list of sentences, with tags on the words)
            E.g. [[(word1, tag1), (word2, tag2)...], [(word1, tag1), (word2, tag2)...]...]
            test data (list of sentences, no tags on the words)
            E.g  [[word1,word2,...][word1,word2,...]]
    output: list of sentences, each sentence is a list of (word,tag) pairs.
            E.g. [[(word1, tag1), (word2, tag2)...], [(word1, tag1), (word2, tag2)...]...]
    '''
    dict1=defaultdict(list)
    tag_list=defaultdict(int)
    for eachwordtag in train:
        for word,tag in eachwordtag:
            dict1[word].append(tag)
            tag_list[tag]+=1 
    #count all the tags to find the most common one tag
    most_common_Tag=max(tag_list, key=tag_list.get)
    #preprocess the test data, get the non-duplicate version of the words such that calculation can be simplified
    word_dict_test=defaultdict(str)
    word_list=[]
    for each_sentence in test:
        for each_word in each_sentence:
            word_list.append(each_word)
    word_list=set(word_list)
    for i in word_list:
        if i in dict1.keys():
            word_dict_test[i]=statistics_on_word(i,dict1)
        else:
            word_dict_test[i]=most_common_Tag
    predicts = []
    for each_sentence in test:
        each_sentence_prediction=[]
        for each_word in each_sentence:
            if each_word in word_dict_test.keys():
                each_sentence_prediction.append((each_word,word_dict_test[each_word]))
            else:
                each_sentence_prediction.append((each_word,most_common_Tag))
        predicts.append(each_sentence_prediction)
    #raise Exception("You must implement me")
    #print('prediction',predicts,'lenght of prediction',len(predicts),len(test))
    return predicts
#passes baseline test on gradescope
#to set up defaultdict
def nested():
    return defaultdict(int)

def preprocess(train,tagset):
    '''
    preprocess returns a counter of default dict tag_word_pair a counter for each tag-word pair, e.g. for tag1 the tag_word_pair has the form {tag1:{w1:1,w2:2}}
    initial tag: containing all the tags at the first place of each sentence [tag1 ...]
    tag_list containing all the tags contained in the training set
    sentence_tag_list [[tag1,...tagk],[...]] tag for each sentence
    word_counter: a counter containing each unique word and its frequency Counter({'the': 43628, ',': 36127, '.': 30841, 'of': 22896....}
    '''

    initial_tag=[]
    tag_word_pair=defaultdict(nested)#{ti:{wi:1,wi+1:2}}... len(tag_word_pair[ti]) to get C(ti)
    sentence_tag_list=[]
    word_list=[]
    tag_list=[]
    for each_sentence in train:
        temp=[]
        initial_tag.append(each_sentence[0][1])#(word1,tag1) at the start of each sentece use[0], use[1] to get the tag
        for word,tag in each_sentence:
            tag_word_pair[tag][word]+=1
            temp.append(tag)
            word_list.append(word)
            tag_list.append(tag)
            #tag_word_pair['unknown'][word]=0
        sentence_tag_list.append(temp)
    word_counter=Counter(word_list)
    return initial_tag,tag_list,sentence_tag_list,tag_word_pair,word_counter

def initial_probability(initial_tag,nonduplicate,smooth_constant):#already taken log of the probability and smoothed
    '''
    set up the initial probability using the initial_tag and a counter
    '''
    probability_dict=defaultdict(int)
    initial_tag_counter=Counter(initial_tag)
    #print('initial_tag_counter=',initial_tag_counter)
    types=len(nonduplicate) #total unique category initial tag number 
    N=sum(initial_tag_counter.values()) # how many sentencees
    #temp=0#temp used to calculate unlogged probability sum up to 1
    for i in nonduplicate:#initial_tag_counter.keys are the initial tags
    #    temp+= (initial_tag_counter[i]+smooth_constant)/(N+smooth_constant*types)
        probability_dict[i]=math.log10((initial_tag_counter[i]+smooth_constant)/(N+smooth_constant*types))
        #if i =='unknown':
        #    print('should be 0',initial_tag_counter[i])==True,initial_tag_counter['unknown']=0
    #print('un logged statistics sum to 1 is',temp==1)==True
    return probability_dict#key is [TAG]
def A_emission(tag_list_sentence,nonduplicate,smooth_constant):#P(ti|ti-1),transition probability in assignment page
    '''
    A_emission_dict_pair is a counter [ti]:[ti+1]:number of times
    '''
    A_emission_dict_pair=defaultdict(nested)
    A_emission_probability=defaultdict(nested)
    for each_sentence in tag_list_sentence:
        for i in range(0,len(each_sentence)-1):
            A_emission_dict_pair[each_sentence[i]][each_sentence[i+1]]+=1 #{ti:{ti+1:n, tk+1: j},...}
    #check how many types of 2nd tag after 1st tag
    #temp=0
    #print('A_emission_dict_pair',A_emission_dict_pair)
    #for each_tag in A_emission_dict_pair:
    #    temp+=len(A_emission_dict_pair[each_tag])
    #   print('each tag=',each_tag,len(A_emission_dict_pair[each_tag]))
    '''
    first tag= DET 15
    first tag= NOUN 16
    first tag= ADJ 15
    first tag= VERB 16
    first tag= IN 15
    first tag= PUNCT 16
    first tag= CONJ 16
    first tag= ADV 15
    first tag= PERIOD 16
    first tag= TO 9
    first tag= PRON 15
    first tag= NUM 14
    first tag= MODAL 13
    first tag= PART 14
    first tag= UH 11
    first tag= X 9
    '''
    #print('total types combination in training set is',temp) 225
    for t1 in nonduplicate:#t1=ti-1 state if don't use nonduplicate 93.53%
        types=len(A_emission_dict_pair)#no.of tags after t1 state
        N=sum(A_emission_dict_pair[t1].values())#no. of t1 state happening as the 1st state
        temp=0
        for t2 in nonduplicate: #t2=ti state. the 2nd state
            temp+=(A_emission_dict_pair[t1][t2]+smooth_constant)/(N+smooth_constant*(types))
            #print('1sttag=',t1,'2nd tag=',t2,'probability=',(A_emission_dict_pair[t1][t2]+smooth_constant)/(N+smooth_constant*(types)))
            A_emission_probability[t2][t1]=math.log10((A_emission_dict_pair[t1][t2]+smooth_constant)/(N+smooth_constant*(types)))#smoothed and taken log DICT IN FORM OF {{ti+1:{ti:...}}
        #print('for each 1st tag=',t1,'sum probability=',temp)#sum up=1 OR NOT
    return A_emission_probability

def B_emission_learn(pair_dict,counter,smooth_constant):#P(Word|Tag)
    B_emission_probability=defaultdict(nested)
    for each_tag in pair_dict:
        #types=len(pair_dict[each_tag])#word types given each tag
        types=len(counter.keys())#Vocabulary size as X in formula
        N=sum(pair_dict[each_tag].values())#counter for each tag occurence
        for each_word in pair_dict[each_tag]:
            B_emission_probability[each_tag][each_word]=math.log10((smooth_constant+pair_dict[each_tag][each_word])/(N+smooth_constant*(types+1)))
        B_emission_probability[each_tag]['UNKNOWN']=math.log10(smooth_constant/(N+smooth_constant*(types+1)))
    #B_emission_probability['unknown']=math.log10(smooth_constant/(N+smooth_constant*(types+1)))
    return B_emission_probability

def viterbi_p1(train, test):
    tagset = {'NOUN', 'VERB', 'ADJ', 'ADV',
          'PRON', 'DET', 'IN', 'NUM',
          'PART', 'UH', 'X', 'MODAL',
          'CONJ', 'PERIOD', 'PUNCT', 'TO'}
    '''
    TODO: implement the simple Viterbi algorithm. This function has time out limitation for 3 mins.
    input:  training data (list of sentences, with tags on the words)
            E.g. [[(word1, tag1), (word2, tag2)], [(word3, tag3), (word4, tag4)]]
            test data (list of sentences, no tags on the words)
            E.g [[word1,word2...]]
    output: list of sentences with tags on the words
            E.g. [[(word1, tag1), (word2, tag2)...], [(word1, tag1), (word2, tag2)...]...]
    most probable tag sequence from a bigram tagger:
    '''
    #initalization of the nested default dict
    smooth_constant=1E-9
    Transition_probability_dict=defaultdict(int)
    Initial_probability_dict=defaultdict(nested)
    Emission_probability_dict=defaultdict(nested)
    initial_tag,tag_list,tag_list_sentence,tag_word_pair,word_counter=preprocess(train,tagset)
    nonduplicate=set(tag_list)#contain a unknown tag
    #tag_word_pairIS NESTED DICT [Tag][Word]
    Initial_probability_dict=initial_probability(initial_tag,nonduplicate,smooth_constant)
    #15:06-3/20 sum up to 1
    Transition_probability_dict=A_emission(tag_list_sentence,nonduplicate,smooth_constant)
    #print(Transition_probability_dict)
    #Transition probability nested dict probability [ti][ti-1] 
    #print('Transition probability_dict',Transition_probability_dict)
    Emission_probability_dict=B_emission_learn(tag_word_pair,word_counter,smooth_constant)#returns value [type,N] for tag as key, used for calculation of smoother_probability 
    predicts=[]
    '''
    #Emission probability is nested dict probability of [tag][word] based on all the tag-word pair in the training set, 
    #treating all unknown cases as a tag, the key['unknown'] will return a constant, as long as the word not appear in the tag_word_pair(no matter the tag) 
    '''
    
    for each_sentence in test:
        viterbi=defaultdict(nested)
        backpointer=defaultdict(nested)
        bestpath=defaultdict(int)
        each_sentence_prediction=deque()
        #initialization at j=0 1st step
        for i in nonduplicate:
            if each_sentence[0] not in tag_word_pair[i]:#the word doesn't appear in the 
                smoothed_probability=Emission_probability_dict[i]['UNKNOWN']
            else:
                smoothed_probability=Emission_probability_dict[i][each_sentence[0]]
            viterbi[0][i]=Initial_probability_dict[i]+smoothed_probability
        for j in range(1,len(each_sentence)):
            for i in nonduplicate:#[j] stands for the time step, starts with 0,,, [i] is the tag
                #for a same tag i and j calculate the Emission Probability with the Count(ti) with Emission_probability_dict_parameter[i][1]    
                if each_sentence[j] not in tag_word_pair[i] :
                    smoothed_probability=Emission_probability_dict[i]['UNKNOWN']
                else:
                    smoothed_probability=Emission_probability_dict[i][each_sentence[j]]
                temp=-1E10
                index=0
                #getting the biggest viterbi probability and corresponding tag i2 previosu for tag i at jth world of the sentence
                for i2 in nonduplicate:
                    if viterbi[j-1][i2]+Transition_probability_dict[i][i2]+smoothed_probability>=temp:
                        temp=viterbi[j-1][i2]+Transition_probability_dict[i][i2]+smoothed_probability
                        index=i2
                viterbi[j][i]=temp
                backpointer[j][i]=index
        T=len(each_sentence)-1
        Best_Last=max(viterbi[T],key=viterbi[T].get)
        pointer=Best_Last
        while T>=0:
            each_sentence_prediction.appendleft((each_sentence[T],pointer))
            pointer=backpointer[T][pointer]
            T-=1
        predicts.append(list(each_sentence_prediction))
    return predicts
def get_keys(d, value):
    return [k for k,v in d.items() if v == value]
def hapax(tag_word_pair,word_counter,smooth_constant):
    tag_word_pair_Hapax=defaultdict(list)
    Hapax_probability=defaultdict(int)
    #DON'T USE TAG_WORD_PAIR TO GET HAPAX WORD, OVERALL OCCURENCE=1 != OCCURENCE=1 IN EACH TAG
    Hapax_word=get_keys(word_counter,1)
    Hapax_word_number=len(Hapax_word)
    for each_tag in tag_word_pair:
        for each_word in tag_word_pair[each_tag]:
            if each_word in Hapax_word:
                tag_word_pair_Hapax[each_tag].append(each_word)
    no_of_tags=len(tag_word_pair)###subject to future change on tag list of unknown 
    for each_tag in tag_word_pair:
        if each_tag not in tag_word_pair_Hapax:
            Hapax_probability[each_tag]=smooth_constant/(Hapax_word_number+smooth_constant*no_of_tags)
        else:
            Hapax_probability[each_tag]=(smooth_constant+len(tag_word_pair_Hapax[each_tag]))/(Hapax_word_number+smooth_constant*no_of_tags)
    return Hapax_probability,Hapax_word
    '''
    print(Hapax_probability,sum(Hapax_probability.values()))
    defaultdict(<class 'int'>, {'DET': 0.001273885917555197, 'NOUN': 0.583671101135647, 'ADJ': 0.17950202555180522, 'VERB': 0.1594093795306601, 'IN': 0.001100174280484778, 
    'PUNCT': 5.790387902347305e-10, 'CONJ': 0.0005211354902500475, 'PERIOD': 0.00011580833708573632, 'ADV': 0.03265778834827758, 'TO': 5.790387902347305e-10, 'PRON': 0.00133178979657867, 
    'NUM': 0.03653734824285028, 'MODAL': 0.0005790393692735206, 'PART': 5.790387902347305e-10, 'UH': 0.002547771256071604, 'X': 0.0007527510063439398}) 1.0
    #print(tag_word_pair_Hapax['X'])-》['whaddya', 'mecum', "d'entretenir", 'ij', 'faires', 'what-will-t.', 'eliot-or-martin', 'buber-think', 'say-speak', 'sangiovanni', 'howda', "why'n", "'tain't"]
    '''
def B_emission_hapax(pair_dict,counter,smooth_constant,Hapax_probability):#P(Word|Tag)
    B_emission_probability=defaultdict(nested)
    for each_tag in pair_dict:
        #types=len(pair_dict[each_tag])#word types given each tag
        types=len(counter.keys())#Vocabulary size as X in formula
        N=sum(pair_dict[each_tag].values())#counter for each tag occurence
        smooth_constant_new=smooth_constant*Hapax_probability[each_tag]
        for each_word in pair_dict[each_tag]:
            B_emission_probability[each_tag][each_word]=math.log10((smooth_constant_new+pair_dict[each_tag][each_word])/(N+smooth_constant_new*(types+1)))
        B_emission_probability[each_tag]['UNKNOWN']=math.log10(smooth_constant_new/(N+smooth_constant_new*(types+1)))
    #B_emission_probability['unknown']=math.log10(smooth_constant/(N+smooth_constant*(types+1)))
    return B_emission_probability
def viterbi_p2(train, test):
    '''
    TODO: implement the optimized Viterbi algorithm. This function has time out limitation for 3 mins.
    input:  training data (list of sentences, with tags on the words)
            E.g. [[(word1, tag1), (word2, tag2)], [(word3, tag3), (word4, tag4)]]
            test data (list of sentences, no tags on the words)
            E.g [[word1,word2...]]
    output: list of sentences with tags on the words
            E.g. [[(word1, tag1), (word2, tag2)...], [(word1, tag1), (word2, tag2)...]...]
    '''
    tagset = {'NOUN', 'VERB', 'ADJ', 'ADV',
          'PRON', 'DET', 'IN', 'NUM',
          'PART', 'UH', 'X', 'MODAL',
          'CONJ', 'PERIOD', 'PUNCT', 'TO'}
    smooth_constant=1E-5
    Transition_probability_dict=defaultdict(int)
    Initial_probability_dict=defaultdict(nested)
    Emission_probability_dict=defaultdict(nested)
    initial_tag,tag_list,tag_list_sentence,tag_word_pair,word_counter=preprocess(train,tagset)
    nonduplicate=set(tag_list)
    Initial_probability_dict=initial_probability(initial_tag,nonduplicate,smooth_constant)
    #15:06-3/20 sum up to 1
    Transition_probability_dict=A_emission(tag_list_sentence,nonduplicate,smooth_constant)
    Hapax_probability,Hapax_word=hapax(tag_word_pair,word_counter,smooth_constant)
    Emission_probability_dict=B_emission_hapax(tag_word_pair,word_counter,smooth_constant,Hapax_probability)#returns value [type,N] for tag as key, used for calculation of smoother_probability 
    predicts=[]
    '''
    #checking if the sum of word_tag_pair sum equals total word counter
    #for each_tag in tag_word_pair:
        statistics+=sum(tag_word_pair[each_tag].values())
    print('tag word pair all word sum',statistics,sum(word_counter.values())) #Result is true, overall sum of word counter ==sum of tag_word_pair
    
    for each_tag in tag_word_pair:
        #tag_word_pair_occuring_once[each_tag]=(get_keys(tag_word_pair[each_tag],1))
        tag_word_pair_occuring_once[each_tag]=(get_keys(tag_word_pair[each_tag],1))
        print('happening once, under each tag=',each_tag,len(tag_word_pair_occuring_once[each_tag]))
        statistics+=len(tag_word_pair_occuring_once[each_tag])
        if len(tag_word_pair_occuring_once[each_tag])==0:
            del tag_word_pair_occuring_once[each_tag]#delete the keys with no words occuring once
    '''
    # word counter to get word appearing once, since occuring once under each tag may not guarantee happening once overall

    predicts = []
    for each_sentence in test:
        viterbi=defaultdict(nested)
        backpointer=defaultdict(nested)
        bestpath=defaultdict(int)
        each_sentence_prediction=deque()
        #initialization at j=0 1st step
        for i in nonduplicate:
            if each_sentence[0] not in tag_word_pair[i]:#the word doesn't appear in the 
                smoothed_probability=Emission_probability_dict[i]['UNKNOWN']
            else:
                smoothed_probability=Emission_probability_dict[i][each_sentence[0]]
            viterbi[0][i]=Initial_probability_dict[i]+smoothed_probability
        for j in range(1,len(each_sentence)):
            for i in nonduplicate:#[j] stands for the time step, starts with 0,,, [i] is the tag
                #for a same tag i and j calculate the Emission Probability with the Count(ti) with Emission_probability_dict_parameter[i][1]    
                if each_sentence[j] not in tag_word_pair[i] :
                    smoothed_probability=Emission_probability_dict[i]['UNKNOWN']
                else:
                    smoothed_probability=Emission_probability_dict[i][each_sentence[j]]
                temp=-1E10
                index=0
                #getting the biggest viterbi probability and corresponding tag i2 previosu for tag i at jth world of the sentence
                for i2 in nonduplicate:
                    if viterbi[j-1][i2]+Transition_probability_dict[i][i2]+smoothed_probability>=temp:
                        temp=viterbi[j-1][i2]+Transition_probability_dict[i][i2]+smoothed_probability
                        index=i2
                viterbi[j][i]=temp
                backpointer[j][i]=index
        T=len(each_sentence)-1
        Best_Last=max(viterbi[T],key=viterbi[T].get)
        pointer=Best_Last
        while T>=0:
            each_sentence_prediction.appendleft((each_sentence[T],pointer))
            pointer=backpointer[T][pointer]
            T-=1
        predicts.append(list(each_sentence_prediction))
    return predicts