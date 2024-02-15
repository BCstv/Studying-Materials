from fastapi import FastAPI

app = FastAPI(root_path=r'C:\Users\Admin\Desktop\Repo1\8 Studying materials\Web-development\FastAPI\pythonProject\.venv')


@app.get("/")
async def root():
    return {"message": "Hello World"}


