import PySimpleGUI as sg
from PIL import Image

import LocalBooru as lb


max_size = (800, 800)

layout = [
    [sg.Text('Search the database and display results')],
    [sg.Input(key='-IN-')],
    [sg.Button('Enter'), sg.Exit()],
    [sg.Image(filename='data/localbooru_bg.gif', key='im1', visible=True, enable_events=True)]
]

window = sg.Window('LocalBooru', layout)

while True:
    event, values = window.Read()
    print(event, values)

    if event in (None, 'Exit'):
        break
    elif event == 'Enter':
        operation, tags, filename = lb.parse_args(['--search', values['-IN-']])
        print(operation, tags)
        if operation == 'search':
            fids = lb.search(tags)
            print(fids)

            if fids:
                #for fid in fids:
                #    with Image.open(f'data/{fid}') as img:
                #        if
                fid = fids.pop()
                with Image.open(f'data/{fid}') as img:
                    thmb = img.copy()
                    thmb.thumbnail((128, 128))
                    filename = 'data/tmp/im1.gif'
                    thmb.save(filename)
                    window['im1'].Update(filename=filename, size=thmb.size, visible=True)
    elif event == 'im1':
        with Image.open(f'data/{fid}') as img:
            filename = 'data/tmp/im1.gif'
            img.thumbnail(max_size)
            img.save(filename)
            window['im1'].Update(filename=filename, size=img.size, visible=True)


window.Close()

