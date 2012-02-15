import os, sys
import Image

def convert_to_jpeg():
    for infile in sys.argv[1:]:
        outfile = os.path.splitext(infile)[0] + ".jpeg"
        if infile != outfile:
            try:
                Image.open(infile).save(outfile)
            except IOError:
                print "Cannot convert", infile

def create_thumbnail(infile):
    outfile = os.path.splitext(infile)[0] + '.jpeg'
    if infile != outfile:
        try:
            im = Image.open(infile)
            im.thumbnail((128, 128))
            im.save(outfile, "JPEG")
        except IOError:
            print "Cannot convert", infile

def main():
    for infile in sys.argv[1:]:
        create_thumbnail(infile)

if __name__ == "__main__":
    main()




