import codecs
import re
import argparse
import requests


parser = argparse.ArgumentParser(description='Process some social net messages.')
parser.add_argument('integer', metavar='first_file_number', type=int,
                    help='an integer from which to start output file naming')
                    
parser.add_argument('filename',
                    help='name of the source file with messages')

args = parser.parse_args()

filename = args.filename
# try:
#   file_data = open(f"drive/MyDrive/PIMU_project/{filename}", encoding="utf-8").read()
# except ValueError: 
#   print("Bad encoding!")
file_data = open(f"./{filename}", encoding="windows-1251").read()

# От кого
# re.findall(r"От кого:[\n ]+Пользователь Анастасия Анодина \([\w\:/\.]*\)\n[\w\n\.\:\?\(\)\/ ]*?(?=Кому|От кого)", file_data)
# От кого и кому
# re.findall(r"От кого:[\n ]+Пользователь Анастасия Анодина \([\w\:/\.]*\)\n[\w\n\.\:\?\(\)\/ ]*?От кого:", file_data)

# get all users
users = re.findall(r"Пользователь ([\w\&\#\; ]* \([\w\:/\.]*\))", file_data)
unique_users = []
for user in users:
    if user not in unique_users:
        unique_users.append(user)


user_number = args.integer
print(f"User count: {len(unique_users)}")
print()

for user in unique_users:
    # print(user)
    user_file = open(f"text{user_number}.txt", "w")
    user_number += 1
    escaped_user = user.replace('(', '\(').replace(')', '\)')
    user_messages = re.findall(rf"От кого:[\n ]+Пользователь {escaped_user}\n([\w\n\.\:\?\(\)\/\&\#\; ]*?)(?=Кому|От кого)", file_data)
    message_string = '\n'.join(user_messages)
    user_file.write(f"<author>{user}</author>\n\n{message_string}")
user_file.close()

current_user_position = 0
for num in range(args.integer, user_number):
    user_filename =  f"text{num}.txt"
    user_file = open(user_filename, "r+")
    user_data = user_file.read()
    user_file.close()
    
    user_image_links = re.findall(r"(https[\w\:/\.]+\.[jpng]{3})\)", user_data)
    print(user_filename)
    print(f"Author: {unique_users[current_user_position]}")
    print(f"Images count: {len(user_image_links)}")
    
    current_user_position += 1
    
    image_number = 1
    for link in user_image_links:
        correct_image_name = f'{user_filename.split(".")[0]}_img{image_number}.{link.split(".")[-1]}'
        image_number += 1
        with open(correct_image_name, 'wb') as handle:
        
            
            # print(f"link {link}")
            # print(f"data {user_data_with_images[:1300]}")      
            response = requests.get(link, stream=True)

            if not response.ok:
                print(f"Bad link: {link}")
                print(f"Near image name: {correct_image_name}")
                print(response.status_code)
                print(response.reason)
                print(f"More info about error on https://developer.mozilla.org/ru/docs/Web/HTTP/Status/{response.status_code}")
                print()

            for block in response.iter_content(1024):
                if not block:
                    break

                handle.write(block)
        
        user_data = re.sub(fr"{link}", f"<img>{correct_image_name}</img>", user_data)
        
    user_sound_links = re.findall(r"(https[\w\:/\.]+\.[og]{3})\)", user_data)
    print(f"Sounds count: {len(user_sound_links)}")  
    print()
    
    sound_number = 1
    for link in user_sound_links:
        correct_sound_name = f'{user_filename.split(".")[0]}_sound{sound_number}.{link.split(".")[-1]}'
        sound_number += 1
        
        with open(correct_sound_name, 'wb') as handle:
            # print(f"link {link}")
            # print(f"data {user_data_with_images[:1300]}")      
            response = requests.get(link, stream=True)

            if not response.ok:
                print(f"Bad link: {link}")
                print(f"Near sound name: {correct_sound_name}")
                print(response.status_code)
                print(response.reason)
                print(f"More info about error on https://developer.mozilla.org/ru/docs/Web/HTTP/Status/{response.status_code}")
                print()

            for block in response.iter_content(1024):
                if not block:
                    break

                handle.write(block)
        
        user_data = re.sub(fr"{link}", f"<sound>{correct_sound_name}</sound>", user_data)
    
    user_file = open(user_filename, "w+")
    user_file.write(user_data)
    user_file.close()
