from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import os, json, csv
from datetime import date, datetime, timezone
from django.core.files.storage import FileSystemStorage
from lxml import etree
import xml.etree.ElementTree as ET



def statusPruefung(request):
    accname = request.GET.get("accname", "")
    username = request.GET.get("username", "")
    pwd = request.GET.get("pwd", "")
    userPath = f"/var/www/django-project/Horus/data/user/userjson/{accname}.json"


    if not os.path.isfile(userPath):
#        if username != "":
#            username1 = username
#        else:
#            username1 = "Horus-User (aendere deinen Usernamen unter Options>Profil>Stammdaten)"

        emptTmpl = {
            "username": username,
            "pwd": pwd,
            "status": "normal",
                "antragGestellt": False,
                "gesperrt": False,
                "module": []
        }

        with open(userPath, "w", encoding="utf-8") as file:
            tmplDump = json.dumps(emptTmpl, indent = 2)
            file.write(tmplDump)
    
    
    with open(userPath, "r", encoding="utf-8") as file:
        userData = file.read()

    userData = json.loads(userData)  

    if userData["gesperrt"] == True:
        return HttpResponseRedirect("http://[2001:7c0:2320:2:f816:3eff:fe82:34b2]/Horus/Gesperrt.html")

    else:
        if userData["pwd"] == pwd:

            if userData["status"] == "normal":
                return HttpResponseRedirect(f"/Horus/Home?accname={accname}&pwd={pwd}")
            elif userData["status"] == "VIP":
                return HttpResponseRedirect(f"/Horus/VIP?accname={accname}&pwd={pwd}")
            elif userData["status"] == "admin":
                return HttpResponseRedirect(f"/Horus/Admin?accname={accname}&pwd={pwd}")
        


        else:
            return HttpResponseRedirect("http://[2001:7c0:2320:2:f816:3eff:fe82:34b2]/Horus/Wrong.html")


def VIP(request):
    accname = request.GET.get("accname", "")
    pwd = request.GET.get("pwd", "")
    modulwahl = request.GET.get("modulwahl", "")
    aktuellesDatum = request.GET.get("aktuellesDatum", "")
    dauer = request.GET.get("dauer", "")
    comment = request.GET.get("comment", "")
    eintragen = request.GET.get("eintragen", False)


    userPath = f"/var/www/django-project/Horus/data/user/userjson/{accname}.json"
    modulPath = "/var/www/django-project/Horus/data/Module.json"


    with open(userPath, "r", encoding="utf-8") as file:
        userData = json.load(file)

    with open(modulPath, "r", encoding="utf-8") as file:
        modulData = json.load(file)


    # Neuen Eintrag hinzufügen
    if eintragen:
        module_vorhanden = False

        for item in userData["module"]:
            if item["modulname"] == modulwahl:
                module_vorhanden = True
                item["lernzeit"] = int(item["lernzeit"]) +int(dauer)
                item["arbeitsberichte"].append({
                "datum": aktuellesDatum,
                "dauer": dauer,
                "text": comment
            })
 #           break

        if not module_vorhanden:
            userData["module"].append({
                "modulname": modulwahl,
                "lernzeit": int(dauer),
                "arbeitsberichte": [{
                    "datum": aktuellesDatum,
                    "dauer": dauer,
                    "text": comment
                }]
            })

        with open(userPath, "w", encoding="utf-8") as file:
            file.write(json.dumps(userData, indent=2))
    
    gesamtLernzeit = 0
    for modul in userData["module"]:
        gesamtLernzeit += int(modul["lernzeit"])
    
    datenProModul = []
    for modul in userData["module"]:
        zeitanteilInProzent = int(modul["lernzeit"])/(gesamtLernzeit/100)
        datenProModul.append({
            "modulname": modul["modulname"],
            "Zeitanteil": modul["lernzeit"],
            "ZeitanteilInProzent": round(zeitanteilInProzent, 2)
        })


    vars = {
        "Accname": accname,
        "Name": userData["username"],
        "PWD": userData["pwd"],
        "modulDaten": userData["module"],
        "Modulauswahl": modulData,
        "gesamtLernzeit": gesamtLernzeit,
        "datenProModul": datenProModul,
    }

    return render(request, "/var/www/django-project/Horus/templates/Horus/Horus-VIP.html", vars)

