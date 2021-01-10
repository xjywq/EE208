import os
from app import app, db
import json
from app.models import SportItem

def StopNone(content):
    if content == None or content == 'None':
        return '新品 热款'
    return content

def get_first(content):
    if isinstance(content, str):
        content = json.loads(content)
    return content[0]

app.add_template_filter(StopNone, 'StopNone')
app.add_template_filter(get_first, 'get_first')

if __name__ == '__main__':
    app.run(debug=True, port=8080)
