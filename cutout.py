import os
import subprocess


class Cutout:
    def __init__(self, gmicPath, filterPath, imagesPath, outputPath):
        self.executable = gmicPath
        self.filter = filterPath
        self.folder = imagesPath
        self.out = outputPath

    def runCutout(self):
        for filename in os.listdir(self.folder):
            inputPath = os.path.join(self.folder, filename)
            outputPath = os.path.join(self.out, filename)

            subprocess.call([
                self.executable,
                self.filter,
                "-cutout",
                inputPath + "," + outputPath + ".jpg"
            ])


