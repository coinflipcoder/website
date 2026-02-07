import argparse
import os
import json
from datetime import datetime
from consts import DEPLOY_TIMESTAMP
import database_handler as database_handler

year = datetime.now().year
counter = database_handler.getButtonValue()
fact = database_handler.getCurrentFact()
wall = database_handler.getAutographs()

HEADER = """So youre one of those creatures, huh.
You think even HTML is bloat?
Thats fine, because youre in luck! I made this txt version of my webbed site, just for you :)\n"""

INTRODUCTION = """I am Fabi, a young and naive programmer from Germany who will retreat
to the backend upon spotting a css class. Its nice to meet you! On
this page you will find a variety of things I have wasted my time on.\n"""

ABOUT = """~~ /about ~~
Contact Me
Feel free to reach out through any of the following platforms:

~[ Fediverse ]~
@coinflipcoder@chaos.social

~[ Discord ]~
@coinflipcoder

~[ Matrix ]~
@me:coinflipcoder.dev

~[ Github ]~
Coinflipcoder

GPG Key
This GPG key is used to sign commits on Github.
 - Download > https://coinflipcoder.dev/assets/gpg_key.asc\n"""

class DataFiles:
    def __init__(self, projects, hackspaces, events):
        self.projects = projects
        self.hackspaces = hackspaces
        self.events = events


def newlines(f, count):
  for i in range(count):
    f.write("\n")


def write_home(f):
  f.write(HEADER)
  newlines(f, 1)
  f.write(INTRODUCTION)
  newlines(f, 1)
  f.write('Sillies (only updated on redeployment)\n')
  f.write(f'Useless fact: {fact['text']}\n')
  f.write(f'> {fact['permalink']}\n')
  newlines(f, 1)
  f.write(f'Big number go uppies: {counter}\n')
  f.write('This is a text file. You cant press this button.\n')


def write_projects(f, projects):
  f.write('~~ /projects ~~\n')
  f.write('Obligatory projects page\n')
  f.write('Here are some of the things I have worked on.\n')
  newlines(f, 1)

  for project in projects:
    f.write(f'~[ {project['title']} ]~\n')
    f.write(f'{project['description']}\n')
    
    f.write(f'Languages: ')
    for lang in project['languages']:
      f.write(f'{lang}')
    f.write('\n')

    for link in project['links']:
      f.write(f' - {link['name']} > {link['url']}\n')
    newlines(f, 1)

  f.write('Look at this incredibly funny meme :3\n')
  f.write('> https://coinflipcoder.dev/assets/images/itsallminecraft.png\n')

def write_hackspaces(f, hackspaces, events):
  f.write('~~ /chaos ~~\n')
  f.write('My Hackspace Passport\n')

  for space in hackspaces:
    f.write(f'- {space['name']} > {space['link']}\n')

  newlines(f, 1)
  f.write('My Event Calendar\n')

  for event in events:
    f.write(f'- {event['name']} ({event['start']}-{event['end']}) > {event['link']}\n')


def write_wall(f):
  f.write(f'~~ /wall ~~\n')
  f.write(f'You cannot add to the autograph wall here. It is also only updated on redeployment.\n')
  newlines(f, 1)
  for entry in wall:
    f.write(f'"{entry[1]}"\n')
    f.write(f'~ {entry[0]}\n')
    newlines(f, 1)

def write_travel(f):
  f.write('~~ /travel ~~\n')
  f.write('Is this map 100% accurate? No.\n')
  f.write('> https://viaduct.world/share/m/J8bw75e6Rc_So4hW\n')


def write_footer(f):
  f.write(f'Last deployed: {DEPLOY_TIMESTAMP} UTC.\n')
  f.write(f'Web design is my passion. Copyleft {year}.\n')


def write(file_dir, data_files):
  with open(f'{file_dir}/txtversion.txt', 'w') as f:
    write_home(f)
    newlines(f, 3)
    write_projects(f, data_files.projects)
    newlines(f, 3)
    write_hackspaces(f, data_files.hackspaces, data_files.events)
    newlines(f, 3)
    f.write(ABOUT)
    newlines(f, 3)
    write_wall(f)
    newlines(f, 2) # only 2 here cuz the wall loop prints a newline after the last entry
    write_travel(f)
    newlines(f, 3)
    write_footer(f)


def main():
  parser = argparse.ArgumentParser(description="Generate the .txt version of the website")
  parser.add_argument("--file-dir", required=True, help="Directory to write the output file")
  parser.add_argument("--data-dir", required=True, help="Directory of the JSON data files")

  args = parser.parse_args()
  os.makedirs(args.file_dir, exist_ok=True)

  with open(f'{args.data_dir}/projects.json', 'r') as file:
    projects = json.load(file)

  with open(f'{args.data_dir}/hackspace_passport.json', 'r') as file:
    hackspaces = json.load(file)

  with open(f'{args.data_dir}/events.json', 'r') as file:
    events = json.load(file)

  data_files = DataFiles(projects, hackspaces, events)

  print("[*] Generating TXT File..")
  write(args.file_dir, data_files)
  print("Done!\n")


if __name__ == "__main__":
  main()
