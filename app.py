#If youtube-dl is taking too much space, remove it and enable internal backend from pafy kernal
import pafy
from youtubesearchpython import VideosSearch as Ysearch
from flask import Flask,request,send_file
from flask_restful import  Api, Resource
from flask_cors import CORS, cross_origin

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
            'status':'Success',
            'result':formattedResults,
        }    
    except Exception as e:
        return {
            'status':'Error',
            'result':str(e)
        }              

def getYoutubeFile(code,quality):
    video = pafy.new("https://www.youtube.com/watch?v="+code)
    extension = None
    if quality=='High':
        video.getbestaudio().download()
    else:
        audiostreams = video.audiostreams
        lowAudio = audiostreams[0]
        for a in audiostreams:
              if lowAudio.get_filesize()> a.get_filesize():
                  lowAudio = a
        print(lowAudio.get_filesize())  
        extension = lowAudio.extension          
        print(extension)    
        lowAudio.download();          
    if extension==None:
        try:
            return video.title+'.m4a'
        except FileNotFoundError:
            return video.title+'.ogg'
    return video.title+'.'+extension    
    
#Flask API 
class SearchYoutube(Resource):
    def get(self):
        query = request.form['query']
        result = searchYoutube(query)
        return result
class GetYTAudio(Resource):
    def post(self):
        code = request.form['code']
        quality = request.form['quality']
        audio = getYoutubeFile(code,quality)
        return send_file(audio)

class Test(Resource):
    def get(self):
        return {
            'status':'Succesful',
            'result':'The fetch was succesful',
        }
app = Flask(__name__)
api = Api(app)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
api.add_resource(SearchYoutube,'/youtubeSearch')
api.add_resource(GetYTAudio,'/getYTAudio')
api.add_resource(Test,'/')

# print(searchYoutube('see you again song')) 
# getYoutubeFile("RgKAFK5djSk")
if __name__ == '__main__':
    app.run(debug=False)    