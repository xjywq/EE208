import os
from app import app, db
from app.models import SportItem

def StopNone(content):
    if content == None or content == 'None':
        return '新品 热款'
    return content

app.add_template_filter(StopNone, 'StopNone')

if __name__ == '__main__':
    app.run(debug=True, port=8080)
