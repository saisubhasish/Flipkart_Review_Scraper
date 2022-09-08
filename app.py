from flask import Flask, render_template, request,jsonify
from flask_cors import CORS,cross_origin
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq       # Urllib is the url handling module of python. It is used to fetch urls.

app = Flask(__name__)                            # Creating object of Flask

@app.route("/", methods=['GET'])                 # methods defines the type of method allowed in the block
@cross_origin()
def  homePage():
    return render_template("index.html")         # render_template() executes the templates insides templates folder

@app.route('/review', methods=['Post', 'GET'])   # route function defines the path
@cross_origin()                                  # cross_origin allows a server to get accessed from any origin
def index():
    if request.method == 'POST':
        try:
            searchString =request.form['content'].replace(" ",'')
            flipkart_url = "https://www.flipkart.com/search?q="+searchString
            uClient = uReq(flipkart_url)         # Sending request url to the browser
            flipkartPage = uClient.read()        # Reading the content of webpage
            uClient.close()
            flipkart_html = bs(flipkartPage, "html.parser")         # Beautiful Soup is a python package for parsing HTML and XML documents. It creates a parse tree for parsed pages that can be used to extract data from HTML.
            big_boxes =flipkart_html.find_all('div' ,{'class': '_1AtVbE col-12-12'})
            del big_boxes[0:3]
            box = big_boxes[0]
            print(box)
            productLink = "https://www.flipkart.com"+box.div.div.div.a['href']
            print(productLink)
            proRes = requests.get(productLink)
            proRes.encoding='utf-8'      # www's most common character encoding. Each character is represented by four bytes.
            prod_html = bs(proRes.text, 'html.parser')

            commentBoxes =prod_html.find_all('div', {'class' : "_16PBlm"})

            fileName = searchString+'.csv'
            fw =open(fileName, "w")
            headers = "price, product, customer name, rating, heading, comment \n"
            fw.write(headers)
            reviews = []
            for commentBox in commentBoxes:
                try:
                    price = prod_html.find_all('div', {'class': "_30jeq3 _16Jk6d"})[0].text

                except:
                    price = "No Price Available"

                try:
                    name = commentBox.div.div.find_all('p', {'class': '_2sc7ZR _2V5EHH'})[0].text
                except:
                    name = 'No name'

                try:
                    rating = commentBox.div.div.div.div.text
                except:
                    rating = "No rating"

                try:
                    commentHead = commentBox.div.div.div.p.text
                except:
                    commentHead = "No Comment Heading"

                try:
                    comTag = commentBox.div.div.find_all('div', {'class': ''})
                    custComment = comTag[0].div.text
                except Exception as e:
                    print("Exception while creating dictionary : ", e)

                myDict ={'price': price, 'product': searchString, "name": name, "rating": rating, "commentHead": commentHead, "comment": custComment}
                reviews.append(myDict)
            return render_template('results.html', reviews=reviews[0:(len(reviews)-1)])

        except Exception as e:
            print("The exception message is : ", e)
            return 'something is wrong'

    else:
        return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)
















