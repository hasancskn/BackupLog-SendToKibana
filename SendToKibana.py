import datetime
import csv
from elasticsearch import helpers, Elasticsearch


yil=str(datetime.datetime.now().year)
ay=str(datetime.datetime.now().month)
gun=str(datetime.datetime.now().day)
if ay=="1" or ay=="2" or ay=="3" or ay=="4" or ay=="5" or ay=="6" or ay=="7" or ay=="8" or ay=="9":
    ay="0"+ay
if gun=="1" or gun=="2" or gun=="3" or gun=="4" or gun=="5" or gun=="6" or gun=="7" or gun=="8" or gun=="9":
    gun="0"+gun

yil=yil[-2]+yil[-1]
log=yil+ay+gun
dosya='51216-116-2063950858-'+log+'-0000000000.log'
print(dosya)
logs=open(dosya,"r+")
logdosyasi=[]
logdosyasi=logs.read()
logdosyasi=logdosyasi.split(" ")
basarili=0
snapshoterror=0
for i in range (len(logdosyasi)):
    if logdosyasi[i]=="successfully":
        basarili=basarili+1
    elif logdosyasi[i]=="error":
        snapshoterror=snapshoterror+1
    #elif logdosyasi[i]=="successfully":

with open("elklog.csv","w",newline="") as f:
    yazici=csv.writer(f)
    yazici.writerow(['SnapshotError',snapshoterror])
    yazici.writerow(["Basarili islem",basarili])


print(snapshoterror)
print(basarili)

es=Elasticsearch()

headers = []
index = 0
index_name="netbackuplog"
doctype="logrecord"
es.indices.delete(index=index_name, ignore=[400, 404])
es.indices.create(index=index_name, ignore=400)
doc = {
    'Bilgi': 'Snapshot Error',
    'Veri': snapshoterror,
    'Log Zamanı': log,
    'Bilgi2':"Başarılı İşlemler",
    'Veri2':basarili,
    'Log Zamanı2':log
}
res = es.index(index=index_name, doc_type=doctype, id=1, body=doc)
print(res['result'])

res = es.get(index=index_name, doc_type=doctype, id=1)
print(res['_source'])

es.indices.refresh(index=index_name)

res = es.search(index=index_name, body={"query": {"match_all": {}}})
print("Got %d Hits:" % res['hits']['total']['value'])
for hit in res['hits']['hits']:
    print("%(Log Zamanı)s %(Bilgi)s: %(Veri)s" % hit["_source"])






