import argparse

parser = argparse.ArgumentParser(description='Get trip reports')
parser.add_argument('start', type=int)
# Parse command line arguments.
args = parser.parse_args()

f = open('trip_reports.html', 'w')

f.write('<html>')
f.write('<body><ul>')
for i in range(args.start, args.start + 100):
   f.write(f'<li><a href="https://ebird.org/tripreport/{i}" target="#blank">{i}</a></li>')
f.write('</ul></body')
f.write('</html>')