def normal(request):
    accname = request.GET.get("accname", "")
    pwd = request.GET.get("pwd", "")
    modulwahl = request.GET.get("modulwahl", "")
    aktuellesDatum = request.GET.get("aktuellesDatum", "")
    dauer = request.GET.get("dauer", "")
    comment = request.GET.get("comment", "")
    eintragen = request.GET.get("eintragen", False)


    userPath = f"/var/www/django-project/Horus/data/user/userjson/{accname}.json"
    modulPath = "/var/www/django-project/Horus/data/Module.json"


    with open(userPath, "r", encoding="utf-8") as file:
        userData = json.load(file)

    with open(modulPath, "r", encoding="utf-8") as file:
        modulData = json.load(file)


    # Neuen Eintrag hinzufügen
    if eintragen:
        module_vorhanden = False

        for item in userData["module"]:
            if item["modulname"] == modulwahl:
                module_vorhanden = True
                item["lernzeit"] = int(item["lernzeit"]) +int(dauer)
                item["arbeitsberichte"].append({
                "datum": aktuellesDatum,
                "dauer": dauer,
                "text": comment
            })
 #           break

        if not module_vorhanden:
            userData["module"].append({
                "modulname": modulwahl,
                "lernzeit": int(dauer),
                "arbeitsberichte": [{
                    "datum": aktuellesDatum,
                    "dauer": dauer,
                    "text": comment
                }]
            })

        with open(userPath, "w", encoding="utf-8") as file:
            file.write(json.dumps(userData, indent=2))
    
    gesamtLernzeit = 0
    for modul in userData["module"]:
        gesamtLernzeit += int(modul["lernzeit"])
    
    datenProModul = []
    for modul in userData["module"]:
        zeitanteilInProzent = int(modul["lernzeit"])/(gesamtLernzeit/100)
        datenProModul.append({
            "modulname": modul["modulname"],
            "Zeitanteil": modul["lernzeit"],
            "ZeitanteilInProzent": round(zeitanteilInProzent, 2)
        })


    vars = {
        "Accname": accname,
        "Name": userData["username"],
        "PWD": userData["pwd"],
        "modulDaten": userData["module"],
        "Modulauswahl": modulData,
        "gesamtLernzeit": gesamtLernzeit,
        "datenProModul": datenProModul,
    }

    return render(request, "/var/www/django-project/Horus/templates/Horus/Horus-Home.html", vars)

def profilVIP(request):
    accname = request.GET.get("accname", "")
    pwd = request.GET.get("pwd", "")
    statuswechsel = request.GET.get("statuswechsel", "")
    changeUsername = request.GET.get("changeUsername", False)
    changePassword = request.GET.get("changePassword", False)


    userPath = f"/var/www/django-project/Horus/data/user/userjson/{accname}.json"
    modulPath = "/var/www/django-project/Horus/data/Module.json"


    with open(userPath, "r", encoding="utf-8") as file:
        userData = json.load(file)

    with open(modulPath, "r", encoding="utf-8") as file:
        modulData = json.load(file)
        

    if changeUsername:
        userData["username"] = changeUsername
        with open(userPath, "w", encoding="utf-8") as file:
            file.write(json.dumps(userData, indent=2))

    if changePassword:
        userData["pwd"] = changePassword
        with open(userPath, "w", encoding="utf-8") as file:
            file.write(json.dumps(userData, indent=2))

    if statuswechsel:
        userData["antragGestellt"] = True
        with open(userPath, "w", encoding="utf-8") as file:
            file.write(json.dumps(userData, indent=2))


    vars = {
        "Accname": accname,
        "Name": userData["username"],
        "PWD": userData["pwd"],
        "modulDaten": userData["module"],
        "antragGestellt": userData["antragGestellt"],
        "Modulauswahl": modulData,
    }


    return render(request, "/var/www/django-project/Horus/templates/Horus/Horus-VIP-Profil.html", vars)

