from BeautifulSoup import BeautifulSoup
import urllib

#CDM

def download_images(url):
    page = urllib.urlopen(url).read()
    folder_to_save = 'teacher_pictures/'
    soup = BeautifulSoup(page)
    images = []

    temp_url = '/'.join(url.split('/')[:3])

    for item in soup.findAll('img',{'class':'facImage'}):

        temp_image_link = item['src'].encode("ascii", "ignore")
        if  'http' not in temp_image_link:
            temp_image_link = temp_url + temp_image_link
        temp_teacher_name = item['alt'].replace('&nbsp;',' ')
        images.append([temp_image_link,temp_teacher_name])

    for i in images:
        file_name = i[1].lower().split()

        if '.' in file_name[0]:
            file_name = file_name[1] +'-'+ file_name[-1]
        else:
            file_name = file_name[0] +'-'+ file_name[-1]
        
        urllib.urlretrieve(i[0], folder_to_save + file_name)

def main():
    url = 'http://www.cdm.depaul.edu/about/Pages/People/Faculty.aspx?ftype=&selectedareataught=&lastnamefilter=ALL&level'
    download_images(url)

if __name__ == '__main__':
    main()
