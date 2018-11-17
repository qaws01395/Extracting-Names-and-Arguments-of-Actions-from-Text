
# coding: utf-8

# In[6]:




# # Read in the file
# file = open('cookingTutorialCrawl.txt', 'r')
# filedata = file.read()
# # print(filedata)
#
# filedata = ' '.join(filedata.split())
# # print(filedata)
#
# # Replace the target string
# filedata = filedata.replace(' ', ',').replace('.', '\n')
# print(filedata)
#
# # Write the file out again
# with open('cookingTutorialCrawlEdit.csv', 'w') as file:
#     file.write(filedata)


# Read in the file
file = open('cookingTutorialCrawl.txt', 'r')
# filedata = file.read()
# print(filedata)
newFile = open('temp.txt', 'w')

for line in file:
    if "–" not in line and "Ingredients" not in line :
        line = ' '.join(line.split())
        line = line.replace(".", '\n').lstrip()
        line = line.replace(',', '~')
        # print(line)
        newFile.write(line)
newFile.close()
file.close()

newFile2 = open('cookingTutorialCrawlEdit.csv', 'w')
file2 = open('temp.txt', 'r')
for line in file2:
    line = line.lstrip().replace(' ', ',')
    # print(line)
    newFile2.write(line)
file2.close()
newFile2.close()

# print(filedata)

# Replace the target string
# filedata = filedata.replace(' ', ',').replace('.', '\n')
# print(filedata)

# Write the file out again
# with open('cookingTutorialCrawlEdit.csv', 'w') as file:
#     file.write(filedata)
