import os 
import math


############################# smart_sort_files(path) ###############################################################
def replace_str(text):
    """
    Remove punctuations, symbols and numbers from string 

    Parameters
    ----------
    text : string to process (str)

    Returns 
    -------
    text : modified string
    """

    #list of items that we will remove them from the text
    deleted_items = [".", "?", "!", ",", ";", ":", "'", "/", "\\", "\"", "-", "_",
              "(", ")", "{", "}", "[", "]", "=", "*", "+", "#", "&", "|", "<", ">", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

    #transform text to lower cases
    text = text.casefold()

    #loop items of the text
    for item in text:

        #if deleted_items contain this item
        if item in deleted_items:

            #remove this item from the text 
            text = str(text).replace(item,"")

    return text


def get_file_words_list(path):
    """
    Process text in file, and store word in text in a list after removing symbols, numbers, repeatings and common words

    Parameters 
    ----------
    path : location of the file (str)

    Returns
    -------
    list_words : list of words in the file (list)  
    """


    #all words that can be removed from the text 
    words_to_delete = 'the a an i you he she it we they me you him her us them my your his her our their mine yours his hers ours theirs its im youre hes shes were theyre myself yourself himself herself itself ourselves yourselves themselves this that these those very few little much many lot most some any enough all both half either neither each every other another such  rather quite what which who when where why how aboard above about across after against along among around at before behind below beneath beside between beyond by despite down downwards during except excluding following for from in including inside into like near of off on onto over since to toward through throughout under underneath unlike until till up upon versus with within without next according ahead apart away because close out due regardless less more or back several and yes no not but too well youll ill none be have do say will want ive got weve was can cant wont as if go get would make know one time so am are is think take just could see now then still does takes says tells goes exact exactly precisely accurate accurately own been anyway doing never everything nothing even thus somehow together while unless being whole during sometime sometimes name please really yet again various full least most two first twice once'

    #build a list of this words
    words_to_delete = words_to_delete.split()

    try:
        #open file and read the text
        file = open(path, 'r')
        text = file.read()
        file.close()
    except UnicodeDecodeError:
        print("Impossible d'ouvrir ce fichier")

    #build list of words after removing the useless words
    text = replace_str(text)
    text = text.split()

    #list of the words
    list_words = list()

    #loop words of the text
    for word in text:
        
        #if this word repeat in the text
        if text.count(word) > 1 :
            #remove this occurence
            text.remove(word)

        #if size of the words bigger than 2 and this word not added yet in the new list and not contains in removed words
        elif not(word in words_to_delete) and (len(word) > 2) and not(word in list_words):

            #add word in the new list
            list_words.append(word)

    return list_words

def delete_repeated_words(list_words) :
    """
    Delete repeated words in the list 

    Parameters
    ----------
    list_words : list to process (list) 

    Returns
    -------
    list_words : modified list (list)
    """    
    
    #loop word il list 
    for word in list_words :

        #if occurence of this word bigger than one
        if list(list_words).count(word) > 1 :

            #remove the word from the list
            list(list_words).remove(word)

    return list_words        

def get_files_words_list():
    """
    In all archives process text in all the files, and store word in text in a list after removing symbols, 
    numbers, repeatings and common words

    Returns
    -------
    words : list of words in all the files (list) 
    """
    #buils list of all words
    words = list()

    #get list of all archives name
    archives = os.listdir(os.getcwd())

    #loop archives         
    for archive in archives :

        #if archive is not a directory
        if not os.path.isdir("./"+archive) : 
            archives.remove(archive)

        #if archive is a directory
        else :    

            #get all themes in the archive
            themes = os.listdir("./"+archive+"/sorted")

            #loop themes
            for theme in themes :
                
                #get files of every theme
                files = os.listdir("./"+archive+"/sorted/"+theme)

                #loop files
                for file in files :

                    #build list of words of every file
                    words.extend(get_file_words_list("./"+archive+"/sorted/"+theme+"/"+file))
    
    #remove repeated items
    words = delete_repeated_words(words)                

    return words      


def get_themes_frequency():
    """
    calculate frequency of all the words for every theme
    
    Returns
    -------
    frequencies : dictionary of frequency words for every theme (dict)
    """

    #dictionary of frequencies
    frequencies = dict()
    
    #all words of all files
    words = get_files_words_list()


    #get the path of archives
    archives = os.listdir(os.getcwd())

    #loop archives
    for archive in archives :


        #if archive is not a directory
        if not os.path.isdir("./"+archive) : 
            archives.remove(archive)

        #if archive is a directory
        else : 

            #build a dictionary of archive
            frequencies[archive] = dict()

            #get list of all themes 
            themes = os.listdir("./"+archive+"/sorted")

            #loop themes
            for theme in themes : 
                
                #number of words in the theme
                nb_words = 0
                
                #build a dictionary of themes
                frequencies[archive][theme] = dict()

                #get list of all files
                files = os.listdir("./"+archive+"/sorted/"+theme)
                
                #loop files
                for file in files :

                    try :
                        
                        #open file and read the text
                        file_op = open("./"+archive+"/sorted/"+theme+"/"+file,"r")
                        text = file_op.read()
                        file_op.close()

                    except UnicodeDecodeError:
                        print("Impossible d'ouvrir le fichier")

                    #transform text from string to list
                    text = text.split()

                    #icrement number of words in the theme
                    nb_words += len(text)

                    #loop words
                    for word in words :
                        
                        #if the word is already exists in the dictionary of themes
                        if word in frequencies :
                            frequencies[archive][theme][word] += 1 if text.count(word) == 0 else text.count(word)

                        #if the word doesn't exists in the dictionary of themes
                        else :
                            frequencies[archive][theme][word] = 1 if text.count(word) == 0 else text.count(word)

                #loop words of theme
                for word in frequencies[archive][theme]:
                    #devide number of occurence of word by number of words to get the frequancy 
                    frequencies[archive][theme][word] /= nb_words 

    return frequencies

def index_of_max(list):
    """
    Return the index of the maximum element of the list 

    Parameters
    ----------
    list : list to process (list)

    Returns 
    -------
    index : the index of the biggest value (int) 
    """    

    max = list[0]
    max_index = 0
    
    i = 0
    for element in list :
        if element > max : 
            max = element
            max_index = i
        
        i += 1

    return max_index    

def guess_theme_file(path,frequencies, themes):
    """
    Guessing the theme of the file

    Parameters
    ----------
    path : the position of the file (str)
    frequencies : dictionary of frequencies of words (dict)
    themes : list of themes of this archive (list)

    Returns 
    -------
    theme_final : the final theme after the guess (str) 

    """
    #transform path from string to list 
    path_list = str(path).split("/")

    #get words of this text in list 
    text = get_file_words_list(path)

    #list of probabilities
    proba_list = list() 

    #counter : counter of themes
    counter = 0

    #loop themes of current archive
    for theme in themes:

        #loop words of text
        for word in frequencies[path_list[1]][theme] :

            #if this word already exists in frequencies
            if word in text : 

                if len(proba_list) > counter :
                    proba_list[counter] += math.log( frequencies[path_list[1]][theme][word] )
                else :
                    proba_list.append( frequencies[path_list[1]][theme][word] )

            #if this word doesn't exists in frequencies
            else :
                
                if len(proba_list) > counter :
                    proba_list[counter] += math.log( 1 - frequencies[path_list[1]][theme][word] )
                else :
                    proba_list.append( 1 - frequencies[path_list[1]][theme][word] )

        #increment counter
        counter += 1

    #calulate the biggest probability in the proba_list
    theme_final = themes[ index_of_max(proba_list) ]

    return theme_final



def smart_sort_files(path):
    """
    Getting the theme of files in the path 

    Parameters 
    ----------
    path : position of the file

    """
    frequencies = get_themes_frequency()

    path_list = str(path).split("/")


    #get themes of this archive
    themes = os.listdir("./"+path_list[0]+"/sorted")

    #get list of files 
    files = os.listdir(path)

    #loops unsorted files
    for file in files:

        #gess the theme of the file 
        theme = guess_theme_file(path+"/"+file,frequencies,themes)

        #move the file to the right position in sorted directory and on the right themes
        os.rename(path+"/"+file,path_list[0]+"/sorted/"+theme+"/"+file)


############################## check_accuracy(path) functions #######################################################
def get_list_of_file_text(path, mode):
    """
    function return the test files into list 

    Parameters
    ----------
    path : the position of the file in the computer (str)
    mode : the mode of opening the file r/w/a (str)

    Returns
    -------
    lines_labels : list contains content of the file (list) 

    """
  
    labels_txt = open(path,mode)
    lines_labels = labels_txt.readlines
    labels_txt.close()
    
    return lines_labels

def lines_to_list(lines):
    """
    function transform list of strings into list of list separated by epaces

    Parameters
    ----------
    lines : list of strings before update(list)

    Retruns
    -------
    lines : list of lists after update (list)
    """
    i = 0
    for line in lines:
        lines[i] = str(line).split()
        i += 1

    return lines   

def find_them_in_file(theme,file_name,lines_file):
    """
    function boolean find the existance of an word in the file

    Parameters
    ----------
    theme : the word searched (str)
    file_name : the name of the file (str)
    lines_file : lines of the file (str)

    Returns
    -------
    result : True if the word is finded (bool) 

    """    
    #considire that theme is not finded 
    result = False

    #loop every line of the file
    for line in lines_file:

        #split the line 
        line = str(line).split()

        #if the name of the file was finded
        if line[0] == file_name :

            #get themes of this name file in this line 
            types = str(line[1]).split(".")

            #loop every theme
            for type in types :

                #if theme is finded correctly 
                if type ==theme :
                    
                    result = True

    return result   


def build_path_from_list(list):
    """
    building path from list of directions

    Paramaeters
    -----------
    list : list of words of the direction for path (list)

    Returns
    -------
    path : the final path (str)
    """        
    #initialisation the path 
    path = ""

    #loop words of the list 
    for word in list :
        #concatenate the word with the old path 
        path += str(word)+"/"

    return path              




def check_accuracy(path):
    """
    Function calculate the percentage of files countains in labels.txt if they classed correctly

    Parameters 
    ----------
    path : position of the file in the computer (str)

    Returns 
    -------
    percentage : the percentage of files classed correctly (float)
    """
    #transform path from string to list 
    path = str(path).split("/")

    #check if the path is not an empty string 
    if len(path) != 0 :

        #getting the files labels.txt
        lines_labels = get_list_of_file_text("./labels.txt","r")

        #transorm lines of labels.txt to list 
        lines_labels = lines_to_list(lines_labels)



        #if the path reprasent the directory sorted 
        if path[len(path)-1] == "sorted" :

            #nitialisation number of themes and number of percentages 
            nb_themes = 0
            sub_percentages = 0
            
            #go to the direction of the path 
            for direction in path :
                os.chdir("./" + direction)

            #get the diretories or themes of the current directory sorted
            themes = os.listdir(".")

            #looping themes
            for theme in themes :

                #increment number of themes
                nb_themes += 1

                #add percentage of the new theme
                sub_percentages += check_accuracy(build_path_from_list(path)+theme)

            percentage = sub_percentages / nb_themes
            return percentage


        #if the path represent the directory theme
        else :
            correct_files = 0
            
            #go to the direction of the path 
            for direction in path :
                os.chdir("./" + direction)

            #get the files of the current directory 
            files = os.listdir(".")

            #open the file labels.txt
            open_labels = open("","r")
            #read all line of the file 
            open_labels_lines = open_labels.readlines()

            #loop files in sorted directory 
            for file in files :
                
                #if name of the file exsists 
                if os.path.isfile("./"+file) :
                    
                    if find_them_in_file(os.getcwd(),file,open_labels_lines):
                        correct_files += 1


                #if name of the file doesn't exsists 
                else :
                    #print error
                    print("this name %s is not a file" % file)
            
            #close the file labels.txt
            open_labels.close()
            #calculate the percentage 
            percentage = correct_files / len(os.listdir(os.getcwd()))
            return percentage

    #if the path is an empty string     
    else :
        print("error : the string that you entered as a path is empty")    