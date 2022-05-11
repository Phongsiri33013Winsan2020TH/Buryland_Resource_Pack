import os
import re
import sys


print("=================================")
print("WitalandMC sounds.json generator. | Original code by Bentroen.")
print("=================================\n")


if sys.version_info[0] < 3:
	raise Exception("This script requires Python 3.")


while True:
	path = input("フォルダーの部分入力：")
	if not os.path.isdir(path):
		print("これはフォルダーではない。")
		continue
	else:
		if not os.path.basename(path).strip() == "sounds":
			print("ERROR: The provided path does not point to a 'sounds' folder.\n")
			continue
		else:
			break


file_count = 0
sounds = []

for dir, subdirs, files in os.walk(path):
	for f in files:
		file_count += 1
		if f[-4:] == ".ogg":
			file_name = os.path.join(dir[(len(dir)-len(path)-1)*-1:], f[:-4]).replace("\\", ".")
			sounds.append(file_name)
		if file_count >= 1500:
			raise Exception("File count exceeded safe limit.")


json_path = os.path.join(os.path.split(path)[0], "sounds.json")
json = open(json_path, 'w')
json.write("{")

last_prefix = ""
first_event = True

for i,f in enumerate(sounds):
	print("{}/{}: {}にしています。".format(i+1, len(sounds), f))
	if f[-1:].isdigit():
		split_name = re.findall(r'(\D+)(\d+)', f)[0]
		prefix = split_name[0]
	else:
		prefix = f
		
	if not last_prefix == prefix:
		if not first_event:
			json.write('\n\t\t]')
			json.write('\n\t},')
		first_event = False
		json.write('\n\t"{}": {{'.format(prefix))
		json.write('\n\t\t"sounds": [')
	else:
		json.write(',')
	json.write('\n\t\t\t"{}"'.format(f.replace(".", "/")))
	last_prefix = prefix

json.write('\n\t\t]')
json.write('\n\t}')
json.write('\n}')
json.close()

print("\n{} files generated.".format(len(sounds)))
os.system("pause")