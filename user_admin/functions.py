def handle_uploaded_file(f):  
    with open('static/upload/Image/'+f.name, 'wb+') as destination:  
        for chunk in f.chunks():  
            destination.write(chunk)  


