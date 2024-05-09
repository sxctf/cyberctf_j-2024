from flask import Flask, redirect, render_template, request, url_for, flash, session
import models
import array
import xml.etree.ElementTree as ET
import uuid
from random import randint
import re

app = Flask(__name__)
app.config['SECRET_KEY'] = 'a really really really really long secret key'

@app.route('/', methods=['GET','POST'])
def index():
    if request.method == "GET":
        return render_template("index.html")
    if request.method == "POST":
        return redirect("/work")

@app.route('/work', methods=['GET','POST'])
def main():
    if request.method == "GET":
        textleft = createXML()
        textright = createXML()
        session['left'] = textleft
        session['right'] = textright
        parsing = parseXML(textright)

        rightGuid = parsing[0]
        rightTime = parsing[1]
        rightType = parsing[2]
        rightSpeed = parsing[3]
        rightPassengers = parsing[4]

        parsing = parseXML(textleft)

        leftGuid = parsing[0]
        leftTime = parsing[1]
        leftType = parsing[2]
        leftSpeed = parsing[3]
        leftPassengers = parsing[4]

        return render_template("work.html",
        lGuid = leftGuid, lTime = leftTime, lType = leftType, lSpeed = leftSpeed, lPass= leftPassengers,
        rGuid = rightGuid, rTime = rightTime, rType = rightType, rSpeed = rightSpeed, rPass= rightPassengers)
    
    if request.method == "POST":
        text_from_input = request.form.get('tagInput')
        out = validate(text_from_input)
        if out!=False:
            ltext_to_update = session['left']
            rtext_to_update = session['right']
            lparsed = parseXML(ltext_to_update)
            rparsed = parseXML(rtext_to_update)

            id = getTagID(out)
            value = getValue(out)
            lparsed[id] = value

            rightGuid = rparsed[0]
            rightTime = rparsed[1]
            rightType = rparsed[2]
            rightSpeed = rparsed[3]
            rightPassengers = rparsed[4]

            leftGuid = lparsed[0]
            leftTime = lparsed[1]
            leftType = lparsed[2]
            leftSpeed = lparsed[3]
            leftPassengers = lparsed[4]
            
            if len(str(lparsed[0]))>512:
                leftGuid = "flag{wlJPbHEKUXoGvoBzRTqvfhoC}"

            return render_template("work.html",
        lGuid = rightGuid, lTime = rightTime, lType = rightType, lSpeed = rightSpeed, lPass= rightPassengers,
        rGuid = leftGuid, rTime = leftTime, rType = leftType, rSpeed = leftSpeed, rPass= leftPassengers)

        else:
            flash("Ошибка в XML")
            return redirect("/work")


def createXML():
    root = ET.Element('train')
    num = randint(1,10)
    timing = str("+"+str(num*12))
    typeArray = ("express","fast","normal")
    typeArrayRand = randint(0,2)
    trainSpeed = str(randint(100,1000))
    trainPassengers = str(randint(50,200))

    trainCode = ET.SubElement(root,'code')
    trainCode.text = str(uuid.uuid4())
    
    trainTime =ET.SubElement(trainCode, 'time')
    trainTime.text = timing

    trainType = ET.SubElement(trainCode, 'type')
    trainType.text = typeArray[typeArrayRand]

    trainMaxSpeed = ET.SubElement(trainCode, 'maxSpeed')
    trainMaxSpeed.text = trainSpeed

    trainMaxPassengers = ET.SubElement(trainCode, 'maxPassengers')
    trainMaxPassengers.text = trainPassengers

    tree = ET.ElementTree(root)
    out = ET.tostring(root)
    return out

def parseXML(xml):
    tree = ET.ElementTree(ET.fromstring(xml))
    root = ET.fromstring(xml)
    out = list()
    t = ""
    for child in root:
        out.append(child.text)
        for c in child:
            print(c.text)
            t = str(c.text)
            out.append(t)
    return out


def validate(s):
    # Регулярное выражение для проверки, содержит ли строка только буквы и цифры
    a = None
    regex = re.compile(r'\<tag\>(.*?)\<\/tag\>')
    ss = str(s)
    match = re.search(r'\<.*?\>(.*?)\<\/.*?\>',ss)
    tags = ["<code>","<time>","<type>","<maxSpeed>","<maxPassengers>"]

    if match:
        a = match.group()
        tagMatch = re.search(r'\<.*?\>',a)
        if not tagMatch.group(0) in tags:
            return False
    if a !=None:
        return a
    else:
        return False

def getTagID(s):
    tagMatch = re.search(r'\<.*?\>',s)

    tags = ["<code>","<time>","<type>","<maxSpeed>","<maxPassengers>"]
    return tags.index(tagMatch.group(0))

def getValue(s):
    tagMatch = re.search(r'\<.*?\>(.*?)\<\/.*?\>',s)
    return tagMatch.group(1)

if __name__ == '__main__':
    app.run(debug=False, port = 8003, host='0.0.0.0')
