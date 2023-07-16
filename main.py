from fastapi import FastAPI, File, UploadFile, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import subprocess
from colabcode import ColabCode

app = FastAPI()


app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def main():
    return HTMLResponse(content=open("static/index.html").read(), status_code=200)

@app.get("/Contacts")
async def Contacts():
    return HTMLResponse(content=open("static/Contacts.html").read(), status_code=200)

@app.post("/submit")
async def get_info(image: UploadFile = File(...), message: str = Form(...)):
    try:
        # Save the image to a directory or perform any other operations you want
         
        msg_str = message
        contents = await image.read()
        img_path = f"static/{image.filename}"
        with open(img_path, "wb") as f:
            f.write(contents)    

        subprocess.check_call(['python', 'generate.py', '--image', img_path, '--message', msg_str], bufsize=0 )
       
        
        return HTMLResponse(content=open("static/output.html").read(), status_code=200)
        
         
        
    except Exception as e:
        return HTMLResponse(content=open("static/error.html").read(), status_code=500)
    
cc = ColabCode(port=8000, code=False)
    
if __name__ == "__main__":
    
    cc.run_app(app=app)


