import argparse

parser = argparse.ArgumentParser(description='Get birdlife regions')
parser.add_argument('start', type=int)
# Parse command line arguments.
args = parser.parse_args()

f = open('bird_life.html', 'w')

f.write('<html>')
f.write('<body><ul>')
for i in range(args.start, args.start + 100):
   f.write(f'<li><a href="https://ebird.org/region/BIRDLIFE_{i}/hotspots?yr=all&m=null" target="#blank">{i}</a></li>')
f.write('</ul></body')
f.write('</html>')
