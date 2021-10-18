# voice emotion tagging
# by Ming Nan Luo & Dejoli TienTcheu Touko Landry
# -*- coding:utf-8 -*-

import os
import soundfile as sf



# define the emotionname as key, and the value as the index.
emotionname_and_emotionindex ={
    'boredom':'01',
    'happy':'03',
    'neutral':'02',
    'sad':'04',
    'anger':'05', 'angry':'05',
    'fear':'06',  'feary':'06',
    'disgust':'07',
    'surprise':'08', 'surprised':'08',
    'excited':'09',
    'pleasure':'10',
    'pain':'11',
    'disapointed':'12',
    'others':'13'
    #'01 = neutral, 02 = calm, 03 = happy, 04 = sad, 05 = angry, 06 = fearful, 07 = disgust, 08 = surprised'
}
emotionname_and_emotionindex_reverse ={
    '01':'boredom','03':'happy','02':'neutral','04':'sad','05':'anger','06':'fear','07':'disgust','08':'surprise',
    '09':'excited','10':'pleasure','11':'pain','12':'disapointed','13':'others',
}

# function to optain wavefile_name and its corresponding emotion
def get_wavname_and_label_from_a_line(line,emotionname_and_emotionindex=emotionname_and_emotionindex):
    line_items = line.split(':')
    wavname = line_items[0].strip()
    emotion_name = line_items[-1].strip()
    emotion_label = emotionname_and_emotionindex[emotion_name] # such '08'
    return wavname,emotion_label
# get all wave paths
def get_all_wav_paths(file_dir):
    '''
    获取指定文件夹及其子文件夹下的所有.wav音频路径
    :param file_dir: 文件夹地址（str）
    :return: 音频地址列表（list）
    '''
    _wav_paths = []
    for dir, sub_dir, file_base_name in os.walk(file_dir):
        #         print(dir, sub_dir, file_base_name)
        for file in file_base_name:
            if file.endswith(".wav") or file.endswith(".WAV"):
                _wav_paths.append(os.path.join(dir, file))
    return _wav_paths

# Access to tag result folder

def tagged_file(ABCD_files,annotated_file_path):
    allset = {}
    for each_person in ABCD_files:
        allset[each_person] = {} #  A={}
        # obtain acteur:
        acteurs_files = os.listdir(os.path.join(annotated_file_path,each_person))
    #     print( acteurs_files )
        for each_acteur in acteurs_files:
            # obtain wavs(lines)
            with open(os.path.join(annotated_file_path,each_person, each_acteur),encoding="utf-8") as f:
                wav_lines = f.readlines()
            allset[each_person][each_acteur]= wav_lines
            print(  allset[each_person][each_acteur] )
    return allset
#Getting Annotators result
def get_each_annotator(allset,ABCD_files):
    dataset ={}
    for each_person in ABCD_files: # A's value is at the begining of the list
        for each_acteur in allset[each_person]:
            for each_wavline in allset[each_person][each_acteur]:
                if len(each_wavline.strip())<1: continue # skip blank lines
                # print(each_wavline)
                wav_filename, wav_label = get_wavname_and_label_from_a_line(each_wavline)
    #             print(wav_filename,":",wav_label)
                key = each_acteur + '#' + wav_filename
    #             print(key,":",wav_label)
                #print(wav_filename,wav_label,key)
                if key not in dataset:
                    dataset[key]=[]
                dataset[key].append(wav_label)
    return dataset

# voting function base on the emotion with max number of vote
def vote(x):
    # x= [04', '08', '04', '05']
    tempset={}
    for each in x:
        if each in tempset:
            tempset[each]+=1
        else:
            tempset[each]=1
    max_num=1
    max_num_name=x[0] # if there are no duplicate value in list X, then choose A's value.
    for each in tempset:
        if tempset[each]>max_num:
            max_num = tempset[each]
            max_num_name = each
    return max_num_name

# audio sample path
# root= r"/Volumes/Elements Yu/ASVP-ESD_UPDATE/"
#assign to audio emotion which has the maximum number of vote(annotation)
def assign_high_annotation(root,annotated_file_path,ABCD_files,final_path):
    sample = get_all_wav_paths(root)
    all_tagged_file = tagged_file(ABCD_files,annotated_file_path)
    dataset = get_each_annotator(all_tagged_file,ABCD_files)
    for i in range(len(sample)):
        audio_base_name = os.path.basename(sample[i])
        #     print(audio_base_name)
        acteurs_content = {}
        for each in dataset:
            acteur_filename, wav_line = each.split('#')
            # wav_line_items = wav_line.split('-')
            wav_label = vote(dataset[each])
            wav_line_items = audio_base_name.split('-')

            if wav_line in audio_base_name:
                data, sr = sf.read(sample[i])
                result_line = '-'.join(wav_line_items[:2]) + '-' + wav_label + '-' + '-'.join(wav_line_items[3:])
                print(result_line)

                sf.write(final_path + result_line, data=data, samplerate=16000)




if __name__ == "__main__":
    annotated_file_path = r"/Volumes/Elements Yu/label/"
    ABCD_files = os.listdir(annotated_file_path)
    # print(ABCD_files)
    root_of_audio_to_tag = r"/Volumes/Elements Yu/ASVP-ESD_UPDATE/"
    final_path = r"/Volumes/Elements Yu/vote/"
    assign_high_annotation(root_of_audio_to_tag,annotated_file_path,ABCD_files,final_path)
