import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--location", dest="location", default="local", help="choose location")
args = parser.parse_args()

print("Twoja lokalizacja to: {}".format(args.location))
