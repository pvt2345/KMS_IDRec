from flask import Flask, render_template, Response, json, request, session,jsonify, flash, request, redirect, url_for
from flaskext.mysql import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from database import DataBase
from topicmodel import run_lda as lda_model
import time
from pymongo import MongoClient
from werkzeug.utils import secure_filename
import os
import glob
from text_mining.multi_process import MultiExtractor
from text_mining.text_extraction.image_extraction import ImageExtraction



mysql = MySQL()
app = Flask(__name__, static_folder='static')
UPLOAD_FOLDER = 'G:\\temp\\'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
UPLOAD_FOLDER_IDREC = "D:\\OneDrive\\Works\\GUIForIDRec\\static\\upload\\"

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app = Flask(__name__, static_folder="static")
# >>>>>>> f54a257af4902aad4696d0b6f77c508243021e5f

PER_PAGE = 10
results = []
dicData = {}
topic_result = {}
cnData = {}

my_client = MongoClient("mongodb://localhost:27017/")
my_database = my_client['papers']
vi_collection = my_database['vi']

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def regularize(a: str):
    split_ = a.split()
    split__ = []
    for item in split_:
        new_item = ''
        for i in range(len(item)):
            if i == 0:
                new_item += item[i]
            else:
                new_item += (item[i].lower())

        split__.append(new_item)

    new_text = (' ').join(split__)
    return new_text

@app.route('/')
def index():
    return render_template('search.html')

@app.route('/idrec', methods=['GET', 'POST'])
def index_idrec():
    if request.method == 'POST':
        files = glob.glob(UPLOAD_FOLDER + '*')
        for file in files:
            os.remove(file)
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        print(file)
        print(type(file))
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            global filename
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            img = cv2.imread(os.path.join(UPLOAD_FOLDER, filename), 0)
            shape_0 = img.shape[0]
            shape_1 = img.shape[1]

            text_data = ''
            text_data += str(shape_0)
            text_data += ',' + str(shape_1)
            list_ = img.tolist()

            for sublist_ in list_:
                for item_ in sublist_:
                    text_data += ',' + str(item_)
            # data = {'B' : img[:,:,0].tolist(), 'G' : img[:,:,1].tolist(), 'R' : img[:,:,2].tolist()}
            # text_data = json.dumps(data)

            r = requests.post("http://10.0.8.30:8000/extraction", data=text_data)
            text_data_received = r.content.decode('utf-8-sig').replace('\'', '\"')
            print(text_data_received)
            global detected_data
            detected_data = json.loads(text_data_received)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            detected_data['name'] = regularize(detected_data['name'])
            print(filepath)
            # os.remove(os.path.join(UPLOAD_FOLDER, filename))
            # return render_template("result.html", filename=filename, detected_data=detected_data)
            return render_template("choose.html")
    else:
        files = glob.glob(UPLOAD_FOLDER + '*')
        for file in files:
            os.remove(file)
        return render_template("result.html")

@app.route('/search/results', defaults={'page': 1}, methods=['POST'])
def search_request(page):
    time_start =time.time()
    keywords = request.form["input"]
    dicData[0] = keywords
    # page = request.form["page"]
    arr = ''.join(keywords).strip().split(' ')
    resultsPaging = []
    data = {'key_search': keywords}
    jsonRes = DataBase().search(keywords)
    global results
    results = []
    print(jsonRes)
    totals = 0
    for record in jsonRes:
        # print(record)
        docDtl = []
        docDtl.append(record['title'])
        docDtl.append(record['reference'])
        content = ''.join(record['content']).strip()
        docDtl.append(content)
        results.append(docDtl)
        totals = totals + 1
    totalPage = int(totals/10) + 1
    dicData[1] = totalPage
    start = (int(page)-1) * 10
    end = start + 10
    resultsPaging = results[start:end]
    print('done in',time.time()-time_start)
    return render_template('results.html', keywords=keywords, results=resultsPaging, totals=totalPage)

