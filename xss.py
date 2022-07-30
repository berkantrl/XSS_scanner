from bs4 import BeautifulSoup as bs 
import requests 
from urllib.parse import urljoin


def get_all_forms(url):
    soup = bs(requests.get(url).content,"html.parser")
    return soup.find_all("form")

def get_forms_details(form):
    details = {}

    action = form.attrs.get("action").lower()
    method = form.attrs.get("method","get").lower()

    inputs = [] 
    for input_tag in form.find_all("input"):
        input_type = input_tag.attrs.get("type","text")
        input_name = input_tag.attrs.get("name")
        inputs.append({"type": input_type, "name":input_name})

    details["action"] = action 
    details["method"] = method
    details["inputs"] = inputs 

    return details 

def submit_forms(form_details,url,value):

    target_url = urljoin(url,form_details["action"])

    inputs = form_details["inputs"]
    data  = {}

    for input in inputs:
        if input["type"] == "text" or input["type"] == "search":
            input["value"] = value 
            input_name = input.get("name")
            input_value = input.get("value")
            if input_name and input_value : 
                data[input_name] = input_value 
            if form_details["method"] == "post":
                return requests.post(target_url,data=data)
            else:
                return requests.get(target_url,params=data)

def scan_xss (url):
    forms = get_all_forms(url)
    print("kontrol ediliyor...")
    js_script = "<script>alert('hi')</script>"
    is_vulnerable = False 
    for form in forms: 
        form_details = get_forms_details(form)
        content = submit_forms(form_details,url,js_script).content.decode()
        if  js_script in content:
            print("XSS zafiyeti saptanmıştır")
            is_vulnerable = True
    return is_vulnerable 

if __name__ == "__main__":
    url = "http://testphp.vulnweb.com/"
    is_vulnerable = scan_xss(url)