def VIPTools(request):
    accname = request.GET.get("accname", "")
    accountname = request.POST.get("accname")
    pwd = request.GET.get("pwd", "")
    dauer = request.GET.get("dauer", "")
    datenUmwandeln = request.GET.get("datenUmwandeln", False)

    if request.method == 'POST' and request.FILES['updateDatei']:
        myfile = request.FILES['updateDatei']
        fs = FileSystemStorage(location='/var/www/django-project/Horus/data/user/userjson')
        filename = f"{accountname}.json"
        if fs.exists(filename):
            fs.delete(filename)
        fs.save(filename, myfile)
        #uploaded_file_url = f"/userjson/{accname}.json"
        return HttpResponseRedirect(f"http://[2001:7c0:2320:2:f816:3eff:fe82:34b2]/Horus/LogIn.html")

    else:


        userPath = f"/var/www/django-project/Horus/data/user/userjson/{accname}.json"
        modulPath = "/var/www/django-project/Horus/data/Module.json"


        with open(userPath, "r", encoding="utf-8") as file:
            userData = json.load(file)

        with open(modulPath, "r", encoding="utf-8") as file:
            modulData = json.load(file)

        
        class Translator:
            def __init__(self, accname):
                self.jsonPath = f"/var/www/html/Horus/user/userjson/{accname}.json"
                self.xmlPath = f"/var/www/html/Horus/user/userxml/{accname}.xml"
                self.csvPath = f"/var/www/html/Horus/user/usercsv/{accname}.csv"

                self.__copyJSON()
                self.__translateJSONToXML()
                self.__translateJSONToCsv()

            def __copyJSON(self):
                with open(self.jsonPath, "w") as jsonFile:
                    jsonFile.write(json.dumps(userData, indent=2))

            def __translateJSONToXML(self):
                root = ET.Element("Accountdaten", attrib={
                    "name": userData["username"],
                    "pwd": userData["pwd"],
                    "status": userData["status"]
                })

                modulElement = ET.SubElement(root, "Module")
                for modul in userData["module"]:
                    moduleinzel = ET.SubElement(modulElement, "Modul", attrib={"name": modul["modulname"], "Gesamtzeit": str(modul["lernzeit"])})
                    for eintrag in modul["arbeitsberichte"]:
                        datum = eintrag["datum"]
                        dauer = eintrag["dauer"]
                        inhalt = eintrag["text"]
                        ET.SubElement(moduleinzel, "Eintrag", attrib={"datum": datum, "dauer": dauer}).text = inhalt

                tree = ET.ElementTree(root)

                with open(self.xmlPath, "wb") as xmlFile:
                    tree.write(xmlFile, encoding="utf-8", xml_declaration=True)
            
            def __translateJSONToCsv(self):
                with open(self.csvPath, mode='w', newline='', encoding='utf-8') as csvFile:
                    csvWriter = csv.writer(csvFile)
                    
                    csvWriter.writerow(['Username', 'Passwort', 'Status', 'Modul', 'Datum', 'Dauer (in Min)', 'Kommentar'])
                    
                    for modul in userData["module"]:
                        for eintrag in modul["arbeitsberichte"]:
                            datum = eintrag["datum"]
                            dauer = eintrag["dauer"]
                            inhalt = eintrag["text"]
                            
                            csvWriter.writerow([userData["username"], userData["pwd"], userData["status"], modul["modulname"], datum, dauer, inhalt])


        if datenUmwandeln:
            Translator(accname)


        vars = {
            "Accname": accname,
            "Name": userData["username"],
            "PWD": userData["pwd"],
            "modulDaten": userData["module"],
            "Modulauswahl": modulData,
        }

        return render(request, "/var/www/django-project/Horus/templates/Horus/Horus-VIP-Tools.html", vars)

