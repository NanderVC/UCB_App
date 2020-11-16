#Function that can be used to find all the png or jpg image files in a folder

def importpictures():

    picturepaths = [[],[],[],[],[]] 
    
    import os
    
    #Editthe path to the path where this file and the main scipt are located
    for subdir, dirs, files in os.walk(r'C:\Users\HP\Documents\Python Scripts\GUIstuff'):
        for file in files: 
            if file.endswith('.png') or file.endswith('.jpg'):
                path = os.path.join(subdir, file)
                category = int(subdir[-1]) -1
                picturepaths[category].append(path)
                
    
    return picturepaths


total = importpictures()
print(total)