import extractor
import cutout


def main():
    e = extractor.Extractor()
    # e.loadFilesToExtract() # extracts layers into images
    # e.generate(20)
    c = cutout.Cutout("E:\\Projects\\2019\\The Game\\steam\\generator\\gmic\\gmic.exe",
                      "E:\\Projects\\2019\\The Game\\steam\\generator\\skript\\output\\product\\myCutout.gmic",
                      "E:\\Projects\\output",
                      "E:\\Projects\\output\\out")
    c.runCutout()


if __name__ == '__main__':
    main()
