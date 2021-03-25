from PIL import Image
import numpy as np
import os
import csv

#Generating barcodes for each image
class barcodeGenerator:
    def __init__(self, imgarray):
        self.imgarray = imgarray

    #Projection 1 of image (0 deg)
    def th1(self):
        rowsums = []
        thresh1 = []

        rowsums = np.sum(imgarray, 1)
        avg = sum(rowsums)/len(rowsums)

        for i in range(len(rowsums)):
            if(rowsums[i] <= avg):
                thresh1.append(0)
            else:
                thresh1.append(1)

        return thresh1

    #Projection 2 of image (45 deg)
    def th2(self):
        thresh2 = []
        right = [np.sum(np.diag(imgarray, d))
                 for d in range(len(imgarray) - 1, -len(imgarray), -1)]
        avg = sum(right)/len(right)

        for i in range(len(right)):
            if(right[i] <= avg):
                thresh2.append(0)
            else:
                thresh2.append(1)
        return thresh2

    #Projection 3 of image (90 deg)
    def th3(self):
        rowsums = []
        thresh3 = []

        rowsums = np.sum(imgarray, 0)
        avg = sum(rowsums)/len(rowsums)

        for i in range(len(rowsums)):
            if(rowsums[i] <= avg):
                thresh3.append(0)
            else:
                thresh3.append(1)

        return thresh3

    #Projection 4 of image (135 deg)
    def th4(self):
        thresh4 = []
        left = [np.sum(np.diag(np.fliplr(imgarray), d))
                for d in range(len(imgarray) - 1, -len(imgarray), -1)]
        avg = sum(left)/len(left)

        for i in range(len(left)):
            if(left[i] <= avg):
                thresh4.append(0)
            else:
                thresh4.append(1)
        return thresh4

    #Combine all projections to one barcode
    def concatenate(self):
        newBarcode = self.th1()+self.th2()+self.th3()+self.th4()
        return newBarcode

#Searching for similar images
class searchAlgorithm:

    def __init__(self, userInput, fileandBarcode):
        self.fileLocationHam = []  
        self.userInput = userInput
        self.fileandBarcode = fileandBarcode

    #Calculates Hamming distance of each image
    def ham(self, x, y):

        hd = 0
        for i in range(len(x)):
            digit1, digit2 = int(x[i]), int(y[i])
            if digit1 != digit2:
                hd += 1
        return hd

    #Calculates accuracy of top nine closest images from Hamming distance
    def accuracy(self,sortArray):
        filename = str(sortArray[0][1])
        numComp = int(filename[24])
        counter = 0
        for i in range(10):
            tempName = str(sortArray[i][1])
            temp = int(tempName[24])
            if numComp == temp:
                counter+=1

        return (counter-1)/9

    #Comparing searched image with all other images in database
    def search(self):
        filelocation = ""
        for i in range(len(fileandBarcode)):
            
            filelocation = fileandBarcode[i][0]
            hd = self.ham(userInput, str(fileandBarcode[i][1]).replace(
                ",", "").replace(" ", "").replace("[", "").replace("]", ""))
            self.fileLocationHam.append((hd, filelocation))
            

        sortedfileLocationHam = sorted(self.fileLocationHam)
        print("\nHamming distance and file location")
        for i in range(10):
            print(sortedfileLocationHam[i])
        return self.accuracy(sortedfileLocationHam)

if __name__ == "__main__":

    filepathList = []
    barcodeList = []

    #Loading each image from database
    for sub, dirs, files in os.walk(r"..\barcodeScan\MNIST_DS"):
        for filename in files:
            filepath = sub+os.sep+filename

            if filepath.endswith(".jpg"):
                filepathList.append(filepath)
    
    #Assigning a barcode to each image in database
    for i in range(len(filepathList)):

        image = Image.open(filepathList[i])
        imgarray = np.asarray(image)
        barcode = barcodeGenerator(image)
        barcodeList.append(barcode.concatenate())
        
    #List stores image file path and its barcode
    fileandBarcode = list(zip(filepathList, barcodeList))

    #Writing fileandBarcode to csv
    with open('filesandbarcode.csv','w') as result:
        w = csv.writer(result,dialect='excel')
        w.writerows(fileandBarcode)  

    #Getting user's barcode
    userInput = input("Enter a barcode: ")
    userInput = userInput.replace(" ", "").replace(
        ",", "").replace("[", "").replace("]", "").replace('"','')

    #Performing comparison
    searching = searchAlgorithm(userInput, fileandBarcode)
    
    print("The hit accuracy for the closest 9 results was: ",
        "{:.0%}".format(searching.search()))
    
    