@app.route('/search/results/page/<int:page>' ,  methods=['GET','POST'])
def search_request_paging(page):
    keywords = dicData[0]
    totalPage = dicData[1]
    print(keywords)
    print("Page: " + str(page))
    start = (int(page)-1) * 10
    end = start + 10
    resultsPaging = results[start:end]
    print(resultsPaging)
    return render_template('results.html', keywords=keywords, results=resultsPaging, totals=totalPage)


@app.route('/search_popup/results', defaults={'page': 1}, methods=['POST'])
def search_popup(page):
    # keywords = request.form["input"]
    keywords = request.args.get('sch_content')
    dicData[0] = keywords
    # page = request.form["page"]
    arr = ''.join(keywords).strip().split(' ')

    resultsPaging = []
    data = {'key_search': keywords}
    # req = requests.post('http://127.0.0.1:5000/search', data=data)
    # jsonRes = req.json()
    jsonRes = DataBase().search(keywords)
    print(jsonRes)
    totals = 0
    for record in jsonRes:
        # print(record)
        docDtl = []
        docDtl.append(record['title'])
        docDtl.append(record['reference'])
        content = ''.join(record['content']).strip()
        docDtl.append(content)
        results.append(docDtl)
        totals = totals + 1
    totalPage = int(totals/10) + 1
    dicData[1] = totalPage
    start = (int(page)-1) * 10
    end = start + 10
    resultsPaging = results[start:end]
    return render_template('search_popup.html', keywords=keywords, results=resultsPaging, totals=totalPage)

@app.route('/search_popup/results/page/<int:page>' ,  methods=['GET','POST'])
def search__popup_request_paging(page):
    keywords = dicData[0]
    totalPage = dicData[1]
    print(keywords)
    print("Page: " + str(page))
    start = (int(page)-1) * 10
    end = start + 10
    resultsPaging = results[start:end]
    print(resultsPaging)
    return render_template('search_popup.html', keywords=keywords, results=resultsPaging, totals=totalPage, content_text="")

@app.route('/search-content', defaults={'page': 1}, methods=['POST'])
def search_request_editor(page):
    sch_content = request.form.get('sch-content')
    content_text = request.form.get('content')
    dicData[0] = sch_content

    data = {'key_search': sch_content}
    # req = requests.post('http://127.0.0.1:5000/search', data=data)
    # jsonRes = req.json()
    jsonRes = DataBase().search(sch_content)
    print(jsonRes)
    totals = 0
    for record in jsonRes:
        # print(record)
        docDtl = []
        docDtl.append(record['title'])
        docDtl.append(record['reference'])
        content = ''.join(record['content']).strip()
        docDtl.append(content)
        results.append(docDtl)
        totals = totals + 1
    totalPage = int(totals/10) + 1
    dicData[1] = totalPage
    start = (int(page)-1) * 10
    end = start + 10
    resultsPaging = results[start:end]
    return render_template('results.html', keywords=sch_content, results=resultsPaging, totals=totalPage, content_text=content_text)


@app.route('/showLogin')
def showSignUp():
    return render_template('signup.html')

@app.route('/login', methods=['POST'])
def logIn():
    try:
        _name = request.form['username']
        _password = request.form['password']

        # validate the received values
        if _name and _password:

            # All Good, let's call MySQL

            conn = mysql.connect()
            cursor = conn.cursor()
            _hashed_password = generate_password_hash(_password)
            cursor.callproc('sp_createUser', (_name,  _hashed_password))
            data = cursor.fetchall()

            if len(data) is 0:
                conn.commit()
                return json.dumps({'message': 'User created successfully !'})
            else:
                return json.dumps({'error': str(data[0])})
        else:
            return json.dumps({'html': '<span>Enter the required fields</span>'})

    except Exception as e:
        return json.dumps({'error': str(e)})
    finally:
        cursor.close()
        conn.close()

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return index()

@app.route('/topic', methods=['GET', 'POST'])
def topic():
    # if request.method == 'POST':
    #     # do stuff when the form is submitted
    #
    #     # redirect to end the POST handling
    #     # the redirect can be to the same route or somewhere else
    #     return redirect(url_for('topic'))

    # show the form, it wasn't submitted
    topic_result = {}
    return render_template('topic.html')

