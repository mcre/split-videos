import datetime as dt
import glob
import os
import math
import shutil
import subprocess
import sys


UTC = dt.timezone(dt.timedelta(hours=0))


def get_metadata(path):
    result = subprocess.check_output(f'ffprobe -show_entries format {path}', shell=True)
    metadata_list = result.decode().strip().split('\n')
    if metadata_list[0] != '[FORMAT]' or metadata_list[-1] != '[/FORMAT]':
        raise Exception()
    return {eq.split('=')[0]: eq.split('=')[1] for eq in metadata_list[1:-1]}


def main(duration):
    for path in sorted(glob.glob('input/**/*.*', recursive=True)):
        if os.path.splitext(path)[1].lower() not in ['.mp4', '.m4a', '.mov', '.qt', '.mpeg', '.mpg', '.vob', '.avi', '.asf', '.wmv', '.webm', '.flv', '.f4v', '.mkv', '.m2ts', '.mts', '.ts']:
            continue

        output = path.replace('input/', 'output/')
        os.makedirs(os.path.dirname(output), exist_ok=True)

        metadata = get_metadata(path)
        duration_original = float(metadata['duration'])

        if duration_original < duration:
            print('copy')
            shutil.copy2(path, output)
            continue

        print(metadata)

        ts = None
        if 'TAG:date' in metadata:
            ts = dt.datetime.fromisoformat(metadata['TAG:date'])

        part_count = math.ceil(duration_original / duration)
        part_duration = duration_original / part_count
        for i in range(part_count):
            new_metadata_string = ''
            if ts is not None:
                ts_offset = ts + dt.timedelta(seconds=i * part_duration)
                data = {
                    'creation_time': ts_offset.astimezone(UTC).strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                    'date': ts_offset.isoformat(),
                }
                new_metadata_string = ' '.join([f'-metadata {k}="{v}"' for k, v in data.items()])

            sp = os.path.splitext(output)
            output_fn = f'{sp[0]}-{i:03}{sp[1]}'

            if i < part_count - 1:
                cmd = f'ffmpeg -y -i {path} -ss {i * part_duration:.3f} -to {(i + 1) * part_duration:.3f} -codec:v copy -codec:a copy {new_metadata_string} {output_fn}'
            else:  # 最後はtoを指定しない
                cmd = f'ffmpeg -y -i {path} -ss {i * part_duration:.3f} -codec:v copy -codec:a copy {new_metadata_string} {output_fn}'
            print('\n\ncall ------')
            print(cmd)
            subprocess.call(cmd, shell=True)
            if ts:
                cmd = f'touch -c -t {ts_offset.astimezone(UTC).strftime("%Y%m%d%H%M.%S")} {output_fn}'
                print(cmd)
                subprocess.call(cmd, shell=True)


if __name__ == '__main__':
    duration = 600
    if len(sys.argv) > 1:
        duration = float(sys.argv[1])
    main(duration)
