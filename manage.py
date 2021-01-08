import os
from app import app, db
from app.models import SportItem

if __name__ == '__main__':
    app.run(debug=True, port=8080) 
