import csv
import sys
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os

fieldnames=['cmd', 'info', 'tags']
run = True

def viewFile():
    with open('archive.csv', 'r') as fl:
                reader = csv.DictReader(fl, fieldnames=fieldnames, delimiter=';')
                for line in reader:
                    print(line['cmd']+' | '+line['info']+' | '+line['tags'])

def main():
    while run:
        comand = input('Choose an action: add, search, view -->')
        if comand == 'quit':
            sys.exit()
        elif comand == 'add':
            cmd = str(input('Write the command: ')).upper()
            info = input('Write the infos: ')
            tag = input('Write a tag: ')
            with open('archive.csv', 'a', newline='') as fl:
                writer = csv.DictWriter(fl, fieldnames, delimiter=';')
                writer.writerow({'cmd': cmd, 'info':info, 'tags': tag})
                g_login = GoogleAuth()
                g_login.LocalWebserverAuth()
                drive = GoogleDrive(g_login)
                file_drive = drive.CreateFile({'title':os.path.basename(fl.name) })
                file_drive.SetContentFile('archive.csv')
                file_drive.Upload()
                print('Command added')
        elif comand == 'search':
            with open('archive.csv', 'r') as fl:
                reader = csv.DictReader(fl, fieldnames=fieldnames)
                choice = input('Search by command or tag? c/t ')
                if choice == 't':
                    tag = input('Write the tag: ')
                    for line in reader:
                        if tag in line['tags']:
                            print(line)
                elif choice == 'c':
                    cmd = input('Write the comando')
                    for line in reader:
                        if cmd in line['cmd']:
                            print(line)
        elif comand == 'view':
            viewFile()

main()
