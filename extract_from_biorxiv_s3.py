import os
import zipfile

done = open("./progress.txt", "w")

for i, d in enumerate(os.scandir("biorxiv-full-2020/")):
    fn = d.name
    fp = d.path
    with zipfile.ZipFile(fp) as zf:
        desired = [x for x in zf.namelist() if x.startswith('content/') and x.endswith('.xml')]
        if len(desired) == 0:
            print("(Skip) no xml file", fn)
            continue
        if len(desired) > 1:
            print("(Skip) more than one content/*.xml file: ", fn)
            continue

        zf.extract(desired[0], path="biorxiv-extracted/" + fn)

        done.write(fn + '\t' + desired[0] + '\n')

    if i % 100 == 0:
        print('.', end='')

done.close()
