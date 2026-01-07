from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import json, os

app = Flask(__name__)

# -------------------------
# データベース設定
# -------------------------
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///essential_oils.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# -------------------------
# モデル定義
# -------------------------
class EssentialOil(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_ja = db.Column(db.String(100), nullable=False)
    name_en = db.Column(db.String(100))
    scientific_name = db.Column(db.String(100))
    manufacturer = db.Column(db.String(100))
    volume = db.Column(db.String(50))
    family = db.Column(db.String(100))
    origin = db.Column(db.String(200))   # 複数選択はカンマ区切り
    parts = db.Column(db.String(200))    # 複数選択
    method = db.Column(db.String(100))
    fragrance = db.Column(db.String(100))
    notes = db.Column(db.String(200))    # 複数選択

# -------------------------
# JSON データ移行
# -------------------------
DATA_FILE = "essential_oils.json"

with app.app_context():
    db.create_all()
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, encoding="utf-8") as f:
            data = json.load(f)
            for name, info in data.items():
                if not EssentialOil.query.filter_by(name_ja=name).first():
                    oil = EssentialOil(
                        name_ja=name,
                        name_en=info.get("英名",""),
                        scientific_name=info.get("学名",""),
                        manufacturer=info.get("メーカー",""),
                        volume=info.get("容量",""),
                        family=info.get("科名",""),
                        origin=",".join(info.get("産地",[])),
                        parts=",".join(info.get("抽出部位",[])),
                        method=info.get("抽出方法",""),
                        fragrance=info.get("香調",""),
                        notes=",".join(info.get("ノート",[]))
                    )
                    db.session.add(oil)
            db.session.commit()
        print("JSONからSQLiteへデータ移行完了")

# -------------------------
# 選択肢リスト
# -------------------------
manufacturer_list = ["&SH","9th perfum","AKARZ","Alomalamd","COONA","DR EBERHARDT",
                     "MIEUXSELECTION","ease","インセント","カリス成城","㈱アメージングクラフト",
                     "㈱バンガン","㈱メドウズアロマテラピープロダクツ","㈱フレーバーライフ",
                     "㈱生々堂","生活の木","無印良品","マンディムーン"]

volume_list = ["1ml","2ml","3ml","5ml","10ml","15ml","30ml","50ml","100ml","200ml"]
family_list = ["アオイ科","アヤメ科","イネ科","ウルシ科","エゴノキ科","カンラン科","クスノキ科",
               "クマツヅラ科","コショウ科","シソ科","スミレ科","セリ科","ナス科","バンレイシ科",
               "ヒノキ科","ビャクダン科","フウロソウ科","フトモモ科","マツ科","マメ科","モクセイ科",
               "バラ科","ショウガ科","ニクズク科","ハマビシ科","キク科"]
origin_list = ["ARG","AUS","BGR","BRA","CAN","CHN","ECU","EGY","FRA","GER","HUN",
               "IDN","IND","ITA","JPN","LKA","MAR","MDG","PER","PHL","PRY","SOM",
               "SLV","ESP","TUR","TUN","USA","VNM","ZAF"]
part_list = ["花","花弁","蕾","花穂", "全草","葉","新葉","若葉","果皮","果実","種子","果肉",
             "樹皮","根皮","根","樹脂","樹脂球","茎","枝","木部","樹冠","球根",
             "根茎","樹液","樹脂含有部"]
method_list = ["水蒸気蒸留","圧搾法","溶剤抽出","CO2抽出"]
fragrance_list = ["シトラス","ハーバル","スパイシー","フローラル","グリーン",
                  "ウッディ","レジン","アーシー","バルサミック"]
note_list = ["トップ","ミドル","ベース"]

# -------------------------
# 一覧・登録
# -------------------------
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method=="POST":
        original_id = request.form.get("original_id")
        name_ja = request.form.get("name_ja")
        name_en = request.form.get("name_en")
        name_lat = request.form.get("name_lat")
        manufacturer = request.form.get("manufacturer")
        volume = request.form.get("volume")
        family = request.form.get("family")
        origin = ",".join(request.form.getlist("origin"))
        parts = ",".join(request.form.getlist("part"))
        method = request.form.get("method")
        fragrance = request.form.get("fragrance")
        notes = ",".join(request.form.getlist("note"))

        if original_id:  # 編集
            oil = EssentialOil.query.get(int(original_id))
            if oil:
                oil.name_ja = name_ja
                oil.name_en = name_en
                oil.scientific_name = name_lat
                oil.manufacturer = manufacturer
                oil.volume = volume
                oil.family = family
                oil.origin = origin
                oil.parts = parts
                oil.method = method
                oil.fragrance = fragrance
                oil.notes = notes
        else:  # 新規
            oil = EssentialOil(
                name_ja=name_ja,
                name_en=name_en,
                scientific_name=name_lat,
                manufacturer=manufacturer,
                volume=volume,
                family=family,
                origin=origin,
                parts=parts,
                method=method,
                fragrance=fragrance,
                notes=notes
            )
            db.session.add(oil)
        db.session.commit()
        return redirect("/")

    oils = EssentialOil.query.all()
    return render_template("index.html",
                           oils=oils,
                           manufacturer_list=manufacturer_list,
                           volume_list=volume_list,
                           family_list=family_list,
                           origin_list=origin_list,
                           part_list=part_list,
                           method_list=method_list,
                           fragrance_list=fragrance_list,
                           note_list=note_list)

# -------------------------
# 編集
# -------------------------
@app.route("/edit/<int:oil_id>")
def edit(oil_id):
    oil = EssentialOil.query.get(oil_id)
    if oil:
        return render_template("index.html",
                               oils=EssentialOil.query.all(),
                               manufacturer_list=manufacturer_list,
                               volume_list=volume_list,
                               family_list=family_list,
                               origin_list=origin_list,
                               part_list=part_list,
                               method_list=method_list,
                               fragrance_list=fragrance_list,
                               note_list=note_list,
                               edit_oil=oil)
    return redirect("/")

# -------------------------
# 削除
# -------------------------
@app.route("/delete/<int:oil_id>")
def delete(oil_id):
    oil = EssentialOil.query.get(oil_id)
    if oil:
        db.session.delete(oil)
        db.session.commit()
    return redirect("/")

# -------------------------
# 実行
# -------------------------
if __name__=="__main__":
    app.run(host="0.0.0.0", port=10000)
