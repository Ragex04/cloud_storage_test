import png
import binascii
import math
import argparse
import sys
'''

So this program takes a file or text as an argument and either encodes/decodes data to/from a png image
made from 16 bit colors.

Ouputs a PNG from a file
pencode.py output.png --file2png /home/directory/file

Outputs a PNG from a text string
pencode.py output.png --txt2png "TESTTESTTESTTEST"

Outputs text from an encoded png
pencode.py input.png --png2txt

Outputs a file from a decoded imaGE
pencode.py input.png --png2file file

This program encoded:
http://i.imgur.com/cfHpDjg.png

'''


class pngencode(object):
    #  Class attribute; Global attribute between all classes
    chex = {'0': (0, 0, 0),  # c(olor)hex  # White
            '1': (255, 255, 255),  # Black
            '2': (255, 0, 0),  # Red
            '3': (0, 255, 0),  # Blue
            '4': (0, 0, 255),  # Green
            '5': (255, 255, 0),  # Yellow
            '6': (0, 255, 255),  # Cyan
            '7': (255, 0, 255),  # Magenta
            '8': (192, 192, 192),  # Silver
            '9': (128, 128, 128), # Gray
            'A': (128, 0, 0),  # Maroon
            'B': (128, 128, 0),  # Olive
            'C': (0, 128, 0),  # Green
            'D': (128, 0, 128),  # Purple
            'E': (0, 128, 128),  # Teal
            'F': (0, 0, 128),  # Navy Blue
            'X': (80, 80, 80)  # NULL gray
            }

    def __init__(self, image):
        self.image = image  # Instance attribute
        pass

    def file_to_png(self, file_to_encode):
        read_stream = open(file_to_encode, 'rb')
        hex_file_data = self.bin_to_hex(read_stream.read())
        rgb_file_data = self.hex_to_rgb(hex_file_data)
        self.write_png(rgb_file_data, self.image)
        return 0

    def text_to_png(self, text):
        hex_data = self.ascii_to_hex(text)
        rgb_data = self.hex_to_rgb(hex_data)
        self.write_png(rgb_data, self.image)
        pass

    def png_to_text(self):
        image_pixels = self.read_to_rgb(self.image)
        hex_data = self.rgb_to_hex(image_pixels)
        text = self.hex_to_ascii(hex_data)
        return text

    def png_to_file(self, outputfile):
        outputfile_stream = open(outputfile, 'wb')
        image_pixels = self.read_to_rgb(self.image)
        hex_data = self.rgb_to_hex(image_pixels)
        data = self.hex_to_bin(hex_data)
        outputfile_stream.write(data)
        pass

    def write_png(self, rgb_data, image):

        length = math.ceil(math.sqrt(len(rgb_data)/3))
        empty = int(length ** 2 - (len(rgb_data) / 3))
        for emptypixel in range(empty):
            for rgb_value in self.chex['X']:
                rgb_data.append(rgb_value)
        #  So, this is what they call magic math *Actually it took me way too long to
        #  Figure this out, but here it is explained*
        #  So, in a regular square, both sides are the same
        #  And we find the area of a square/rectangle by multiplying the sides.
        #  So, since we want a perfect regular square, we want the total area, in pixels
        #  To be slightly less than that of the total number of hexadecimal digits.
        #  So, if you take the length of the data supplied, and divide it by three
        #  (Since each pixel has a red, blue, and green value, and this function takes just a list of values)
        #  You get the exact numbers of pixels in the message.
        #  But we need to turn the message into a square, so we root the total pixels of the message
        #  And we get out side length as a float. But, you cant have 1/2 or 2/3's of a pixel
        #  It has to be a whole number, so math.ceil() rounds up to the next whole number, so now
        #  We have a square, with an incomplete area. So, we square the length of our image
        #  And subtract our messages pixel length from that, to get the number of pixels that need to be filled
        #  And fill them with our 'X' character aka NULL.
        #  And it works.
        write_stream = open(image, 'wb')  # Opens file as write-binary stream mode
        png_write = png.Writer(length, length)  # Creates a Writer instance with height, width

        # Pypng likes its pixel data kinda weird, this is how it requires it
        # 4x4 image
        # p = [ (r, g, b, r, g, b, r, g, b, r, g, b),
        #       (r, g, b, r, g, b, r, g, b, r, g, b),
        #       (r, g, b, r, g, b, r, g, b, r, g, b),
        #       (r, g, b, r, g, b, r, g, b, r, g, b)
        #       ]
        # It likes each column in a tuple, nested in a list. Basically.

        pixel_column = []
        image_pixels = []
        for value in rgb_data:
            pixel_column.append(value)
            if len(pixel_column) == length*3:  # since each pixel takes 3 values
                image_pixels.append(tuple(pixel_column))  # Appends a tuple(aka column) to the final image
                pixel_column = []  # Resets column

        png_write.write(write_stream, image_pixels)  # Writes the image to the write_stream
        write_stream.close()
        #  with the image_pixels data
        return 0  # Should probably think of something better to return.

    def read_to_rgb(self, image):
        # Returns a straight list of rgb values
        # [r, g, b, r, g, b, r, ....]
        image_pixels = []  # Creates an empty list to store values
        image_stream = open(image, 'rb')  # Open image as file object in read-binary mode
        png_image_stream = png.Reader(file=image_stream)  # Create a Reader() instance
        for pixel in png_image_stream.read_flat()[2]:  # Grab individual pixel rgb value from read flat
            #  BEWARE!! read_flat reads whole image into memory. No matter size. Could take hella long.
            image_pixels.append(pixel)
        return image_pixels

    def rgb_to_hex(self, rgb_data):
        # Returns a string of hex values.
        rgb_tuple = []
        tmp = []
        hexlist = []
        for rgbvalue in rgb_data:
            tmp.append(rgbvalue)
            if len(tmp) == 3:  # Each pixel has three rgb values
                rgb_tuple.append(tuple(tmp))  # turn each pixel worth of data into a tuple
                # And append it to a list
                tmp = []
        for pixel in rgb_tuple:
            hexbyte = list(self.chex.keys())[list(self.chex.values()).index(pixel)]  # Ugly, but it gets a dict key
            # Based on a given value
            if hexbyte == 'X':  # Ignore end padding, aka 'Nulls'
                pass
            else:
                hexlist.append(hexbyte)  # Append hex byte to list
        hex_string = ''.join(hexlist)  # Change list to string
        return hex_string

    def hex_to_rgb(self, hex_data):
        # Returns a list of rgb values.
        rgb_list = []
        hex_data = hex_data.upper()  # Make hex data uppercase, so that it correctly matches chex keys
        for byte in hex_data:
            for value in self.chex[byte]:
                rgb_list.append(value)  # Appends the tuple of the matching hex value to a list
        return rgb_list

    @staticmethod  # Doesn't pass the 'self' to class. PEP8 thing.
    def ascii_to_hex(text_data):
        return binascii.b2a_hex(str.encode(text_data)).decode("utf-8")

    @staticmethod  # Doesn't actually seem to make much of a difference.
    def hex_to_ascii(hex_data):
        return binascii.a2b_hex(str.encode(hex_data)).decode("utf-8")
    @staticmethod
    def hex_to_bin(hex_data):
        return binascii.a2b_hex(str.encode(hex_data))

    @staticmethod
    def bin_to_hex(bin_data):
        return binascii.b2a_hex(bin_data).decode('utf-8')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Encodes/decodes data to/from viewable png files', epilog="This program takes data, turns it into hexadecimal, and then into 16bit rgb colors, and to decode, it does the reverse. Requires at least one optional argument.")
    parser.add_argument('image', type=str, help='The image to create or decode')
    parser.add_argument('--png2file', type=str, action='store', help='Converts an encoded image to file')
    parser.add_argument('--png2txt', action='store_true', default=False, help='Decodes and ouputs image text')
    parser.add_argument('--file2png', type=str, action='store', help='Encodes a file into a png')
    parser.add_argument('--txt2png', type=str, action='store', help='Encodes a text argument into an image')
    args = parser.parse_args()
    x = pngencode(args.image)

    if args.png2txt == True:
        print(x.png_to_text())
    elif args.png2file != None:
        x.png_to_file(args.png2file)
    elif args.file2png != None:
        x.file_to_png(args.file2png)
    elif args.txt2png != None:
        x.text_to_png(args.txt2png)
    else:
        print("{} Requires at least one optional argument.\nSee {} -h for details.".format(sys.argv[0], sys.argv[0]))
