#!/usr/bin/python3

import os
import sys

import getpass
import logging

import hashlib
import re
import time

import json
import requests



class CrawlerError(Exception):
  def name(self):
    return type(self).__name__

class DownloadError(CrawlerError):
  pass

class JsonError(CrawlerError):
  pass

class ParserError(CrawlerError):
  pass



class Json(dict):
  def __init__(self, filename, *args, **kwargs):
    super().__init__(*args, **kwargs)

    self.filename = filename
    if os.path.exists(self.filename):
      with open(self.filename, "r", encoding="utf-8") as f:
        try:
          self.update(json.load(f))
        except json.decoder.JSONDecodeError as e:
          raise JsonError(e)

  def flush(self):
    with open(self.filename, "w", encoding="utf-8") as f:
      json.dump(self, f)


class Config(Json):
  def fetch(self, path, params={}):
    for k in params:
      if params[k] is None:
        params[k] = self["params"][k]
    try:
      return json.loads(requests.get(self["location"]["origin"] + self["location"]["pathname"].format(path, self["data"]["token"]), params=params).text)
    except requests.exceptions.HTTPError as e:
      raise DownloadError("{{ url: {}, e: {} }}", path, e)
    except json.decoder.JSONDecodeError as e:
      raise JsonError("{{ url: {}, e: {} }}", path, e)

  def login(self):
    if "token" not in self["data"] or self.fetch("User/saveLastLogin")["status"] == 100001:
      try:
        loginInfo = json.loads(requests.post(self["location"]["origin"] + self["location"]["login"], data=self["data"]).text)
        logging.info("loginInfo: {}".format(loginInfo))
        self["params"]["uid"] = loginInfo["message"]["uid"]
        self["data"]["token"] = loginInfo["message"]["token"]
      except json.decoder.JSONDecodeError as e:
        raise JsonError("{{ url: {}, e: {} }}".format(self["location"]["login"], e))
      except KeyError:
        raise JsonError("Failed to get login.message from {}".format(loginInfo))
      logging.debug("Update token")
      config.flush()

  def updateAccount(self):
    if "data" not in self:
      self["data"] = {}
    if "email" not in self["data"]:
      self["data"]["email"] = input("Input email    (Press Ctrl+C to cancel): ")
      logging.debug("Update email")
      self.flush()
      print()
    if "password" not in self["data"]:
      self["data"]["password"] = hashlib.md5(getpass.getpass("Input password (Press Ctrl+C to cancel): ").encode()).hexdigest()
      logging.debug("Update password")
      self.flush()
      print()

    self.login()


def downloadFile(url, filename):
  if os.path.exists(filename):
    return
  try:
    url = url.split("?", 1)[0]
    r = requests.get(url, timeout=tuple(config["timeout"]))
    r.raise_for_status()
    with open(filename, "wb") as f:
      f.write(r.content)
  except requests.exceptions.HTTPError as e:
    print("download ('{}') HTTPError: {}".format(url, r.status_code))
    with open("{}.{}".format(filename, "xml"), "wb") as f:
      f.write(r.content)


def fetchHomeworks():
  def fetchHomeworksPage(page):
    publishList = config.fetch("Work/getPublishList", params={"p": page + 1, "sort_order": "publish_at", "sort": "ASC", "plan_id": None, "uid": None, "cid": None})
    logging.info("publishList: {}".format(publishList))
    try:
      return [[row[k] for k in ["homework_id", "plan_title"]] for row in publishList["message"]["rows"]], publishList["message"]["totalPages"]
    except KeyError:
      raise JsonError("Failed to get publishList")

  homeworks, totalPages = fetchHomeworksPage(0)
  for page in range(1, totalPages):
    homeworks.extend(fetchHomeworksPage(page)[0])

  return homeworks


def fetchSubmitStudents():
  def fetchSubmitStudentsPage(page):
    submitList = config.fetch("Work/getWorkSubmitList", params={"p": page + 1, "homework_id": None, "is_answer": None, "uid": None, "cid": None})
    logging.info("submitList: {}".format(submitList))
    try:
      return [[row[k] for k in ["uid", "student_id", "realname"]] for row in submitList["message"]["teacher_not_review"]]
    except KeyError:
      raise JsonError("Failed to get submitList")

  submitStudents = fetchSubmitStudentsPage(0)

  return submitStudents


