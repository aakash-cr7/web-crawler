import os
from urllib.parse import urlparse

def create_directory(directory):
    if not os.path.exists(directory):
        print('Creating a new directory ' + directory)
        os.makedirs(directory)

def write_file(path, data):
    with open(path, 'w') as f:
        f.write(data)

# Appending data to current file
def append(path, data):
    with open(path, 'a') as file:
        file.write(data + '\n')

# Deleting content of a file
def delete_file_content(path):
    print('in delete ' + path)
    with open(path, 'w'):
        pass

# Converting each line of a file into a set item
def file_to_set(file_name):
    results = set()
    with open(file_name, 'rt') as f:
        for line in f:
            # remove new line character from line that we added in append method
            results.add(line.replace('\n', ''))
    return results

# Converting each item of a set into a new line in a file
def set_to_file(urls, file):
    # Fix for if the file path is not there
    #if file == '':
    #   return
    delete_file_content(file)
    for link in sorted(urls):
        append(file, link)

# Creating project folder, files
def create_files(project_name, base_url):

    # Creating a waiting list, a list of links 
    queue = os.path.join(project_name, 'queue.txt')
    # A list of already visited links
    crawled_list = os.path.join(project_name, 'crawled_list.txt')

    if not os.path.isfile(queue):
        write_file(queue, base_url)
    if not os.path.isfile(crawled_list):
        # Creating empty file
        write_file(crawled_list, '')  

# (name.example.com)
def get_sub_domain_name(url):
    try:
        return urlparse(url).netloc
    except:
        return '' 

# Get domain name (example.com)
def get_domain_name(url):
    try:
        results = get_sub_domain_name(url).split('.')
        # Fix for getting google.co.in
        if results[-2] == 'co':
            return results[-3] + '.' + results[-2] + '.' + results[-1]
        return results[-2] + '.' + results[-1]
    except:
        return ''

#print(get_domain_name('https://www.google.co.in/?gfe_rd=cr&ei=Gw_5Vr2lEYSM8Qemu4HICw&gws_rd=ssl#q=india'))


