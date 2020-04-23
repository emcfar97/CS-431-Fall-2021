import ffmpeg
from ffprobe import FFProbe
from os import remove, listdir, getcwd
from os.path import join, exists

def get_stream(folder):
    
    stream = [
        ffmpeg.input(join(folder, file)) for file in listdir(folder)
        ]
    new = join(dest, listdir(folder)[0]).replace('flv', 'mp4')
    
    return stream, new

def get_folders():
    
    targets = input('Target folders: ')
    
    if '..' in targets:
        start, end = targets.split('..')
        return tuple(str(i) for i in range(int(start), int(end) + 1))
        
    else: return tuple(targets.split())
    
root = getcwd()[:2].upper()
source = rf'{root}\Users\Emc11\Videos\Captures'
dest = rf'{root}\Users\Emc11\Dropbox\Videos\Captures'

while True:
    user_input = input(
        'Choose from:\n1 - Convert files\n2 - Concat files\n3 - Change framerate\n4 - Download m3u8\n5 - Check directories\n6 - Exit\n'
        )
    try:
        if  user_input ==  '1': # convert files

            files = [
                (join(source, file), join(dest, file.replace('.flv', '.mp4'))) 
                for file in listdir(source) if file.endswith('flv')
                ]
            if not files: print(f'No files at {source}')
            for flv, mp4 in files:
                try: ffmpeg.input(flv).output(mp4, crf=20, preset='fast').run()
                except Exception as error: print(error); continue
                remove(flv)

        elif user_input == '2': # concat files
            
            targets = get_folders()
            
            for folder in listdir(source):
                
                if not folder.endswith((targets)): continue
                stream, new = get_stream(join(source, folder))
                
                try: ffmpeg.concat(*stream).output(new, crf=20, preset='fast').run()
                except Exception as error: print(error); continue
                for file in stream: remove(file.node.kwargs['filename'])

        elif user_input == '3': # change framerate
            
            targets = get_folders()

            for folder in listdir(source):

                if not folder.endswith((targets)): continue
                folder = join(source, folder)
                stream, new = get_stream(folder)
                
                desired = int(input('Enter desired length (minutes): ')) * 60
                duration = sum(
                    float(FFProbe(join(folder, file)).streams[0].duration)
                    for file in listdir(folder)
                    )
                try:
                    ffmpeg.concat(*stream).setpts(
                        f'{desired / duration:.4f}*PTS') \
                        .output(new, crf=20, preset='fast').run()
                except Exception as error: print(error); continue
                for file in stream: remove(file.node.kwargs['filename'])
                
        elif user_input == '4': # download m3u8
            
            url = input('Enter url: ')
            name = f'{url.split("/")[3]}.mp4'
            ffmpeg.input(url).output(
                rf'{root}\Users\Emc11\Downloads\{name}').run()
            
        elif user_input == '5':
        
            for file in listdir(source):
                if file.endswith('.ini'): continue
                if file.startswith('Batch'):
                    print(f'{file}: {listdir(join(source, file))}')
                    continue
                print(file)
            print() 
        
        elif user_input == '6': break
            
    except: continue
