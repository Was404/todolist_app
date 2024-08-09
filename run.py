from app import create_app  # TODO cannot import name 'create_app' from 'app'

app = create_app()  # 

if __name__ == '__main__':
    app.run(debug=True) 