def fetchStudentAnswer(student):
  studentAnswer = config.fetch("Work/getInfo", params={"homework_id": None, "be_uid": student[0], "uid": None, "cid": None})
  logging.info("studentAnswer: {}".format(studentAnswer))
  try:
    studentAnswer = studentAnswer["message"]["question_list"][0]["answer_record"]
    ret = {"select": studentAnswer["select"], "record": studentAnswer}
    if "attach_info" in studentAnswer:
      ret["attachs"] = [[attach["path"], attach["ext"].lower()] for attach in studentAnswer["attach_info"]]
    return ret
  except KeyError:
    raise JsonError("Failed to get studentAnswer")


def main():
  config.updateAccount()

  homeworks = fetchHomeworks()
  print("homework index: homework title")
  for i in range(len(homeworks)):
    print("{}: {}".format(i, homeworks[i][1]))
  print()

  while True:
    try:
      homeworkIndex = int(input("Input homework index (Press Ctrl+C to cancel): "))
      if 0 <= homeworkIndex < len(homeworks):
        break
      else:
        raise ValueError
    except ValueError:
      print("Please input homework index between 0 and {}".format(len(homeworks)))
  homework = homeworks[homeworkIndex]

  config["params"]["homework_id"] = homework[0]
  homeworkPath = "./{}/".format(homework[1])

  if not os.path.exists(homeworkPath):
    os.makedirs(homeworkPath, mode=0o755)

  cache = Json(homeworkPath + "cache.json")
  if "submitStudents" not in cache:
    cache["submitStudents"] = fetchSubmitStudents()
    cache.flush()

  if "studentAnswers" not in cache:
    cache["studentAnswers"] = {}

  for student in cache["submitStudents"]:
    if student[0] not in cache["studentAnswers"]:
      cache["studentAnswers"][student[0]] = [student, fetchStudentAnswer(student)]
      print("{}/{} {} {}".format(len(cache["studentAnswers"]), len(cache["submitStudents"]), student[1], student[2]))
      cache.flush()

  studentAnswersIndex = 0
  for student, answer in cache["studentAnswers"].values():
    studentAnswersIndex += 1
    print("{}/{} {} {} ".format(studentAnswersIndex, len(cache["studentAnswers"]), student[1], student[2]), end="")
    if answer["select"] != "":
      print("text: '{}' ".format(answer["select"].replace("\n", r"\n")), end="")
    print()

    attachsCount = 0
    if "attachs" in answer:
      for attach in answer["attachs"]:
        downloadFile(attach[0], "{}{}.{}.{}.{}".format(homeworkPath, student[1], student[2], attachsCount, attach[1]))
        attachsCount += 1

    for matchedAttach in re.findall(r"(https?:/(/[\w\-]+(\.[\w\-]+)*)+/?(\?[\w\-\.,@?^=%&:\/~\+#]*)?)", answer["select"]):
      attach = matchedAttach[0], matchedAttach[0].split("?", 1)[0].split(".")[-1].lower()
      downloadFile(attach[0], "{}{}.{}.{}.{}".format(homeworkPath, student[1], student[2], attachsCount, attach[1]))
      attachsCount += 1
      print("download ({})".format(matchedAttach[0]))

    if attachsCount == 0:
      raise ParserError("Nothing download: https://teaching.applysquare.com/T/Course/index/cid/{}#T-Work-treviewinfo-id-{}-be_uid-{}".format(config["params"]["cid"], config["params"]["homework_id"], student[0]))


if __name__ == "__main__":
  logging.basicConfig(level=logging.ERROR, format="%(asctime)s %(levelname)s - %(message)s")

  if len(sys.argv) > 1:
    config = Config(sys.argv[1])
    try:
      main()
    except CrawlerError as e:
      logging.error("{}: {}".format(e.name(), e))
      import traceback
      traceback.print_exc()
      exit(2)
  else:
    print("usage:")
    print("  {} CONFIG")
    print("options:")
    print("  CONFIG    Config json filename")
