import PyPDF2
import os
from os import listdir
from os.path import isfile, join
from io import StringIO
import pandas as pd
from collections import Counter
import spacy
import textract
import textract as textract
from spacy.lang.fr.examples import sentences

nlp = spacy.load("fr_core_news_sm")
from spacy.matcher import PhraseMatcher

# Function to read resumes from the folder one by one
mypath = './DATA/CV/'  # enter your path here where you saved the resumes
onlyfiles = [os.path.join(mypath, f) for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]


def pdfextract(file):
    extension = os.path.splitext(file)[1]
    if (extension == ".pdf"):
        fileOpen = open(file, 'rb')
        fileReader = PyPDF2.PdfFileReader(fileOpen)
        countpage = fileReader.getNumPages()
        count = 0
        text = []
        while count < countpage:
            pageObj = fileReader.getPage(count)
            count += 1
            t = pageObj.extractText()
            text.append(t)

    #elif extension == ".doc" or extension == ".docx":
        #text = textract.process(file)



    return text


# function to read resume ends


# function that does phrase matching and builds a candidate profile
def create_profile(file):
    text = pdfextract(file)
    if (text != "0"):
        text = str(text)
        text = text.replace("\\n", "")
        text = text.lower()
        # below is the csv where we have all the keywords, you can customize your own
        keyword_dict = pd.read_csv('csv/hardskills.csv')
        java_words = [nlp(text) for text in keyword_dict['java language'].dropna(axis=0)]
        php_words = [nlp(text) for text in keyword_dict['php language'].dropna(axis=0)]
        csharp_words = [nlp(text) for text in keyword_dict['c# language'].dropna(axis=0)]
        web_words = [nlp(text) for text in keyword_dict['web'].dropna(axis=0)]
        os_words = [nlp(text) for text in keyword_dict['os'].dropna(axis=0)]
        mobile_words = [nlp(text) for text in keyword_dict['mobile'].dropna(axis=0)]
        ide_words = [nlp(text) for text in keyword_dict['ide'].dropna(axis=0)]
        javascript_words = [nlp(text) for text in keyword_dict['javascript language'].dropna(axis=0)]
        database_words = [nlp(text) for text in keyword_dict['database'].dropna(axis=0)]

        matcher = PhraseMatcher(nlp.vocab)
        matcher.add('javascript', None, *javascript_words)
        matcher.add('JAVA', None, *java_words)
        matcher.add('php', None, *php_words)
        matcher.add('C#', None, *csharp_words)
        matcher.add('web', None, *web_words)
        matcher.add('os', None, *os_words)
        matcher.add('mobile', None, *mobile_words)
        matcher.add('IDE', None, *ide_words)
        matcher.add('database', None, *database_words)
        doc = nlp(text)

        d = []
        matches = matcher(doc)
        for match_id, start, end in matches:
            rule_id = nlp.vocab.strings[match_id]  # get the unicode ID, i.e. 'COLOR'
            span = doc[start: end]  # get the matched slice of the doc
            d.append((rule_id, span.text))
        keywords = "\n".join(f'{i[0]} {i[1]} ({j})' for i, j in Counter(d).items())

        ## convertimg string of keywords to dataframe
        df = pd.read_csv(StringIO(keywords), names=['Keywords_List'])
        df1 = pd.DataFrame(df.Keywords_List.str.split(' ', 1).tolist(), columns=['Subject', 'Keyword'])
        df2 = pd.DataFrame(df1.Keyword.str.split('(', 1).tolist(), columns=['Keyword', 'Count'])
        df3 = pd.concat([df1['Subject'], df2['Keyword'], df2['Count']], axis=1)
        df3['Count'] = df3['Count'].apply(lambda x: x.rstrip(")"))

        base = os.path.basename(file)
        filename = os.path.splitext(base)[0]

        name = filename.split('_')
        name2 = name[0]
        name2 = name2.lower()
        ## converting str to dataframe
        name3 = pd.read_csv(StringIO(name2), names=['Candidate Name'])

        dataf = pd.concat([name3['Candidate Name'], df3['Subject'], df3['Keyword'], df3['Count']], axis=1)
        dataf['Candidate Name'].fillna(dataf['Candidate Name'].iloc[0], inplace=True)

        return (dataf)


# function ends

# code to execute/call the above functions

final_database = pd.DataFrame()
i = 0
while i < len(onlyfiles):
    file = onlyfiles[i]
    dat = create_profile(file)
    final_database = final_database.append(dat)
    i += 1

    print(final_database)

# code to count words under each category and visulaize it through Matplotlib

final_database2 = final_database['Keyword'].groupby(
    [final_database['Candidate Name'], final_database['Subject']]).count().unstack()
final_database2.reset_index(inplace=True)
final_database2.fillna(0, inplace=True)
new_data = final_database2.iloc[:, 1:]
new_data.index = final_database2['Candidate Name']
# execute the below line if you want to see the candidate profile in a csv format
sample2=new_data.to_csv('sample.csv')
import matplotlib.pyplot as plt

plt.rcParams.update({'font.size': 10})
ax = new_data.plot.barh(title="Resume keywords by category", legend=True, figsize=(20, 100), stacked=True)
labels = []
for j in new_data.columns:
    for i in new_data.index:
        label = str(j) + ": " + str(new_data.loc[i][j])
        labels.append(label)
patches = ax.patches
for label, rect in zip(labels, patches):
    width = rect.get_width()
    if width > 0:
        x = rect.get_x()
        y = rect.get_y()
        height = rect.get_height()
        ax.text(x + width / 2., y + height / 2., label, ha='center', va='center')
plt.show()
