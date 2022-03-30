from app import app

if __name__ == '__main__': #on flask run include: -p 5372 after to run it on port 5372.
    app.run(port=5372)
    print("main = running")
    #if run w/ project_name.py instead of flask run