def profil(request):
    accname = request.GET.get("accname", "")
    pwd = request.GET.get("pwd", "")
    statuswechsel = request.GET.get("statuswechsel", "")
    changeUsername = request.GET.get("changeUsername", False)
    changePassword = request.GET.get("changePassword", False)


    userPath = f"/var/www/django-project/Horus/data/user/userjson/{accname}.json"
    modulPath = "/var/www/django-project/Horus/data/Module.json"


    with open(userPath, "r", encoding="utf-8") as file:
        userData = json.load(file)

    with open(modulPath, "r", encoding="utf-8") as file:
        modulData = json.load(file)
        

    if changeUsername:
        userData["username"] = changeUsername
        with open(userPath, "w", encoding="utf-8") as file:
            file.write(json.dumps(userData, indent=2))

    if changePassword:
        userData["pwd"] = changePassword
        with open(userPath, "w", encoding="utf-8") as file:
            file.write(json.dumps(userData, indent=2))

    if statuswechsel:
        userData["antragGestellt"] = True
        with open(userPath, "w", encoding="utf-8") as file:
            file.write(json.dumps(userData, indent=2))


    vars = {
        "Accname": accname,
        "Name": userData["username"],
        "PWD": userData["pwd"],
        "modulDaten": userData["module"],
        "antragGestellt": userData["antragGestellt"],
        "Modulauswahl": modulData,
    }

    return render(request, "/var/www/django-project/Horus/templates/Horus/Horus-Profil.html", vars)

def profilAdmin(request):
    accname = request.GET.get("accname", "")
    pwd = request.GET.get("pwd", "")
    changeUsername = request.GET.get("changeUsername", False)
    changePassword = request.GET.get("changePassword", False)


    userPath = f"/var/www/django-project/Horus/data/user/userjson/{accname}.json"
    modulPath = "/var/www/django-project/Horus/data/Module.json"


    with open(userPath, "r", encoding="utf-8") as file:
        userData = json.load(file)

    with open(modulPath, "r", encoding="utf-8") as file:
        modulData = json.load(file)
        

    if changeUsername:
        userData["username"] = changeUsername
        with open(userPath, "w", encoding="utf-8") as file:
            file.write(json.dumps(userData, indent=2))

    if changePassword:
        userData["pwd"] = changePassword
        with open(userPath, "w", encoding="utf-8") as file:
            file.write(json.dumps(userData, indent=2))


    vars = {
        "Accname": accname,
        "Name": userData["username"],
        "PWD": userData["pwd"],
        "modulDaten": userData["module"],
        "Modulauswahl": modulData,
    }

    return render(request, "/var/www/django-project/Horus/templates/Horus/Horus-Admin-Profil.html", vars)

