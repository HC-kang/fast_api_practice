from imp import reload
import uvicorn

if __name__ == '__main__':
    uvicorn.run('app.main2:app', host='0.0.0.0', port=8000, reload=True)
