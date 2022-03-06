from script import *

df = pd.read_csv('dataset.csv')
i = 0

#login into IG account
IL = instaloader.Instaloader(download_video_thumbnails=False, save_metadata=False)
IL.login('fabiofabione90', 'qwertyuiopas123')

while True:
    i += 1
    p = df.iloc[17]
    igLink = str(p['IG profile'])
    fbLink = str(p['fb profile'])
    twLink = str(p['Twitter profile'])
    print('\n\n' + str(i) + '   ' + igLink + '   ' + fbLink + '   ' + twLink + '\n')
    downloadSocials(igLink, IL, fbLink, twLink)
    if df.iloc[i]['IG profile'] == df.iloc[-1]['IG profile'] or i > 9:
        break
webdriver.close()

print('\nDownload complete')