def adminTools(request):
    accname = request.GET.get("accname", "")
    accountname = request.POST.get("accname")
    pwd = request.GET.get("pwd", "")
    dauer = request.GET.get("dauer", "")
    modulname = request.GET.get("modulname", "")
    sperre = request.GET.get("sperre", "")
    freigabe = request.GET.get("freigabe", "")
    ablehnen = request.GET.get("ablehnen", "")
    genehmigen = request.GET.get("genehmigen", "")
    datenUmwandeln = request.GET.get("datenUmwandeln", False)
    addmodul = request.GET.get("addmodul", False)
    deletemodul = request.GET.get("deletemodul", False)

    if request.method == 'POST' and request.FILES['updateDatei']:
        myfile = request.FILES['updateDatei']
        fs = FileSystemStorage(location='/var/www/django-project/Horus/data/user/userjson')
        filename = f"{accountname}.json"
        if fs.exists(filename):
            fs.delete(filename)
        fs.save(filename, myfile)
        #uploaded_file_url = f"/userjson/{accname}.json"
        return HttpResponseRedirect(f"http://[2001:7c0:2320:2:f816:3eff:fe82:34b2]/Horus/LogIn.html")

    else:


        userPath = f"/var/www/django-project/Horus/data/user/userjson/{accname}.json"
        modulPath = "/var/www/django-project/Horus/data/Module.json"        

        with open(userPath, "r", encoding="utf-8") as file:
            userData = json.load(file)

        with open(modulPath, "r", encoding="utf-8") as file:
            modulData = json.load(file)




        if datenUmwandeln:

            #JSON#######################################################################################################
            jsonUserPath = f"/var/www/html/Horus/user/userjson/{accname}.json"
            with open(jsonUserPath, "w") as jsonFile:
                jsonFile.write(json.dumps(userData, indent=2))


            #XML########################################################################################################
            xmlUserPath = f"/var/www/html/Horus/user/userxml/{accname}.xml"

            root = ET.Element("Accountdaten", attrib={
                "name": userData["username"],
                "pwd": userData["pwd"],
                "status": userData["status"]
            })

            modulElement = ET.SubElement(root, "Module")
            for modul in userData["module"]:
                moduleinzel = ET.SubElement(modulElement, "Modul", attrib={"name": modul["modulname"], "Gesamtzeit": str(modul["lernzeit"])})
                for eintrag in modul["arbeitsberichte"]:
                    datum = eintrag["datum"]
                    dauer = eintrag["dauer"]
                    inhalt = eintrag["text"]
                    ET.SubElement(moduleinzel, "Eintrag", attrib={"datum": datum, "dauer": dauer}).text = inhalt

            tree = ET.ElementTree(root)

            with open(xmlUserPath, "wb") as xmlFile:
                tree.write(xmlFile, encoding="utf-8", xml_declaration=True)
            
            #CSV########################################################################################################
            csvUserPath = f"/var/www/html/Horus/user/usercsv/{accname}.csv"

            with open(csvUserPath, mode='w', newline='', encoding='utf-8') as csvFile:
                csvWriter = csv.writer(csvFile)
                
                csvWriter.writerow(['Username', 'Passwort', 'Status', 'Modul', 'Datum', 'Dauer (in Min)', 'Kommentar'])
                
                for modul in userData["module"]:
                    for eintrag in modul["arbeitsberichte"]:
                        datum = eintrag["datum"]
                        dauer = eintrag["dauer"]
                        inhalt = eintrag["text"]
                        
                        csvWriter.writerow([userData["username"], userData["pwd"], userData["status"], modul["modulname"], datum, dauer, inhalt])

        if addmodul:
            if modulname not in modulData:
                modulData.append(modulname)
                with open(modulPath, "w", encoding="utf-8") as file:
                    file.write(json.dumps(modulData, indent=2))

        if deletemodul:
            modulname = request.GET.get("modulname", "").strip()
            if modulname in modulData:
                modulData.remove(modulname)

            with open(modulPath, "w", encoding="utf-8") as file:
                    file.write(json.dumps(modulData, indent=2))
        
        if sperre:
            sperrPath = f"/var/www/django-project/Horus/data/user/userjson/{sperre}"
            with open(sperrPath, "r", encoding="utf-8") as file:
                sperrData = json.load(file)
            sperrData["gesperrt"] = True
            with open(sperrPath, "w", encoding="utf-8") as file:
                file.write(json.dumps(sperrData, indent=2))
        
        if freigabe:
            freePath = f"/var/www/django-project/Horus/data/user/userjson/{freigabe}"
            with open(freePath, "r", encoding="utf-8") as file:
                freeData = json.load(file)
            freeData["gesperrt"] = False
            with open(freePath, "w", encoding="utf-8") as file:
                file.write(json.dumps(freeData, indent=2))

        if genehmigen:
            allowPath = f"/var/www/django-project/Horus/data/user/userjson/{genehmigen}"
            with open(allowPath, "r", encoding="utf-8") as file:
                allowData = json.load(file)

            if allowData["status"] == "normal":
                allowData["status"] = "VIP"
            elif allowData["status"] == "VIP":
                allowData["status"] = "admin"
            
            allowData["antragGestellt"] = False
            with open(allowPath, "w", encoding="utf-8") as file:
                file.write(json.dumps(allowData, indent=2))
        
        if ablehnen:
            refusePath = f"/var/www/django-project/Horus/data/user/userjson/{ablehnen}"
            with open(refusePath, "r", encoding="utf-8") as file:
                refuseData = json.load(file)
            
            refuseData["antragGestellt"] = False

            with open(refusePath, "w", encoding="utf-8") as file:
                file.write(json.dumps(refuseData, indent=2))
        


        SearchContainer = []
        antragVIP = []
        antragAdmin = []
        allUser = os.listdir("/var/www/django-project/Horus/data/user/userjson/")
        userDataPath = "/var/www/django-project/Horus/data/user/userjson/"
        
        for user in allUser:
            filePath = os.path.join(userDataPath, user)
            with open(filePath, "r", encoding="utf-8") as file:
                fileUser = json.load(file)
                data= {
                    "filename": user,
                    "accname": accname,
                    "username": fileUser["username"],
                    "gesperrt": fileUser["gesperrt"],
                    "antrag": fileUser["antragGestellt"],
                    "status": fileUser["status"],
                }
                if user != f"{accname}.json":
                    if fileUser["username"] != "Administrator (Überschrieben)":
                        SearchContainer.append(data)
                        if fileUser["status"] == "normal" and fileUser["antragGestellt"] == True:
                            antragVIP.append(data)
                        elif fileUser["status"] == "VIP" and fileUser["antragGestellt"] == True:
                            antragAdmin.append(data)
                    else:
                        pass
                else:
                    pass




        vars = {
            "Accname": accname,
            "Name": userData["username"],
            "PWD": userData["pwd"],
            "modulDaten": userData["module"],
            "Modulauswahl": modulData,
            "SearchContainer": SearchContainer,
            "antragVIP": antragVIP,
            "antragAdmin": antragAdmin,
        }





        return render(request, "/var/www/django-project/Horus/templates/Horus/Horus-Admin-Tools.html", vars)

