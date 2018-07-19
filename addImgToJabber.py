import sys
from PIL import Image

"""
Global variables
"""
size1 = 20
size2 = 40
size3 = 60

size2Name = '@2x'
size3Name = '@3x'

def main(argv):
    """
    This script automatically adds the given img/emoji to your installed Cisco Jabber client
    'C:\Program Files (x86)\Cisco Systems\Cisco Jabber' is assumed to be the path to the Cisco Jabber installation.

    Usage: python addImgToJabber.py path_to_img
    """

    # Read the image
    im = Image.open(argv[0])
    imgName = argv[0].replace('.jpg', '')
    imgName = imgName.replace('.png', '')
    outputImg = argv[0].replace('jpg', 'png')

    im1 = im.resize((size1, size1), Image.ANTIALIAS)
    im2 = im.resize((size2, size2), Image.ANTIALIAS)
    im3 = im.resize((size3, size3), Image.ANTIALIAS)

    # Read the xml file
    with open('C:\Program Files (x86)\Cisco Systems\Cisco Jabber\Emoticons\emoticonDefs.xml') as file:
        lines = file.readlines()
        newLines = lines[:-1]
        for line in lines:
            if '<emoticon' in line:
                lineProperties = line.split(' ')
                for pr in lineProperties:
                    if 'order' in pr:
                        order = int(pr.split('"')[1])
                        lastId = order
                    if 'defaultKey' in pr:
                        key = pr.split('"')[1]
                        if imgName == key.replace('(', '').replace(')', ''):
                            raise Exception("Image already loaded")

    thefile = open('C:\Program Files (x86)\Cisco Systems\Cisco Jabber\Emoticons\emoticonDefs.xml', 'w')

    newLines.append('\t<emoticon defaultKey="(' + imgName + ')" image="' + imgName + '.png" order="' + str(order + 1) + '" text="' + imgName + '" hidden="false" clickToCall="true">\n')
    newLines.append('\t</emoticon>\n')
    newLines.append('</emoticons>')

    # Write new xml file
    for item in newLines:
        if not line.strip(): continue
        thefile.write(item)
    thefile.close()

    # Write new iamges
    im1.save('C:\Program Files (x86)\Cisco Systems\Cisco Jabber\Emoticons\\' + imgName + '.png')
    im2.save('C:\Program Files (x86)\Cisco Systems\Cisco Jabber\Emoticons\\' + imgName + size2Name + '.png')
    im3.save('C:\Program Files (x86)\Cisco Systems\Cisco Jabber\Emoticons\\' + imgName + size3Name  +'.png')


if __name__ == "__main__":
    main(sys.argv[1:])