@app.route('/topic/lda', methods=['POST'])
def run_lda():
    n_topic = request.form["numberTopic"]
    n_word = request.form["numberKeyword"]
    topics = lda_model.run_lda(int(n_topic),int(n_word))
    # topics = [
    #     {'topic':'topic 1','words':'word 1, word 2, word 3,..., word n','name topic':'nhập tên topic'},
    #     {'topic': 'topic 2', 'words': 'word 1, word 2, word 3,..., word n', 'name topic': 'nhập tên topic'},
    #     {'topic': 'topic 3', 'words': 'word 1, word 2, word 3,..., word n', 'name topic': 'nhập tên topic'}
    # ]
    ID = 1

    for topic in topics:
        topic['id'] = ID
        ID = ID + 1
        topic_result[ID] = topic
    return render_template('result_lda.html', topics=topics)

@app.route('/topic/update', methods=['POST'])
def acceptTopic():
    numberRow = len(topic_result)
    topic_names = []
    for id in range(numberRow):
        topicName = request.form['topicName'+str(id+1)]
        # print(topicName)
        topic_names.append({'name topic':topicName})
    docFinal = lda_model.btn_ok(topic_names)
    print(docFinal[0]['topic'])
    # docFinal = [
    #     {'so_van_ban':'NQ123','trich_yeu_noi_dung':'abc...','topic':'thuế thu nhập cá nhân'},
    #     {'so_van_ban': 'NQ123', 'trich_yeu_noi_dung': 'abc...', 'topic': 'thuế thu nhập cá nhân'},
    #     {'so_van_ban': 'NQ123', 'trich_yeu_noi_dung': 'abc...', 'topic': 'thuế thu nhập cá nhân'},
    #     {'so_van_ban': 'NQ123', 'trich_yeu_noi_dung': 'abc...', 'topic': 'thuế thu nhập cá nhân'},
    #     {'so_van_ban': 'NQ123', 'trich_yeu_noi_dung': 'abc...', 'topic': 'thuế thu nhập cá nhân'}
    # ]
    return render_template('document.html', documents=docFinal)



@app.route('/editor_edit', methods=['GET', 'POST'])
def editor():
    return render_template('editor.html', tabs=3, return_data="")

@app.route('/editor/edit', methods=['GET', 'POST'])
def editor_edit():
    reference = request.args.get('reference')
    content = request.args.get('content')
    # returnData = ''.join(content).join(" ").join(reference)
    returnData = ""
    if content is None:
        returnData = reference
    if content is not None:
        returnData = content + " " + reference
    return render_template('editor.html', tabs=3, return_data=returnData)

@app.route('/progress')
def progress():
    def generate():
        x = 0

        while x <= 100:
            yield "data:" + str(x) + "\n\n"
            x = x + 1
            time.sleep(0.5)

    return Response(generate(), mimetype='text/event-stream')

# @app.route('/vi/page/<int:page>', defaults={'page' : 1})
@app.route('/vi', defaults={'page' : 1})
def output_vi(page):
    cnData['vi'] = vi_collection.find().sort("datetime", -1)
    cnData['total'] = cnData['vi'].count()
    # totals = cnData['total']
    totalPages = cnData['total']//10 + 1
    start = 0
    end =  10
    resultPaging = cnData['vi'][start:end]
    return render_template('vi.html', docs = resultPaging, totals=totalPages)
    # return render_template('vi.html', docs = cnData['vi'])

@app.route('/vi/page/<int:page>')
def output_vi_paging(page):
    cnData['vi'] = vi_collection.find().sort("datetime", -1)
    cnData['total'] = cnData['vi'].count()
    # keywords = dicData[0]
    totalPage = cnData['total']//10 + 1
    # print(keywords)
    print("Page: " + str(page))
    start = (int(page) - 1) * 10
    end = start + 10
    cnData['vi'] = vi_collection.find().sort("datetime", -1)
    resultsPaging = cnData['vi'][start:end]
    print(resultsPaging)
    return render_template('vi.html', docs=resultsPaging, totals=totalPage)

