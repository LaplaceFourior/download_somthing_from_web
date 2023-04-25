import json

file_formats = {
    'txt': 'Text file',
    'pdf': 'PDF file',
    'doc': 'Microsoft Word document',
    'docx': 'Microsoft Word Open XML document',
    'xls': 'Microsoft Excel spreadsheet',
    'xlsx': 'Microsoft Excel Open XML spreadsheet',
    'ppt': 'Microsoft PowerPoint presentation',
    'pptx': 'Microsoft PowerPoint Open XML presentation',
    'jpg': 'JPEG image',
    'png': 'PNG image',
    'gif': 'GIF image',
    'mp3': 'MP3 audio file',
    'mp4': 'MP4 video file',
    'avi': 'AVI video file',
    'mov': 'QuickTime movie file',
    'zip': 'ZIP archive file',
    'rar': 'RAR archive file',
    'tar': 'TAR archive file',
    'gz': 'GZIP archive file',
    '7z': '7-Zip archive file'
}

# with open('allfile.json', 'w') as f:
#     json.dump(file_formats, f)

# for key in file_formats:
#     print( type(key))