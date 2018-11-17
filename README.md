# NLP-extraction-and-planning

## Data processing

### Manually mark data
1. Run `python replacePrint.py` -> temp.txt (can be deleted), cookingTutorialCrawlEdit.csv are created
2. Use editor open cookingTutorialCrawlEdit.csv, delete unnecessary text before 'Step 1: ...' and save as stage1_CT.csv
3. Use tool (MS Office, Libre Office) to open stage1_CT.csv
4. Replace action verbs with #, action arguments with @, save as stage2_CT.csv
5. Delete all the words except for # and @, save as mark_CT.csv
