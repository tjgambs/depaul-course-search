from BeautifulSoup import BeautifulSoup
import urllib
import download_cdm_pictures

#Works for Buisiness
#Communications
#Education
#Law
#Liberal Arts
#Music
#New Learning
#Science and Health


def download_images(url,_tag,_class):
    page = urllib.urlopen(url).read()
    folder_to_save = 'teacher_pictures/'
    soup = BeautifulSoup(page)
    images = []

    temp_url = '/'.join(url.split('/')[:3])

    for item in soup.findAll(_tag,_class):
        temp_image_link = item.find('img')['src'].encode("ascii", "ignore")
        if  'http' not in temp_image_link:
            temp_image_link = temp_url + temp_image_link
        temp_teacher_name = item.find('h3').text.replace('&nbsp;',' ')
        images.append([temp_image_link,temp_teacher_name])

    for i in images:
        file_name = i[1].lower().split()

        if '.' in file_name[0]:
            file_name = file_name[1] +'-'+ file_name[-1]
        else:
            file_name = file_name[0] +'-'+ file_name[-1]
        urllib.urlretrieve(i[0], folder_to_save+file_name)

def main():
    urls = [['http://driehaus.depaul.edu/faculty-and-staff/faculty/Pages/default.aspx','div',{'class':'member-portrait grid_4'}],
            ['http://communication.depaul.edu/faculty-and-staff/faculty/Pages/default.aspx','div',{'class':'panel-obj'}],
            ['http://education.depaul.edu/faculty-and-staff/faculty/Pages/default.aspx','div',{'class':'panel-obj'}],
            ['http://law.depaul.edu/faculty-and-staff/faculty-a-z/Pages/default.aspx','div',{'class':'panel-obj'}],
            ['http://las.depaul.edu/faculty-and-staff/pages/faculty-a-z-listing.aspx','div',{'class':'panel-obj'}],
            ['http://music.depaul.edu/faculty-staff/faculty-a-z/Pages/default.aspx','div',{'class':'panel-obj'}],
            ['http://snl.depaul.edu/faculty-and-staff/faculty-a-z/Pages/default.aspx','div',{'class':'panel-obj'}],
            ['http://csh.depaul.edu/faculty-staff/faculty-a-z/pages/default.aspx','div',{'class':'panel-obj'}]]

    for url in urls:
        download_images(url[0],url[1],url[2])
    download_cdm_pictures.main()

if __name__ == '__main__':
    main()
