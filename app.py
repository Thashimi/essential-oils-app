from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)
DATA_FILE = "essential_oils.json"

# JSON読み込み（空ファイル対策付き）
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        try:
            oils = json.load(f)
        except json.JSONDecodeError:
            oils = {}
else:
    oils = {}

# ドロップダウン選択肢
manufacturer_list = [
    "&SH","9th perfum","AKARZ","Alomalamd","COONA","DR EBERHARDT",
    "MIEUXSELECTION","ease","インセント","カリス成城","㈱アメージングクラフト",
    "㈱バンガン","㈱メドウズアロマテラピープロダクツ","㈱フレーバーライフ",
    "㈱生々堂","生活の木","無印良品","マンディムーン"
]

volume_list = ["1ml","2ml","3ml","5ml","10ml","15ml","30ml","50ml","100ml","200ml"]

family_list = [
    "アオイ科","アヤメ科","イネ科","ウルシ科","エゴノキ科","カンラン科","クスノキ科",
    "クマツヅラ科","コショウ科","シソ科","スミレ科","セリ科","ナス科","バンレイシ科",
    "ヒノキ科","ビャクダン科","フウロソウ科","フトモモ科","マツ科","マメ科","モクセイ科",
    "バラ科","ショウガ科","ニクズク科","ハマビシ科","キク科"
]

origin_list = [
    "ARG","AUS","BGR","BRA","CAN","CHN","ECU","EGY","FRA","GER","HUN",
    "IDN","IND","ITA","JPN","LKA","MAR","MDG","PER","PHL","PRY","SOM",
    "SLV","ESP","TUR","TUN","USA","VNM","ZAF"
]

part_list = [
    "花","花弁","蕾","花穂","葉","新葉","若葉","果皮","果実","種子","果肉",
    "樹皮","根皮","根","樹脂","樹脂球","茎","枝","木部","樹冠","球根",
    "根茎","樹液","樹脂含有部"
]

method_list = ["水蒸気蒸留","圧搾法","溶剤抽出","CO2抽出"]

fragrance_list = ["シトラス","ハーバル","スパイシー","フローラル","グリーン",
                  "ウッディ","レジン","アーシー","バルサミック"]

note_list = ["トップ","ミドル","ベース"]

# -------------------------
# ルート（一覧＋登録）
# -------------------------
@app.route("/", methods=["GET", "POST"])
def index():
    global oils
    if request.method == "POST":
        original_name = request.form.get("original_name")
        name_ja = request.form.get("name_ja")
        name_en = request.form.get("name_en")
        name_lat = request.form.get("name_lat")
        manufacturer = request.form.get("manufacturer")
        volume = request.form.get("volume")
        family = request.form.get("family")
        origin = request.form.getlist("origin")  # 複数選択
        part = request.form.get("part")
        method = request.form.get("method")
        fragrance = request.form.get("fragrance")
        note = request.form.getlist("note")      # 複数選択

        # 編集時に名前変更された場合、古いキーを削除
        if original_name and original_name != name_ja and original_name in oils:
            oils.pop(original_name)

        oils[name_ja] = {
            "英名": name_en,
            "学名": name_lat,
            "メーカー": manufacturer,
            "容量": volume,
            "科名": family,
            "産地": origin,
            "抽出部位": part,
            "抽出方法": method,
            "香調": fragrance,
            "ノート": note
        }

        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(oils, f, ensure_ascii=False, indent=2)

        return redirect("/")

    return render_template(
        "index.html",
        oils=oils,
        manufacturer_list=manufacturer_list,
        volume_list=volume_list,
        family_list=family_list,
        origin_list=origin_list,
        part_list=part_list,
        method_list=method_list,
        fragrance_list=fragrance_list,
        note_list=note_list
    )

# -------------------------
# 削除
# -------------------------
@app.route("/delete/<name_ja>")
def delete(name_ja):
    global oils
    if name_ja in oils:
        oils.pop(name_ja)
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(oils, f, ensure_ascii=False, indent=2)
    return redirect("/")

# -------------------------
# 編集
# -------------------------
@app.route("/edit/<name_ja>")
def edit(name_ja):
    global oils
    if name_ja in oils:
        oil = oils[name_ja]
        return render_template(
            "index.html",
            oils=oils,
            manufacturer_list=manufacturer_list,
            volume_list=volume_list,
            family_list=family_list,
            origin_list=origin_list,
            part_list=part_list,
            method_list=method_list,
            fragrance_list=fragrance_list,
            note_list=note_list,
            edit_oil={"name": name_ja, **oil}
        )
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

