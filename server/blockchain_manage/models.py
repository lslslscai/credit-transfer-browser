from time import sleep
from django.db import models
from aelf_sdk.credit_transfer_contract_pb2 import School, SRT, Teacher, CourseInfo, CourseRecord, SRUploadInput, SRModifyInput, SRDropInput
from aelf.types_pb2 import Address
from aelf_sdk import AElf
from google.protobuf.wrappers_pb2 import StringValue

import pickle

class cr_handler:
    def __init__(self, priKey, ip) -> None:
        self.aelfChain = AElf('http://'+ip)
        self._priKey = priKey
        self.contractAddress = str("2LUmicHyH4RXrMjG4beDwuDsiWJESyLkgkwPdGTR8kahRzq5XS")

    def getTransactionResult(self, input):
        ret = self.aelfChain.get_transaction_result(input)
        print(type(ret))

        formattedRet = dict()
        return ret

    def SRT_Create(self, input):
        transfer_input = StringValue()
        transfer_input.value = input["studentID"]

        transaction = self.aelfChain.create_transaction(
            self.contractAddress,
            "SRT_Create",
            transfer_input.SerializeToString()
        )
        transaction = self.aelfChain.sign_transaction(self._priKey, transaction)
        result = self.aelfChain.send_transaction(transaction.SerializePartialToString().hex())

        return result['TransactionId']

    def Course_Create(self, input):
        transfer_input = CourseInfo()
        transfer_input.isCompulsory = input["isCompulsory"]
        transfer_input.courseID = input["courseID"]
        transfer_input.isValid = input["isValid"]
        transfer_input.courseType = input["courseType"]
        transfer_input.credit = input["credit"]
        print("sending transaction")
        transaction = self.aelfChain.create_transaction(
            self.contractAddress,
            "Course_Create",
            transfer_input.SerializeToString()
        )
        transaction = self.aelfChain.sign_transaction(self._priKey, transaction)
        result = self.aelfChain.send_transaction(transaction.SerializePartialToString().hex())

        return result['TransactionId']

    def Course_Adjust(self, input):
        transfer_input = CourseInfo()
        transfer_input.isCompulsory = input["isCompulsory"]
        transfer_input.courseID = input["courseID"]
        transfer_input.isValid = input["isValid"]
        transfer_input.courseType = input["courseType"]
        transfer_input.credit = input["credit"]
        print("sending transaction")
        transaction = self.aelfChain.create_transaction(
            self.contractAddress,
            "Course_Adjust",
            transfer_input.SerializeToString()
        )
        transaction = self.aelfChain.sign_transaction(self._priKey, transaction)
        result = self.aelfChain.send_transaction(transaction.SerializePartialToString().hex())

        return result['TransactionId']

    def SRT_Adjust(self, input):
        raw = self.get_SRT(input["studentID"])
        print(raw)
        transfer_input = SRT()
        transfer_input.studentID = input["studentID"]
        transfer_input.rating = raw["rating"]
        transfer_input.state = input["studentState"]

        transaction = self.aelfChain.create_transaction(
            self.contractAddress,
            "SRT_Adjust",
             transfer_input.SerializeToString()
        )
        transaction = self.aelfChain.sign_transaction(self._priKey, transaction)
        result = self.aelfChain.send_transaction(transaction.SerializePartialToString().hex())

        return result['TransactionId']

    def get_SRT(self, input):
        transfer_input = StringValue()
        transfer_input.value = input
        transaction = self.aelfChain.create_transaction(
            self.contractAddress,
            "get_SRT",
             transfer_input.SerializeToString()
        )
        self.aelfChain.sign_transaction(self._priKey, transaction)
        result = self.aelfChain.execute_transaction(transaction)

        ret = SRT()
        ret.ParseFromString(bytes.fromhex(result.decode()))
        formattedRet = self.decodeData(ret, "SRT")
        return formattedRet

    def get_CourseInfo(self, input):
        transfer_input = StringValue()
        transfer_input.value = input
        transaction = self.aelfChain.create_transaction(
            self.contractAddress,
            "get_CourseInfo",
             transfer_input.SerializeToString()
        )
        self.aelfChain.sign_transaction(self._priKey, transaction)
        result = self.aelfChain.execute_transaction(transaction)

        ret = CourseInfo()
        ret.ParseFromString(bytes.fromhex(result.decode()))
        formattedRet = self.decodeData(ret, "CourseInfo")
        return formattedRet

    def SR_Adjust(self, input):
        transfer_input = SRModifyInput()
        transfer_input.courseID = input["courseID"]
        transfer_input.studentID = input["studentID"]
        transfer_input.state = input["courseState"]
        transfer_input.score = int(input["score"]*100)
        transfer_input.GPA = int(input["GPA"]*100)
        print("sending transaction")
        transaction = self.aelfChain.create_transaction(
            self.contractAddress,
            "SR_Adjust",
            transfer_input.SerializeToString()
        )
        transaction = self.aelfChain.sign_transaction(self._priKey, transaction)
        result = self.aelfChain.send_transaction(transaction.SerializePartialToString().hex())
        print(result)
        return result['TransactionId']

    def get_School(self, input):
        transfer_input = StringValue()
        transfer_input.value = input
        transaction = self.aelfChain.create_transaction(
            self.contractAddress,
            "get_School",
            transfer_input.SerializeToString()
        )
        self.aelfChain.sign_transaction(self._priKey, transaction)
        result = self.aelfChain.execute_transaction(transaction)

        ret = School()
        ret.ParseFromString(bytes.fromhex(result.decode()))
        formattedRet = self.decodeData(ret, "School")
        return formattedRet

    def decodeData(self, content, type):
        ret = dict()
        if type == "SRT":
            ret["studentID"] = content.studentID
            ret["state"] = content.state
            ret["rating"] = content.rating
            return ret
        if type == "School":
            ret["schoolID"] = content.schoolID
            ret["schoolAddress"] = content.schoolAddress["value"]
            ret["rating"] = content.rating
            return ret
        if type == "courseInfo":
            ret["courseID"] = content.coureseID
            ret["isCompulsory"] = content.isCompulsory
            ret["courseType"] = content.courseType
            ret["isValid"] = content.isValid
            return ret
        if type == "courseRecord":
            ret["courseID"] = content.courseID
            ret["studentID"] = content.studentID
            ret["protocol"] = content.protocol
            ret["state"] = content.state
            ret["GPA"] = content.GPA
            ret["score"] = content.score
            ret["note"] = content.note
            return ret