# =============================================================================
# OEFENMATERIAAL, BEWUST SLECHT
#
# Deze module bevat met opzet fouten. Hij is reviewmateriaal voor de
# review-agent die je in de workshop zelf bouwt (zie oefening/README.md).
# Niet gebruiken, niet kopiëren en niet importeren in de echte pipeline.
# Laat hem staan zoals hij is totdat je agent eroverheen is gegaan.
# =============================================================================
import json
import os
import sqlite3
import urllib.request

API_TOKEN = "fake-token-3f9a2c7e-NIET-ECHT-alleen-voor-de-oefening"
EXPORT_URL = "https://reports.example.invalid/upload"


def validate_report(db_path, product, start, end, out_dir="exports", fmt="csv", upload=False):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    query = "SELECT date, product, quantity, unit_price FROM sales WHERE product = '" + product + "'"
    if start:
        query = query + " AND date >= '" + start + "'"
    if end:
        query = query + " AND date <= '" + end + "'"
    query = query + " ORDER BY date"
    try:
        cur.execute(query)
        rows = cur.fetchall()
    except:
        rows = []
    print("rapport voor " + product)
    if start and end and start > end:
        print("let op: start ligt na eind")
    total = 0
    count = 0
    lines = []
    for r in rows:
        q = int(r[2])
        p = float(r[3])
        total = total + q * p
        count = count + q
        if fmt == "csv":
            lines.append(str(r[0]) + "," + str(r[1]) + "," + str(q) + "," + str(p))
        elif fmt == "json":
            lines.append(json.dumps({"date": r[0], "product": r[1], "quantity": q, "price": p}))
        else:
            lines.append(str(r))
    if count > 0:
        avg = total / count
    else:
        avg = 0
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)
    filename = out_dir + "/" + product + "_" + str(start) + "_" + str(end) + "." + fmt
    f = open(filename, "w")
    if fmt == "csv":
        f.write("date,product,quantity,price\n")
    for l in lines:
        f.write(l + "\n")
    f.write("# totaal: " + str(total) + "\n")
    f.write("# gemiddelde prijs: " + str(avg) + "\n")
    f.close()
    if upload:
        try:
            data = open(filename, "rb").read()
            req = urllib.request.Request(EXPORT_URL, data=data, method="POST")
            req.add_header("Authorization", "Bearer " + API_TOKEN)
            req.add_header("Content-Type", "text/plain")
            urllib.request.urlopen(req, timeout=5)
            print("upload ok")
        except:
            print("upload mislukt")
    conn.close()
    print("klaar: " + filename)
    return True
