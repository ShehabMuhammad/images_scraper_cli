import os, re, requests, random, sys

dic = {}
for i in sys.argv[1:]:
    dic[i.split("=")[0]] = i.split("=")[1];

url = dic["--url"];
deep_scraping = dic["--deep_scraping"]
out_dir = dic["--o"] or ""
count = 0;
cache = [];

def scrape(url, deep_scraping=False):
    global count;
    try:
        Archive = requests.get(url);
        if url not in cache:
            cache.append(url);
        else:
            return;
    except Exception as e:
        print("An Error occured during scraping the main url, The Error is" + str(e));
        return;
    html = Archive.text
    Links = re.findall('(https?://[^\s$"\']+)' , html)
    for i in Links:
        count += 1
        print(f"Now count is {count}")
        if i.endswith(".jpg") or i.endswith(".png"):
            try:
                
                if i not in cache:
                    img = requests.get(i);
                    cache.append(i);
                else:
                    continue;
            except Exception as e:
                print(f"Was not able to get {i}, Moving on..");
                continue;
            file = open(out_dir +"/" + "file_num"+str(count)+"_"+str(random.random()) + ".jpg" ,'wb');
            file.write(img.content);
        else:
            if deep_scraping and i not in cache:
                scrape(i, deep_scraping=False);   

if __name__ == '__main__':
    scrape(url, deep_scraping)
