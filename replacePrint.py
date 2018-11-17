
# coding: utf-8

# In[6]:




# Read in the file
file = open('cookingTutorialCrawl.csv', 'r')
filedata = file.read()
# print(filedata)

# Replace the target string
filedata = filedata.replace(' ', ',').replace('.', '\n')
print(filedata)

# Write the file out again
with open('cookingTutorialCrawlEdit.csv', 'w') as file:
    file.write(filedata)


