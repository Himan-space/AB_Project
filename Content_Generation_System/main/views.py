from django.shortcuts import render
from django.http import FileResponse
from .generator import *
import aspose.words as aw
import markdown


# Create your views here.
def index(request):
    md = markdown.Markdown(extensions=["fenced_code"])
    context = {}
    context['prompts'] = get_questions_dict().keys()
    context['country_codes'] = get_country_code_dict()
    context['domains'] = get_urls
    if request.method == 'POST':
        prompt = get_prompt(request.POST['prompt'])
        country_code = request.POST['region']
        domain = [request.POST['domain']] if request.POST['domain'] else get_urls()
        #print(prompt,country_code,domain)
         
        content_str = generate_content_piece(prompt, country_code, domain)
        content = md.convert(content_str)
        context['content'] = content


        file_path_md = "static/data/output.md"
        # Write the content to the file
        with open(file_path_md, "w") as file:
            file.write(content_str)
        
        file_path = "static/data/output.txt"
        # Write the content to the file
        with open(file_path, "w") as file:
            file.write(content)

        output = aw.Document()
        output.remove_all_children()
        input = aw.Document(file_path_md)
        output.append_document(input, aw.ImportFormatMode.KEEP_SOURCE_FORMATTING)
        output.save("static/data/output.docx")

        return render(request, 'main/base.html',context)
    context['content'] = 'Kindly select or enter prompt.'
    return render(request, 'main/base.html',context)


def download(request, file_type):
    if file_type == 'md':
        filename = 'static/data/output.md'
    elif file_type == 'docx':
        filename = 'static/data/output.docx'
        
    response = FileResponse(open(filename, 'rb'))
    return response