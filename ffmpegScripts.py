import ffmpeg
from os import path
from pathlib import Path
from ffprobe import FFProbe
from re import search, sub, findall

EXT = '.mp4', '.flv', '.mkv'
ROOT = Path(Path(__file__).drive)
USER = ROOT / path.expandvars(r'\Users\$USERNAME')
DOWN = USER / r'Downloads\Images'
SOURCE = USER / r'Videos\Captures'
DEST = USER / r'Dropbox\Videos\Captures'

def get_stream(files, text):
        
    new = DEST / files[0].with_suffix('.mp4').name

    if text and text in 'yes':
        stream = [
            ffmpeg.input(str(file)).drawtext(
                text=file.stem, fontsize=45, 
                x=int(FFProbe(file).streams[0].width) * .70, 
                y=int(FFProbe(file).streams[0].height) * .85,
                shadowcolor='white', shadowx=2, shadowy=2
                ) 
            for file in files
            ]
    else: stream = [ffmpeg.input(str(file)) for file in files]
    
    return new, stream

def get_folders():
    
    targets = input('Target folders: ')
    
    if '..' in targets:
        start, end = targets.split('..')
        return ''.join(str(i) for i in range(int(start), int(end) + 1))
        
    return targets

while True:
    
    user_input = input(
        'Choose from:\n1 - Convert videos\n2 - Concat videos\n3 - Change framerate\n4 - Split video\n5 - Download m3u8\n6 - Check directories\n7 - Change destination directory\n8 - Exit\n'
        )
    
    try:
        if   user_input == '1': # convert vidoes
                
            text = input('Overlay text? ').lower()

            files = [
                (
                    SOURCE / file, DEST / file.with_suffix('.mp4').name
                    )
                for file in SOURCE.iterdir() if file.suffix in EXT
                ]
            
            for file, mp4 in files:
                try: 
                    if text and text in 'yes':
                        metadata = FFProbe(str(file)).streams[0]
                        ffmpeg.input(str(file)).drawtext(
                            text=file.stem, fontsize=45, 
                            x=int(metadata.width) * .70, 
                            y=int(metadata.height) * .85,
                            shadowcolor='white', shadowx=2, shadowy=2
                        ).output(str(mp4), crf=20, preset='fast').run()
                    else: 
                        ffmpeg.input(str(file)).output(str(mp4), crf=20, preset='fast').run()
                except Exception as error: print(error); continue
                file.unlink()

        elif user_input == '2': # concat videos
            
            text = input('Overlay text? ').lower()
            
            for folder in SOURCE.glob(f'*Batch[{get_folders()}]'):
                
                files = [
                    file for file in folder.iterdir()
                    if file.suffix in EXT
                    ]
                new, stream = get_stream(files, text)
                
                try: ffmpeg.concat(*stream).output(str(new), crf=20, preset='fast').run()
                except Exception as error: print(error); continue
                for file in files: file.unlink()

        elif user_input == '3': # change framerate
            
            text = input('Overlay text? ').lower()

            for folder in SOURCE.glob(f'*Batch[{get_folders()}]'):

                files = [
                    file for file in folder.iterdir()
                    if file.suffix in EXT
                    ]
                new, stream = get_stream(files, text)
                
                desired = float(input('Enter desired length (minutes): ')) * 60
                duration = sum(
                    float(FFProbe(file).streams[0].duration)
                    for file in files
                    )
                try:
                    ffmpeg.concat(*stream).setpts(
                        f'{(desired - 1) / duration:.4f}*PTS') \
                        .output(str(new), crf=20, preset='fast'
                        ).run()
                except Exception as error: print(error); continue
                for file in files: file.unlink()

        elif user_input == '4': # split video

            file = Path(input('Enter filepath: ').strip())

            if file.exists():
                
                if search(' \d+', file.stem):
                    num = int(*findall(' (\d+)', file.stem))
                    new = sub(f' {num}+', f' {num+1:02}', file.stem)
                else: new = f'{file.stem} Part 00'
                new = file.with_stem(new)

                start = input('Enter start time (seconds or hh:mm:ss): ')
                end = input('Enter end time (seconds or hh:mm:ss): ')
                
                if end == '':
                    
                    ffmpeg.input(str(file)).trim(
                        start=start).output(str(new), preset='fast').run()

                else:
                    
                    ffmpeg.input(str(file)) \
                        .trim(start=start, end=end) \
                        .setpts('PTS-STARTPTS') \
                        .output(str(new), preset='fast').run()

            else: raise FileNotFoundError

        elif user_input == '5': # download m3u8
            
            url = input('Enter url: ')
            name = f'{url.split("/")[3]}.mp4'
            ffmpeg.input(url).output(str(DOWN / name)).run()

        elif user_input == '6': # check directories
            
            print(ROOT)
            for file in SOURCE.iterdir():
                if file.is_dir():
                    print(f'{file}: {[str(i) for i in file.iterdir()]}')
                elif file.suffix in EXT: print(str(file))
            print() 
        
        elif user_input == '7': # change destination

            path = Path(input('Enter path: '))
            if path.exists(): 
                DEST = path
                print('Success\n')
            else: raise FileNotFoundError

        elif user_input == '8': break
            
    except Exception as error: print(error, '\n')
