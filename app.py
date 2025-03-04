from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pytz
from PIL import Image, ImageDraw, ImageFont

# Sebze Listeleri

biberler = {"Çarli Biber":"carli",
            "Sarı Acı Çarli":"sari-aci-carli",
            "Yeşil Acı Çarli":"yesil-aci-carli",
            "Sivri Biber":"sivri",
            "Kıl Sivri Biber": "kil-sivri",
            "Kılçık Sivri Biber": "kilcik-sivri",
            "Üçburun Köybiberi":"ucburun",
            "Yeşil Dolma Biber":"yesil-dolma",
            "Kapya Biber":"kapya",
            "Şili Kırmızı Biber":"sili-kirmizi",
            "Şili Yeşil Biber":"sili-yesil",
            "Macar Çarli Biber":"macar-carli",
            "Macar Dolma Biber":"macar-dolma",
            "Jalopen":"jalopen",
            "Yeşil Kampari Biber":"yesil-kampari",
            "California Kırmızı":"california-kirmizi",
            "California Sarı":"california-sari",
            }
domatesler = {"Domates Tekli":"domates-tekli",
              "Domates Salkım":"domates-salkim",
              "Domates-Oval":"domates-oval",
              "Salkito Kokteyl":"salkito-kokteyl"}

salataliklar={"Salatalık":"salatalik",
              "Silor Salatalık":"silor"
}

app = Flask(__name__) # To initalize our Flask app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sebzeler.db' # /// for relative path. Our database will be secured in test.db
db = SQLAlchemy(app) # We finally create an database for 'app'


class Sebze(db.Model): # Sebze class for init
    id = db.Column(db.Integer, primary_key=True)
    sendid = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float(120), nullable=False)


    def __repr__(self):
        return f'<User {self.sendid}>'
class PyVars:
    items_dict = dict()
    with app.app_context(): # To use all sebze prices, we need to load first
        items = Sebze.query.all()
    items_dict = dict()
    for i in items:
        items_dict[i.sendid ] = i.price
    items_id_dict = dict()
    for i in items:
        items_id_dict[i.sendid + " " + str(i.id)] = i.price

print(PyVars.items_id_dict)
@app.route('/', methods=['POST','GET'])

def index():
    with app.app_context(): # To use all sebze prices, we need to load first
        items = Sebze.query.all()
    for i in items:
        PyVars.items_id_dict[i.sendid + " " + str(i.id)] = i.price
        PyVars.items_dict[i.sendid] = i.price
    if request.method == "POST":
        
        img = Image.open("pillow\main_schema.png")
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("pillow/font.ttf", 20)
        
        item_send_biber_once = dict()
        item_send_domates_once = dict()
        item_send_salatalik_once = dict()
        baslik = request.form['date']
        for item in biberler.values():
            item_send_biber_once[item] = request.form[item+'-once']
        for item in domatesler.values():
            item_send_domates_once[item] = request.form[item+'-once']
        for item in salataliklar.values():
            item_send_salatalik_once[item] = request.form[item+'-once']
            
        patlican_once= request.form['patlican-once']
        
        item_send_biber_bugun = dict()
        item_send_domates_bugun = dict()
        item_send_salatalik_bugun = dict()
        for item in biberler.values():
            item_send_biber_bugun[item] = request.form[item+'-bugun']
        for item in domatesler.values():
            item_send_domates_bugun[item] = request.form[item+'-bugun']
        for item in salataliklar.values():
            item_send_salatalik_bugun[item] = request.form[item+'-bugun']
            
        patlican_bugun = request.form['patlican-bugun']
        
        def draw_table(start_x,start_y,str_list,suffix,color,font,line=0,lineadder=31):
            for i in str_list:
                draw.text((start_x, start_y+line), i+suffix, fill=color, font=font,anchor='rt')
                line+=lineadder
            return
        draw_table(354,253,item_send_biber_once.values()," TL",(255, 0, 0),font)
        draw_table(854,253,item_send_domates_once.values()," TL",(255, 0, 0),font)
        draw_table(854,423,item_send_salatalik_once.values()," TL",(255, 0, 0),font)
        draw.text((854,528), patlican_once+ " TL", fill=(255, 0, 0), font=font,anchor='rt')
        
        draw_table(464,253,item_send_biber_bugun.values()," TL",(255, 0, 0),font)
        draw_table(964,253,item_send_domates_bugun.values()," TL",(255, 0, 0),font)
        draw_table(964,423,item_send_salatalik_bugun.values()," TL",(255, 0, 0),font)
        draw.text((964,528), patlican_bugun+ " TL", fill=(255, 0, 0), font=font,anchor='rt')
        font = ImageFont.truetype("pillow/font.ttf", 58)
        draw.text((500,45), baslik, fill=(255, 255, 255), font=font,anchor='mm')
        
        img.save('static/yazili_resim.png')
        
        idcount=1
        for item in item_send_biber_bugun.values():
            with app.app_context():
                item_to_update = db.session.get(Sebze, idcount)  
                if item_to_update:
                    item_to_update.price = float(item)
                    db.session.commit()
                idcount+=1
        
        for item in item_send_domates_bugun.values():
            with app.app_context():
                item_to_update = db.session.get(Sebze, idcount)  
                if item_to_update:
                    item_to_update.price = float(item)
                    db.session.commit()
            idcount+=1
            
        for item in item_send_salatalik_bugun.values():
            with app.app_context():
                item_to_update = db.session.get(Sebze, idcount)
                if item_to_update:
                    item_to_update.price = float(item)
                    db.session.commit()
            idcount+=1
            
        with app.app_context():
            item_to_update = db.session.get(Sebze,idcount)
            if item_to_update:
                item_to_update.price = float(patlican_bugun)
                db.session.commit()
        
        return redirect('/success/')
    else:
        return render_template('index.html', biberler=biberler, domatesler=domatesler, salataliklar=salataliklar, items_dict=PyVars.items_dict)
    

@app.route ('/success/')
def success():
    return render_template('success.html')

@app.route('/resim.png')
def resim():
    return redirect('static/yazili_resim.png')

if __name__ == "__main__":
    app.run(debug=True)
    

