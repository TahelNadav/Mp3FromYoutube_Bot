# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import view

if __name__ == '__main__':
    view.app.run(port=5003)
#
# from googleapiclient.discovery import build
#
# api_key = 'AIzaSyCbNWORtYUVDopm3bcjlB-IhP0bUxVzMt0'
#
# youtube = build('youtube', 'v3', developerKey=api_key)
# type(youtube)
# s=youtube.search().list(q='python',part='snippet',type='video')
# l=s.execute()
# print((l['items']))
