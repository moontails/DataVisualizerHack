import os
import json

def split_converter(base_path):
    files = os.listdir(base_path)
    for file in files:
        print file
        infile = open(base_path + file, 'r')
        outfile = open(file + '.json', 'w')

        template = { "create": { "_index": "reviews", "_type": "doc"} }

        for line in infile:
            doc = json.loads(line.strip())
            json.dump(template,outfile)
            outfile.write("\n")

            json.dump(doc,outfile)
            outfile.write('\n')

        infile.close()
        outfile.close()

def converter(filename):
    infile = open(filename, 'r')
    outfile = open('business.json', 'w')

    template = { "create": { "_index": "business", "_type": "doc"} }

    for line in infile:
        doc = json.loads(line.strip())

        json.dump(template,outfile)
        outfile.write("\n")

        json.dump(doc,outfile)
        outfile.write('\n')

    infile.close()
    outfile.close()

if __name__ == "__main__":
    #split_converter('yelp_dataset/split/')

    converter('yelp_dataset/business.json')