def admin(request):
    accname = request.GET.get("accname", "")
    pwd = request.GET.get("pwd", "")
    modulwahl = request.GET.get("modulwahl", "")
    aktuellesDatum = request.GET.get("aktuellesDatum", "")
    dauer = request.GET.get("dauer", "")
    comment = request.GET.get("comment", "")
    eintragen = request.GET.get("eintragen", False)


    userPath = f"/var/www/django-project/Horus/data/user/userjson/{accname}.json"
    modulPath = "/var/www/django-project/Horus/data/Module.json"


    with open(userPath, "r", encoding="utf-8") as file:
        userData = json.load(file)

    with open(modulPath, "r", encoding="utf-8") as file:
        modulData = json.load(file)





    # Neuen Eintrag hinzufügen
    if eintragen:
        module_vorhanden = False

        for item in userData["module"]:
            if item["modulname"] == modulwahl:
                module_vorhanden = True
                item["lernzeit"] = int(item["lernzeit"]) +int(dauer)
                item["arbeitsberichte"].append({
                "datum": aktuellesDatum,
                "dauer": dauer,
                "text": comment
            })
 #           break

        if not module_vorhanden:
            userData["module"].append({
                "modulname": modulwahl,
                "lernzeit": int(dauer),
                "arbeitsberichte": [{
                    "datum": aktuellesDatum,
                    "dauer": dauer,
                    "text": comment
                }]
            })

        with open(userPath, "w", encoding="utf-8") as file:
            file.write(json.dumps(userData, indent=2))
    
    gesamtLernzeit = 0
    for modul in userData["module"]:
        gesamtLernzeit += int(modul["lernzeit"])
    
    datenProModul = []
    for modul in userData["module"]:
        zeitanteilInProzent = int(modul["lernzeit"])/(gesamtLernzeit/100)
        datenProModul.append({
            "modulname": modul["modulname"],
            "Zeitanteil": modul["lernzeit"],
            "ZeitanteilInProzent": round(zeitanteilInProzent, 2)
        })


    vars = {
        "Accname": accname,
        "Name": userData["username"],
        "PWD": userData["pwd"],
        "modulDaten": userData["module"],
        "Modulauswahl": modulData,
        "gesamtLernzeit": gesamtLernzeit,
        "datenProModul": datenProModul,
    }
    return render(request, "/var/www/django-project/Horus/templates/Horus/Horus-Admin.html", vars)
