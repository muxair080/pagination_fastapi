import httpx 
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

@app.get('/')
def index():
    return {"pagination : " : "This is the pagination code in fastapi"}

response_data = httpx.get('https://jsonplaceholder.typicode.com/posts')
data = response_data.json()
data_length = len(data)

@app.get('/getposts')
def getPosts(page_num : int = 1,page_size : int = 10):
    start = (page_num - 1)*page_size
    end = start + page_size

    response = {
        'data' : data[start:end],
        'total' : data_length,
        'posts per page' : page_size,
        'pagination' : {}
    }

    if end > data_length:
        response['pagination']['next'] = None
        response['data'] = 'This is the end of the posts'

        if page_num > 1:
            page = page_num -1
            response['pagination']['previous'] = f'/posts?page_num={page} &page_size={page_size}'
        
        else:
            response['pagination']['previous'] = None
    else:
        if page_num > 1:
            page = page_num -1
            response['pagination']['previous'] = f'/posts?page_num={page} &page_size={page_size}'
        
        else:
            response['pagination']['previous'] = None
    page = page_num-1
    response['pagination']['next'] = f'/posts?page_num={page}&page_size={page_size}'

    return response

