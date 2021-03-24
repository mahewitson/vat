import argparse
import requests
import validators
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from bs4 import Comment

parser = argparse.ArgumentParser(description='The Achilles HTML Vulnerability Analyzer Version 1.0')

parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.0')
parser.add_argument('file', type=str, help="The filename of the HTML to analyze")

args = parser.parse_args()

file = args.file
report = ''
#print(file)
if(file):
  f = open(file)
  file_html = f.read()
#  print(file_html)
  parsed_html = BeautifulSoup(file_html, 'html.parser')
#  print(parsed_html)

  forms           = parsed_html.find_all('form')
  comments        = parsed_html.find_all(string=lambda text:isinstance(text, Comment))
  password_inputs = parsed_html.find_all('input', { 'name' : 'password'})

  for form in forms:
    if(form.get('action').find('https') < 0):
        report += file + ' Form Issue: Insecure form action ' + form.get('action') + ' found in document\n'

  for comment in comments:
    if(comment.find('key: ') > -1):
      report += file + ' Comment Issue: Key found in HTML comments, please remove\n'

  for password_input in password_inputs:
    if(password_input.get('type') != 'password'):
      report += file + ' Input Issue: Password field requesting plain text\n'

else:
  print('That one wasn\'t so good')

if(report != ''):
  print(report)
