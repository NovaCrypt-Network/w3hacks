from django.shortcuts import render
from django.core.files.storage import FileSystemStorage

def index(request):
    if request.method == "POST":
        myfile = request.FILES["myfile"]
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        print(uploaded_file_url)

    return render(request, "landingpage/index.html")