@app.route('/vi/showdoc')
def vi_show():
    doc_name = request.args.get('documentname')
    my_query = {'title' : doc_name}
    data = vi_collection.find(my_query)[0]
    content = data['content'].splitlines()
    pdf_urls = data['pdf_urls']
    pdf_path = data['pdf_path']
    datetime = data['datetime']
    if(len(pdf_urls ) > 0):
        return render_template('vi_showdoc.html', doc_name  = doc_name, content = content, pdf_urls = pdf_urls, pdf_path = pdf_path, datetime = datetime)
    else:
        return render_template('vi_showdoc.html', doc_name  = doc_name, content = content, datetime = datetime)

@app.route('/vi/search_results', defaults={'page' : 1}, methods=['GET', 'POST'])
def vi_showresults(page):
    global vi_keywords
    vi_keywords = request.form["input"]
    query = {"$or": [{"title": {"$regex": "\w*{}\w*".format(vi_keywords)}},
                     {"content": {"$regex": "\w*{}\w*".format(vi_keywords)}}]}
    cnData['vi'] = vi_collection.find(query).sort("datetime", -1)
    cnData['total'] = cnData['vi'].count()
    # keywords = dicData[0]
    totalPage = cnData['total'] // 10 + 1
    # print(keywords)
    print("Page: " + str(page))
    start = 0
    end = 10
    # cnData['vi'] = vi_collection.find().sort("datetime", -1)
    resultsPaging = cnData['vi'][start:end]
    # print(resultsPaging)
    return render_template('vi.html', docs=resultsPaging, totals=totalPage, keywords = vi_keywords)

@app.route('/vi/search_results/page/<int:page>', methods=['GET', 'POST'])
def vi_showresults_paging(page):
    query = {"$or" : [{"title" : {"$regex" : "\w*{}\w*".format(vi_keywords)}}, {"content": {"$regex" : "\w*{}\w*".format(vi_keywords)}}]}
    cnData['vi'] = vi_collection.find(query).sort("datetime", -1)
    cnData['total'] = cnData['vi'].count()
    # keywords = dicData[0]
    totalPage = cnData['total'] // 10 + 1
    # print(keywords)
    print("Page: " + str(page))
    start = (int(page) - 1) * 10
    end = start + 10
    # cnData['vi'] = vi_collection.find().sort("datetime", -1)
    resultsPaging = cnData['vi'][start:end]
    # print(resultsPaging)
    return render_template('vi.html', docs=resultsPaging, totals=totalPage, keywords = vi_keywords)

@app.route('/en/page/1')
def output_en():
    return  render_template('en.html')

@app.route('/extract', methods=['GET', 'POST'])
def extract_request():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        print(file)
        print(type(file))
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            return redirect(url_for('extract_request',
                                    filename=filename))

    pdf_path = UPLOAD_FOLDER + '*.pdf'
    pdf_files = glob.glob(pdf_path)
    if len(pdf_files) > 0:
        # pdf_file = pdf_files[0]
        # print(pdf_file)
        # text_obj = ImageExtraction(pdf_file)
        Extractor = MultiExtractor()
        global text_obj
        text_obj = Extractor.extract(pdf_files)
        # text_obj.extract()
        info = text_obj[0]._info
        data = text_obj[0].to_json()
        os.remove(pdf_files[0])
        content = text_obj[0].data.print(print_content=False)
        # print(content)
        # print(data)
        return render_template('extract.html', data=data, content=content)
    else:
        return render_template('extract.html')

@app.route('/insert_todb')
def insert_todb():
    obj = text_obj[0]
    database = DataBase()
    print('writing...')
    if database.insert(obj.to_record(), table='info') != -1:  # insert thành công info
        obj.data.to_database(database, parent=obj.so_van_ban, table='content', parent_ref=obj.so_van_ban,
                             title_ref=obj.trich_yeu_nd)

    print("saved")
    return "saved"
if __name__ == "__main__":
    app.run(debug=True, port=9000)
    # app.run(debug=True, port=8000, host='0.0.0.0')
