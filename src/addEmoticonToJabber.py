import sys

from PIL import Image

"""
Global variables
"""
img1Size = 20
img2Size = 40
img3Size = 60

img2Suffix = '@2x'
img3Suffix = '@3x'


def main(argv):
    """
    This script automatically adds the given img/emoji to your installed Cisco Jabber client.
    The path to the Cisco Jabber installation is defined in the script.properties file.
    
    Tested in Windows, it may not work properly in GNU/Linux or MacOSX systems.

    Usage: python addEmoticonToJabber.py path_to_img
    """

    # Read properties
    with open('script.properties') as file:
        pathToJabber = file.readlines()[0].split('=')[1]
        print pathToJabber

    # Read the image
    im = Image.open(argv[0])
    imgName = argv[0].split('.')[0]

    im1 = im.resize((img1Size, img1Size), Image.ANTIALIAS)
    im2 = im.resize((img2Size, img2Size), Image.ANTIALIAS)
    im3 = im.resize((img3Size, img3Size), Image.ANTIALIAS)

    # Read the xml file
    order = 0

    with open(pathToJabber + 'Emoticons\emoticonDefs.xml') as file:
        lines = file.readlines()
        newLines = lines[:-1]
        for line in lines:
            if '<emoticon' in line:
                lineProperties = line.split(' ')
                for pr in lineProperties:
                    if 'order' in pr:
                        order = int(pr.split('"')[1])   # Take last order id

                    if 'defaultKey' in pr:
                        key = pr.split('"')[1]  # Avoid duplicated images
                        if imgName == key.replace('(', '').replace(')', ''):
                            raise Exception("Image already loaded")

    thefile = open(pathToJabber + 'Emoticons\emoticonDefs.xml', 'w')

    newLines.append('\t<emoticon defaultKey="(' + imgName + ')" image="' + imgName + '.png" order="' + str(order + 1)
                    + '" text="' + imgName + '" hidden="false" clickToCall="true">\n')
    newLines.append('\t</emoticon>\n')
    newLines.append('</emoticons>')

    # Write new xml file
    for line in newLines:
        if not line.strip(): continue  # Avoid empty lines
        thefile.write(line)
    thefile.close()

    # Write new emoticons
    im1.save(pathToJabber + 'Emoticons\\' + imgName + '.png')
    im2.save(pathToJabber + 'Emoticons\\' + imgName + img2Suffix + '.png')
    im3.save(pathToJabber + 'Emoticons\\' + imgName + img3Suffix + '.png')


if __name__ == "__main__":
    main(sys.argv[1:])
