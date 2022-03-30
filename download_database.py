from script import *

df = pd.read_csv('dataset.csv')
i = 1

#login into IG account
IL = instaloader.Instaloader(download_video_thumbnails=False, save_metadata=False)
IL.login('fabiofabione90', 'qwertyuiopas123')

while True:
    i += 1
    p = df.iloc[i]
    igLink = str(p['IG profile'])
    fbLink = str(p['fb profile'])
    twLink = str(p['Twitter profile'])
    name = str(p['Celebrity name'])
    print('\n\n' + str(i) + '   ' + name + '   ' + igLink + '   ' + fbLink + '   ' + twLink + '\n')
    downloadSocials(igLink, IL, fbLink, twLink, name)
    if df.iloc[i]['IG profile'] == df.iloc[-1]['IG profile']:
        break
webdriver.close()

print('\nDownload complete')