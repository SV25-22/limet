def title_tag(txt):
    return txt.split(" ")[-1]

def read_titles(file_location):
    try:
        with open(file_location,'r') as file:
            titles = file.readlines()
            #print(titles)
            for i in range(len(titles)):
                titles[i] = titles[i].replace("\n","")
            return titles
    except Exception as e:
        print(f"An error has occured {e}")

def delete_title(file_location,title):
    try:
        with open(file_location, 'r') as file:
            titles = file.readlines()
        for i in range(len(titles)):
            if title in titles[i] :
                del titles[i]
                break
        with open(file_location,'w') as file:
            file.write(''.join(titles))
    except Exception as e:
        print(e)
        print("error deleting")

def add_title(title,once):

    new_title = title
    if(once):
        new_title = title + " o"
    else:
        new_title = title + " s"

    titles = read_titles("naslovi.txt")
    titles.append(new_title)
    try:
        with open("naslovi.txt",'w') as file:
            file.write('\n'.join(titles))
    except Exception as e:
        print(e)
        print("error adding")

def delete_titles(titles):
    for i in range(len(titles)):
        tag = title_tag(titles[i])
        if("o" in tag):
            titles[i] = titles[i][:-1]
            titles[i] = titles[i] + "(movie)"
        else:
            titles[i] = titles[i][:-2]
    return titles

def edit_titles_show(titles):
    for i in range(len(titles)):
        if("(movie)" in titles[i]):
            titles[i] = titles[i][:-8]
    return titles

def edit_title_indexing(titles):
    indexes = []
    for i in range(len(titles)):
        if("(movie)" in titles[i]):
            indexes.append(1)
        else:
            indexes.append(0)
    return indexes