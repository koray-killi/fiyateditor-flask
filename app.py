from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pytz
from PIL import Image, ImageDraw, ImageFont

# Sebze Listeleri
Heroku = False

class Fiyatlar:
    def __init__(self,isim,dun,bugun):
        self.isim = isim
        self.dun = float(dun)
        self.bugun = float(bugun)


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
    def refresh():
        with app.app_context(): # To use all sebze prices, we need to load first
            items = Sebze.query.all()
        for i in items:
            PyVars.items_id_dict[i.sendid + " " + str(i.id)] = i.price
            PyVars.items_dict[i.sendid] = i.price
        return

print(PyVars.items_id_dict)
@app.route('/', methods=['POST','GET'])

def index():
    PyVars.refresh()
    if request.method == "POST":
        
        #       IMAGE CREATION SIDE        #
        def transparant_maker(image_way):
            img = Image.open(image_way) 
            rgba = img.convert("RGBA")
            datas = rgba.getdata()
            newData = [] 
            for item in datas: 
                if item[0] == 0 and item[1] == 0 and item[2] == 0:  # finding black colour by its RGB value 
                    # storing a transparent value when we find a black colour 
                    newData.append((255, 255, 255, 0)) 
                else: 
                    newData.append(item)  # other colours remain unchanged 
            
            rgba.putdata(newData) 
            return rgba
            
            
        img= Image.open("pillow/main_schema.png").convert("RGBA")
        up_arr = Image.open("pillow/up.png").convert("RGBA")
        down_arr = Image.open("pillow/down.png").convert("RGBA")
        eq_arr = Image.open("pillow/eq.png").convert("RGBA")
        
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("pillow/font.ttf", 20)
        
        def request_for(input_list,once):
            output_dict = dict()
            if once == True:
                for i in input_list:
                    output_dict[i] = request.form[i+'-once']
                    
            else:
                for i in input_list:
                    output_dict[i] = request.form[i+'-bugun']
            return output_dict
        
        def class_request_for(input_list):
            output_list=list()
            for i in input_list:
                output_list.append(Fiyatlar(i,request.form[i+'-once'],request.form[i+'-bugun']))
            return output_list  

        baslik = request.form['date']
        
        item_send_biber_once = request_for(biberler.values(),once=True)
        item_send_domates_once = request_for(domatesler.values(),once=True)
        item_send_salatalik_once = request_for(salataliklar.values(),once=True)
        patlican_once= request.form['patlican-once']
        
        item_send_biber_bugun = request_for(biberler.values(),once=False)
        item_send_domates_bugun = request_for(domatesler.values(),once=False)
        item_send_salatalik_bugun = request_for(salataliklar.values(),once=False)
        patlican_bugun = request.form['patlican-bugun']
            
        def draw_table(start_x,start_y,str_dict,color,font,once,line=0,lineadder=31,compress_list=None,suffix=" TL",single=False,ex_args=list()):
            print(ex_args)
            if single == True:
                draw.text((start_x, start_y+line), str_dict+suffix, fill=color, font=font,anchor='rt')
                if once==True:
                    if compress_list.dun<compress_list.bugun:
                        img.paste(up_arr,(start_x+18,start_y+line-4), up_arr)
                    elif compress_list.dun>compress_list.bugun:
                        img.paste(down_arr,(start_x+18,start_y+line-4), down_arr)
                    else:
                        img.paste(eq_arr,(start_x+18,start_y+line-7), eq_arr)
                        
                return
        
            for j,i in str_dict.items():
                draw.text((start_x, start_y+line), i+suffix, fill=color, font=font,anchor='rt')
                item_index = list(str_dict.keys()).index(j)
                
                if once==True:
                    print(f'Karşılaştırılan:{compress_list[item_index].isim}\n Önce Fiyat: {compress_list[item_index].dun}, Bugün Fiyat: {compress_list[item_index].bugun}')
                    if compress_list[item_index].dun<compress_list[item_index].bugun:
                        img.paste(up_arr,(start_x+18,start_y+line-4), up_arr)
                    elif compress_list[item_index].dun>compress_list[item_index].bugun:
                        img.paste(down_arr,(start_x+18,start_y+line-4), down_arr)
                    else:
                        img.paste(eq_arr,(start_x+18,start_y+line-7), eq_arr)
                line+=lineadder
            return

        # Drawing old values
        draw_table(354,253,item_send_biber_once,(50, 141, 168),font,once=True,compress_list=class_request_for(biberler.values()))
        draw_table(854,253,item_send_domates_once,(50, 141, 168),font,once=True,compress_list=class_request_for(domatesler.values()))
        draw_table(854,423,item_send_salatalik_once,(50, 141, 168),font,once=True,compress_list=class_request_for(salataliklar.values()))
        draw_table(854,528,patlican_once,(50, 141, 168),font,once=True,compress_list=Fiyatlar('patlican',patlican_once,patlican_bugun),single=True)
        
        # Drawing Today values and arrows
        draw_table(464,253,item_send_biber_bugun,(0, 0, 0),font,once=False)
        draw_table(964,253,item_send_domates_bugun,(0, 0, 0),font,once=False)
        draw_table(964,423,item_send_salatalik_bugun,(0, 0, 0),font,once=False)
        draw_table(964,528,patlican_bugun,(0, 0, 0),font,once=False,single=True)
        
        # Drawing title
        font = ImageFont.truetype("pillow/font.ttf", 58)
        draw.text((500,45), baslik, fill=(255, 255, 255), font=font,anchor='mm')
        
        img.save('static/yazili_resim.png')
        
        #       SQL SIDE        #

        def sql_edit(input_list,obje):
            idcount=1
            for item in input_list:
                with app.app_context():
                    item_to_update = db.session.get(obje, idcount)  
                    if item_to_update:
                        item_to_update.price = float(item)
                        db.session.commit()
                idcount+=1
            return
        
        sql_edit(list(item_send_biber_bugun.values())+list( item_send_domates_bugun.values())+list(item_send_salatalik_bugun.values())+[patlican_bugun],Sebze)
        
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
    if Heroku == False:
        app.run(debug=True)
    else:
        app.run()
    

