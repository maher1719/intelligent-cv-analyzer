

from resume_parser import resumeparse


from pyresparser import ResumeParser
import json
#data = ResumeParser
data = resumeparse.read_file('Amal_Ben_Othman_CV.pdf')#.get_extracted_data()
fileJson= open("cv.json","w")
print(data)
fileJson.write(json.dumps(data, indent = 4))