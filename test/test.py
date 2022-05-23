import os
from shutil import ExecError
from time import sleep
import requests
import json

os.system('cls')
def test(testName,
         courseID = "100572160005",
         studentID = "100563018216282",
         teacherID = "10057216001",
         score = 90.0,
         GPA = 4.0,
         courseState = "true"):
    print("running test \""+ testName + "\" with parameters:")
    print("     courseID : " + courseID)
    print("     studentID : " + studentID)
    print("     score : " + str(score))
    print("     GPA : " + str(GPA))
    print("     teacherID : " + teacherID)
    formData = {
            "courseID": courseID,
            "studentID": studentID,
            "score" : score,
            "GPA": GPA,
            "pushType": "SR_Adjust",
            "teacherID": teacherID,
            "courseState": courseState
        }

    res = requests.post("http://127.0.0.1:8000/api/db_manage/adjust/", formData)
    try:
        id = json.loads(res.text)["txRet"]
    except Exception:
        print("test result is: " + res.text)
        if res.text == "can't modify!":
            if testName == "BlockedChangeTest":
                print("test \""+ testName + "\" succeed\n")
                return True
            else: ("test \""+ testName + "\" failed!\n" + res.text+"\n")

        elif res.text == "not exist!":
            if testName == "RecordNotExistTest":
                print("test \""+ testName + "\" succeed\n")
                return True
            else: ("test \""+ testName + "\" failed!\n" + res.text+"\n")

        elif res.text == "invalid format!":
            if testName == "InvalidScoreTest" \
                or testName == "InvalidGPATest" \
                or testName == "InvalidStateTest":
                    print("test \""+ testName + "\" succeed\n")
                    return True
            else: ("test \""+ testName + "\" failed!\n" + res.text+"\n")

        elif res.text == "sender identification error!":
            if testName == "TeacherNotExistTest" \
                or testName == "InvalidTeacherTest":
                    print("test \""+ testName + "\" succeed\n")
                    return True
            else: ("test \""+ testName + "\" failed!\n" + res.text+"\n")

        return False

    print(id)
    resStatus = "PENDING"
    while resStatus == "PENDING":
        sleep(1)
        res = requests.get("http://127.0.0.1:8000/api/db_manage/select/?type=txRet&teacherID="
                           +teacherID
                           +"&txID="
                           +id)
        resStatus = json.loads(res.text)["Status"]

    if resStatus == "MINED":
        print("test "+""+ "succeed\n")
        return True
    else:
        print("test "+""+ "failed!\n" + resStatus+ " " + json.loads(res.text)["Error"]+"\n")
        return False
all = 9
succ = 0
if test("InvalidScoreTest", score=100.1): succ += 1
if test("InvalidGPATest", GPA=4.01): succ += 1
if test("InvalidStateTest", courseState="false"): succ += 1
if test("InvalidTeacherTest", teacherID="10056216001"): succ += 1
if test("TeacherNotExistTest", teacherID="10057216002"): succ += 1
if test("RecordNotExistTest", courseID="100572160002"): succ += 1
if test("RecordNotExistTest", studentID="100563018216281"): succ += 1
if test("SuccessTest"): succ += 1
if test("BlockedChangeTest"): succ += 1

print("all "+str(all)+" tests finished, "+str(succ)+" succeed")

