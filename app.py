#If youtube-dl is taking too much space, remove it and enable internal backend from pafy kernal
import pafy
from youtubesearchpython import VideosSearch as Ysearch
from flask import Flask,request,send_file
from flask_restful import  Api, Resource


#API functions
def searchYoutube(query): 
    try:
        results = Ysearch(query).result()['result']
        formattedResults = []
        for result in results[0:10]:
            formattedResults.append({
                'title':result['title'],

                'id':result['id'],
                'thumbnail':result['thumbnails'][0],
                'viewCount':result['viewCount']['short'],
                'duration':result['duration'],
                'artist':{
                    'name':result['channel']['name'],
                    'id':result['channel']['id'],
                    'thumbnail':result['channel']['thumbnails'][0]
                }
            })
        print("Youtube Search Succesful")
        return {
            'code':'Success',
            'result':formattedResults,
        }    
    except Exception as e:
        return {
            'code':'Error',
            'result':str(e)
        }              

def getYoutubeFile(code):
    video = pafy.new("https://www.youtube.com/watch?v="+code)
    video.getbestaudio().download()
    try:
        return video.title+'.m4a'
    except FileNotFoundError:
        return video.title+'.ogg'
    
#Flask API 
class SearchYoutube(Resource):
    def get(self):
        query = request.form['query']
        result = searchYoutube(query)
        return result
class GetYTAudio(Resource):
    def post(self):
        code = request.form['code']
        audio = getYoutubeFile(code)
        return send_file(audio)

app = Flask(__name__)
api = Api(app)
api.add_resource(SearchYoutube,'/youtubeSearch')
api.add_resource(GetYTAudio,'/getYTAudio')

# print(searchYoutube('see you again song')) 
# getYoutubeFile("RgKAFK5djSk")
if __name__ == '__main__':
    app.run(debug=False)    