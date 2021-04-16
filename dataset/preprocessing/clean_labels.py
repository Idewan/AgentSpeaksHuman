import csv
import json

"""
Clean labels goes through the origin labels.csv file and extracts only those that we want
to select. Only run once.

"""

if __name__ == "__main__":
    with open("photos_identities.json") as jf:
        data = json.load(jf)

    # Remove the images we do not use
    with open("labels.csv", 'w', newline='') as file:
        writer = csv.writer(file)

        with open("list_attr_celeba.txt", "r") as f:
            n = int(f.readline())
            headers = "n " + f.readline()
            c_headers = headers.split(" ")
            c_headers.pop(len(c_headers) - 1)

            writer.writerow(c_headers)

            for _ in range(n):
                l = f.readline()
                c_w = l[:10]
                if c_w in data:

                    c_l = [data[c_w]]
                    for i in range(11, len(l)):
                        if l[i] == "1" and l[i-1] == "-":
                            c_l.append(0)
                        elif l[i] == "1":
                            c_l.append(1)

                    writer.writerow(c_l)