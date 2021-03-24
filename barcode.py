from PIL import Image
import numpy as np
import os


class barcodeGenerator:
    def __init__(self, imgarray):
        self.imgarray = imgarray

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

    def concatenate(self):
        newBarcode = self.th1()+self.th2()+self.th3()+self.th4()
        return newBarcode


class searchAlgorithm:

    def __init__(self, userInput, fileandBarcode):
        self.sharyarWithHam = []  # Sharyar eating black forest ham
        self.userInput = userInput
        self.fileandBarcode = fileandBarcode

    def ham(self, x, y):

        hd = 0
        for i in range(len(x)):
            digit1, digit2 = int(x[i]), int(y[i])
            if digit1 != digit2:
                hd += 1
        return hd

    def search(self):
        filelocation = ""
        for i in range(len(fileandBarcode)):
            # if str(fileandBarcode[i][1]).replace(",", "").replace(" ", "").replace("[", "").replace("]", "") == userInput:
            filelocation = fileandBarcode[i][0]
            hd = self.ham(userInput, str(fileandBarcode[i][1]).replace(
                ",", "").replace(" ", "").replace("[", "").replace("]", ""))
            self.sharyarWithHam.append((hd, filelocation))
            # print(type(fileandBarcode[i][1]))

        sortedSharyarWithHam = sorted(self.sharyarWithHam)
        for i in range(10):
            print(sortedSharyarWithHam[i])
        # print(sortedSharyarWithHam)
        # print(sortedSharyarWithHam[1][1])
        # return filelocation


if __name__ == "__main__":

    filepathList = []
    barcodeList = []

    for sub, dirs, files in os.walk(r"..\barcodeScan\MNIST_DS"):
        for filename in files:
            filepath = sub+os.sep+filename

            if filepath.endswith(".jpg"):
                filepathList.append(filepath)

    for i in range(len(filepathList)):

        image = Image.open(filepathList[i])
        imgarray = np.asarray(image)
        barcode = barcodeGenerator(image)
        barcodeList.append(barcode.concatenate())

    fileandBarcode = list(zip(filepathList, barcodeList))

    print(fileandBarcode)

    userInput = input("Enter a barcode: ")
    userInput = userInput.replace(" ", "").replace(",", "")
    print(userInput)

    searching = searchAlgorithm(userInput, fileandBarcode)
    # print(searching.ham("00100", "11011"))
    searching.search()


