# NLP-extraction-and-planning

## Description
Given a paragraph of natural language text, we want to extract the susbstantial 'action-argument' sentences from text, giving the order by semantics meaning, in order to plan the automatic process to accomplish a new unkonwn task. So far we are able to give the possibility of 'action-argument' using LSTM, Pas Tagging techniques. 

## Data processing
We made a web crawler to grab receipe data from websites, and keep the steps descriptions for cooking dishes.


### Manually mark data
1. Run `python replacePrint.py` -> temp.txt (can be deleted), cookingTutorialCrawlEdit.csv are created
2. Use editor open cookingTutorialCrawlEdit.csv, delete unnecessary text before 'Step 1: ...' and save as stage1_CT.csv
3. Use tool (MS Office, Libre Office) to open stage1_CT.csv
4. Replace action verbs with #, action arguments with @, save as stage2_CT.csv
5. Delete all the words except for # and @, save as mark_CT.csv
