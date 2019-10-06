from psd_tools import PSDImage
from PIL import Image, ImageSequence
import os, time, random


class Extractor:
    def __init__(self, folder="faces", outputFolder="output"):
        self.folder = folder
        self.outputFolder = outputFolder
        self.faces = None

    def loadFilesToExtract(self):
        self.faces = os.listdir(self.folder)
        for face in self.faces:
            psdImage = PSDImage.open(os.path.join(self.folder, face))
            self.extractLayers(psdImage, face)

    def extractLayers(self, psdFile, filename):
        for index, layer in enumerate(psdFile):
            outputImage = Image.new("RGBA", layer.as_PIL().size)
            outputImage.paste(layer.as_PIL())

            # create folder for the facial feature if not exists
            if not os.path.exists(os.path.join(self.outputFolder, layer.name)):
                os.makedirs(os.path.join(self.outputFolder, layer.name))
                # save to distinct folder
            outputImage.save(os.path.join(self.outputFolder, layer.name, filename + ".png"))

    def getRandomFeature(self, name):
        return os.path.join(self.outputFolder, name, random.choice(os.listdir(os.path.join(self.outputFolder, name))))

    def findPsdLayerByName(self, psd, name):
        try:
            return [layer for layer in psd if layer.name.startswith(name)][0]
        except:
            raise Exception("No layer by name " + name)

    def resize(self, layer, image, finalImage):
        offset = (layer.bbox[0], layer.bbox[1])  # left top
        resizeTo = (layer.bbox[2] - layer.bbox[0], layer.bbox[3] - layer.bbox[1])
        resized = image.resize(resizeTo, Image.ANTIALIAS)
        finalImage.paste(resized, offset, mask=resized)  # mask fixes blending
        return finalImage

    def combinator(self):
        baseFacePsd = PSDImage.open(self.getRandomFeature("base"))
        eyesImage = Image.open(self.getRandomFeature("eyes"), "r")
        noseMouthImage = Image.open(self.getRandomFeature("nose_mouth"), "r")

        baseFaceImage = self.findPsdLayerByName(baseFacePsd, "smudged").as_PIL()
        noseMouthLayer = self.findPsdLayerByName(baseFacePsd, "nose_mouth")
        eyesLayer = self.findPsdLayerByName(baseFacePsd, "eyes")

        finaleImage = Image.new("RGBA", baseFaceImage.size)
        finaleImage = self.resize(eyesLayer, eyesImage, finaleImage)  # eyes
        finaleImage = self.resize(noseMouthLayer, noseMouthImage, finaleImage)  # nose and mouth
        try:  # hair overlay
            hairOverlayLayer = self.findPsdLayerByName(baseFacePsd, "hair_overlay")
            hairImage = hairOverlayLayer.as_PIL()
            finaleImage = self.resize(hairOverlayLayer, hairImage, finaleImage)
        except Exception:
            pass

        finaleImage = Image.alpha_composite(baseFaceImage, finaleImage)
        finaleImage.save(os.path.join(self.outputFolder, "product", "output_" + str(time.time()) + ".png"))

    def generate(self, n):
        for i in range(0, n):
            self.combinator()
