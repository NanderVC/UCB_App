'''---------------------------------------------------------------------------
-----------------Interactive Upper Confidence Bound Image App-----------------
---------------------------------------------------------------------------'''

'''This app presents the user with pictures of five different categories of
food: Vegetables, Dairy, Sweets, Meat and one pan dishes high in carbs. The
user can then indicate if they like the picture they are seeing. Based on this
choice, the Upper Confidence Interval for every cargeory is calculated and
the user is presented with categories they like more often than the ones they
don't like until one of the categories' picture library is emptied. A 
histogram is then shown with the user's preferenced choices. '''


#Doing the neccessary imports
import kivy 
import matplotlib.pyplot as plt
import math
import numpy as np
import os
import findstrings


kivy.require('1.11.1')

#We only really need the basic kivy imports, since we'll be doing all of the
#graphics in the .kv file
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty
from kivy.core.window import Window


class MyFloat(FloatLayout):
    
    def __init__(self):
        #Our float object will inherit the init method of the MyFloat class
        super(MyFloat, self).__init__()
    
        #This line uses the the importpictures method to import the path names
        #of all the png files the directory of the main script
        total = findstrings.importpictures()
        
        #Initializing all the variables we will need for the algorithm to work,
        #including a list containing a list of all the images the user is presented
        #with, the number of times a category of picture has been selected by user,
        #and the number of times a category has been presented to the user
        self.var_user = ''
        self.imglist = total
        self.choices = []
        #Change this path to the local path where this script is and choose any of the 
        #pictures
        self.img = r'C:\Users\HP\Documents\Python Scripts\GUIstuff\2\Broccoli.jpg'
        self.selected_cat = 1
        self.cat_presented = [0] * 5
        self.cat_sum = [0] * 5
        self.round = 1
        
    #Buttons intitalized that can be linked with the .kv file
    button1 = ObjectProperty(None)
    button2 = ObjectProperty(None)
    exit_button = ObjectProperty(None)
    
    
    def btn_like(self):
        self.var_user += 'yes'
        print(self.var_user)
    
        
    def btn_not_like(self):
        self.var_user += 'no'
        
    def exit_button(self):
        #remove histogram from folder to prevent future crash on starting app again
        os.remove('histogram.png')
        App.get_running_app().stop()
        Window.close()
     
    '''The UCB algorithm rewards a category by adding 1 to self.cat_sum every
    time the user hits the "like" button. The Upper confidence interval is then
    calculated by adding the confidence interval to the average reward over x
    number of rounds up to that point'''    
     
    def algorithm(self):
        max_upper_bound = 0
        reward = 0
        if self.var_user == 'yes':
            reward = 1
            self.choices.append(self.selected_cat)
        else:
            reward = 0
            
        self.var_user = ''
        
        self.cat_sum[self.selected_cat] = self.cat_sum[self.selected_cat] + reward
        self.cat_presented[self.selected_cat] = self.cat_presented[self.selected_cat] + 1
        
        #loops over all the categories to calculate averages, confidence intervals
        #and finally the upper bound.
        for j in range(5):
        
            if self.cat_presented[j] > 0:
                average = self.cat_sum[j]/self.cat_presented[j]
                confidence = math.sqrt((3/2)*math.log(self.round)/self.cat_presented[j])
                upper_bound = average + confidence
                
            else:
                upper_bound = 1e400
                
            
            if upper_bound > max_upper_bound:
                max_upper_bound = upper_bound
                self.selected_cat = j
                
        self.round += 1
        
        if len(self.imglist[self.selected_cat]) == 0:
            
            #Plots a histogram with the user's choices of preferred food
            plt.figure()
            plt.hist(self.choices)
            plt.xlim(0,5)
            plt.xticks([0,1,2,3,4], labels=["dairy","vegetables","meat","carbs", "sweets"])
            plt.savefig('histogram.png')
            
            self.img = 'histogram.png'
            
            self.button1.disabled = True
            self.button2.disabled = True
            
        else:
             
            self.img = self.imglist[self.selected_cat][0]
            self.imglist[self.selected_cat].remove(self.imglist[self.selected_cat][0])
        
        

#Build the actual app        
class MyApp(App):
    
    def build(self):
        return MyFloat()
            
    
if __name__ == '__main__':
    
    MyApp().run()
    
  