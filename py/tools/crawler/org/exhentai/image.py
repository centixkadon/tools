
import asyncio

import os
import time

import argparse
import bs4
import re

import httpx

from py.utility import color
from py.utility import loggers
from py.utility import jsonio



class DownloadWarning(Warning):
  """"""


class HelpConfigAction(argparse.Action):
  def __init__(self, option_strings, dest=argparse.SUPPRESS, default=argparse.SUPPRESS, help=None):
    super().__init__(option_strings=option_strings, dest=dest, default=default, nargs=0, help=help)

  def __call__(self, parser, namespace, values, option_string=None):
    parser.print_help()
    print("""
config json file example:
{
  "origin": "https://exhentai.org",
  "headers": {
    "Every-Key": "you can find in your browser"
  },
  "cookies": {
    "igneous": "xxx",
    "ipb_member_id": "xxx",
    "ipb_pass_hash": "xxx"
  }
}""")
    parser.exit()



class Image:
  def __init__(self, *, cache, logfile, **_):
    self.__storage_handler = jsonio.JsonHandler(filename=f"{cache}/storage.json", default={})
    self.__files = {}
    if logfile:
      with open(logfile, "wb") as f:
        f.write(b'')

  def save_file(self, *, filename, buffer, **_):
    self.__files[filename] = buffer
    with open(filename, "wb") as f:
      f.write(buffer)
      logger.debug(f"save_file '{filename}'")
      self.__files.pop(filename)

  def close(self, **_):
    self.__storage_handler.save()
    for filename, buffer in self.__files:
      with open(filename, "wb") as f:
        f.write(buffer)

  async def run(self, *, parser, client, command, **_):
    storage_handler = self.__storage_handler
    async with httpx.AsyncClient(**client) as aclient:
      self.__client = aclient
      self.__client_count = 0

      logger.info(f"command {command}")
      storage_handler[command] = storage_handler[command]() or {}
      try:
        kwargs.update({
          "storage": storage_handler[command],
          "timeout": client.get("timeout")
        })
        await self.__getattribute__(command)(**kwargs)
      except httpx.TransportError as e:
        logger.critical(f"run", exc_info=e)
        parser.exit(1)

  async def search(self, *, storage: jsonio.JsonHandler, keyword, begin, end, **_):
    logger.debug(f"kwargs {kwargs}")
    logger.info(f"search '{keyword}' from page {begin} to page {end}")

    storage[keyword] = storage[keyword]() or {}
    search_results = storage[keyword]

    for page in range(begin, end):
      search_results[page] = search_results[page]() or {}
      params = {"f_search": keyword} if keyword else {}
      if page != 0:
        params["page"] = page
      await self._search_page(search_result=search_results[page], search_params=params, **kwargs)

  async def _search_page(self, *, cache, search_result: jsonio.JsonHandler, search_params, search_expired, origin, search_format, logfile, **_):
    if search_result.time(0) + search_expired < time.time():
      r = await self.get(origin, params=search_params, **kwargs)
      with open(f"{cache}/index.html", "wb") as f:
        f.write(r)

      soup = bs4.BeautifulSoup(r, features="xml")
      search_result["value"] = [{
        "url": gallery.select_one('a')["href"],
        "title": gallery.select_one('.glink').text,
      } for gallery in soup.select('.glname')]

      search_result["time"] = time.time()

    for gallery in search_result.value:
      if search_format:
        url = gallery.url()
        title = re.compile('[\\/:*?"<>|]').sub("", gallery.title(""))
        title = re.compile('\\s+').sub(" ", title)
        line = search_format.format(url=url, title=title, url_split=url.split("/"))
        print(line)
        if logfile:
          with open(logfile, "a", encoding="utf-8") as f:
            f.write(f"{line}\n")



  async def download(self, *, cache, storage: jsonio.JsonHandler, gallery_expired, gallery, path, download_format, sheet_delay, **_):
    logger.debug(f"kwargs {kwargs}")
    logger.info(f"download {gallery}")

    os.makedirs(path, exist_ok=True)

    storage[gallery] = storage[gallery]({})
    gallery_info = storage[gallery]
    if gallery_info.time(0) + gallery_expired < time.time():
      r = await self.get(gallery, **kwargs)
      with open(f"{cache}/gallery.html", "wb") as f:
        f.write(r)

      soup = bs4.BeautifulSoup(r, features="xml")
      gallery_info["pages"] = [gallery_page["href"] for gallery_page in soup.select('.ptt a') if gallery_page.text not in "<>"]
      gallery_info["sheets"] = [{
        "url": sheet.select_one('a')["href"],
        "title": sheet.select_one('img')["title"].split(": ", 1)[1],
      } for sheet in soup.select('.gdtm')]

      gallery_info["time"] = time.time()

    waitings = set()
    for gallery_page in gallery_info["pages"]():
      storage[gallery_page] = storage[gallery_page]({})
      gallery_page_info = storage[gallery_page]
      if gallery_page_info.time(0) + gallery_expired < time.time():
        r = await self.get(gallery_page, **kwargs)
        with open(f"{cache}/gallery.html", "wb") as f:
          f.write(r)

        soup = bs4.BeautifulSoup(r, features="xml")
        gallery_page_info["sheets"] = [{
          "url": sheet.select_one('a')["href"],
          "title": sheet.select_one('img')["title"].split(": ", 1)[1],
        } for sheet in soup.select('.gdtm')]

        gallery_page_info["time"] = time.time()

      for gallery_sheet in gallery_page_info["sheets"]:
        url = gallery_sheet.url()
        filename = download_format.format(path=path, url_split=url.split("/"), title=gallery_sheet.title())
        if not os.path.exists(filename):
          def waiting(url=url, filename=filename, delay=sheet_delay):
            return self._download_image(url=url, filename=filename, delay=delay, **kwargs)
          waitings.add(waiting)

    await self._download_futures(waitings, **kwargs)


  async def _download_futures(self, waitings, *, sheet_delay, image_parallel, image_retries, **_):
    tasks = {}
    while len(tasks) < image_parallel and waitings:
      func = waitings.pop()
      tasks.setdefault(asyncio.ensure_future(func(delay=sheet_delay * len(tasks))), jsonio.JsonParser({
        "func": func,
        "retries": 0,
      }))

    while tasks:
      logger.info(f"download task {len(tasks)} waiting {len(waitings)}")
      dones, pendings = await asyncio.wait(tasks.keys(), return_when=asyncio.FIRST_COMPLETED)
      logger.debug(f"download done {len(dones)} pending {len(pendings)}")

      dones, exceptions = self._raise_for_dones(dones, except_ignores=(httpx.RequestError, asyncio.TimeoutError, Warning))
      for done in dones:
        tasks.pop(done)
        logger.debug(f"download_image success left {len(tasks)} + {len(waitings)}")
      for exception in exceptions:
        task = tasks.pop(exception)
        retries = task.retries()
        # logger.warning(f"download_image failed retries {retries}", exc_info=exception.exception())
        logger.warning(f"download_image failed retries {retries}")

        if retries < image_retries:
          tasks.setdefault(asyncio.ensure_future(task.func()()), jsonio.JsonParser({
            "func": task.func(),
            "retries": retries + 1,
          }))

      while len(tasks) < image_parallel and waitings:
        func = waitings.pop()
        tasks.setdefault(asyncio.ensure_future(func()), jsonio.JsonParser({
          "func": func,
          "retries": 0,
        }))



  async def get(self, url, *, params=None, timeout, **_):
    logger.debug(f"GET kwargs {kwargs}")
    logger.debug(f"GET {url} params={params}")

    self.__client_count += 1
    if self.__client_count % 10 == 0:
      logger.info(f"GET count {self.__client_count}")
    response = await asyncio.wait_for(self.__client.get(url, params=params), timeout)
    response.raise_for_status()
    logger.debug(f"GET {url} params={params} done")
    return response.content

  async def _download_image(self, *, delay, url, filename, **_):
    logger.info(f"_download_image {url}")
    r = await self._get_image(delay=delay, url=url, **kwargs)
    if r:
      self.save_file(filename=filename, buffer=r, **kwargs)
    else:
      raise DownloadWarning("image content is empty")

  async def _get_image(self, *, delay, url, image_urls = [], next_loads = [], cache, sheet_delay, client, **_):
    logger.debug(f"kwargs {kwargs}")
    logger.debug(f"_get_image {url} next_load {len(next_loads)} delay {delay}")

    await asyncio.sleep(delay)

    r = await self.get(url, params={"nl": next_loads}, **kwargs)
    with open(f"{cache}/sheet{len(next_loads)}.html", "wb") as f:
      f.write(r)

    soup = bs4.BeautifulSoup(r, features="xml")

    image_url = soup.select_one('#i3 img')["src"]
    if image_url not in image_urls:
      r = await self._get_image_one(image_url, **kwargs)
      if r:
        return r
      image_urls = image_urls + [image_url]

    next_load = soup.select_one('#loadfail')["onclick"].split("'")[1]
    if next_load not in next_loads:
      r = await self._get_image(delay=sheet_delay, url=url, image_urls=image_urls, next_loads=next_loads + [next_load], **kwargs)
      if r:
        return r
    else:
      for image_url in image_urls:
        r = await self._get_image_one(image_url, proxies=client["proxies"], **kwargs)
        if r:
          return r

    return b''

  async def _get_image_one(self, url, *, proxies=None, image_timeout, image_timeout_step, image_timeout_retries, **_):
    logger.debug(f"_get_image_one {url}")
    if url.startswith("https://exhentai.org"):
      if url.endswith("509.gif"):
        logger.error(f"_get_image_one reached the image limit {url}")
      else:
        logger.error(f"_get_image_one unexcepted url {url}")
      raise RuntimeError(f"unexcepted url {url}")

    async with httpx.AsyncClient() if proxies is None else httpx.AsyncClient(proxies=proxies) as client:
      for image_timeout_retry in range(image_timeout_retries):
        try:
          timeout = image_timeout + image_timeout_step * image_timeout_retry
          response = await asyncio.wait_for(client.get(url, timeout=timeout), timeout)
          response.raise_for_status()
          logger.debug(f"_get_image_one {url} done")
          return response.content
        except (httpx.RequestError, asyncio.TimeoutError) as e:
          logger.warning(f"_get_image_one {url}")
          return b''
        except httpx.HTTPStatusError as e:
          logger.error(f"_get_image_one {url}", exc_info=e)
          raise e

  def _raise_for_dones(self, futures, except_ignores=[]):
    try:
      iter(except_ignores)
    except TypeError:
      except_ignores = [except_ignores]

    self._cancel(futures)

    dones = set()
    exceptions = set()
    for future in futures:
      exception = future.exception()
      if exception is None:
        dones.add(future)
      else:
        exceptions.add(future)
        for except_ignore in except_ignores:
          if isinstance(exception, except_ignore):
            exception = None
            break
      if exception is not None:
        raise exception

    return dones, exceptions

  def _cancel(self, futures):
    for future in futures:
      future.cancel()



def main():
  if False:
    async def func2():
      raise RuntimeError("help")
    async def func1():
      await func2()
    async def test():
      dones, pendings = await asyncio.wait({func1()}, return_when=asyncio.FIRST_COMPLETED)
      for done in dones:
        e = done.exception()
        if e is not None:
          try:
            raise e
          except RuntimeError as ee:
            # raise TimeoutError("timeout").with_traceback(ee.__traceback__)
            # raise TimeoutError("timeout")
            # raise ee.with_traceback(ee.__traceback__.tb_next)
            ee = ee.with_traceback(ee.__traceback__.tb_next)
            raise ee
          finally:
            print("finally")
    asyncio.run(test())
    return

  parser = argparse.ArgumentParser(description=color.red("Download images from exhentai."), epilog=color.green("Python module argparse epilog."), add_help=False)
  parser.add_argument("-h", "--help", help="show help message and exit", action="help")
  parser.add_argument("-h2", "--help2", help="show help message with config json file example and exit", action=HelpConfigAction)
  parser.add_argument("-V", "--version", action="version", version="%(prog)s 0.1")
  parser.add_argument("-v", "--verbose", help=f"set log level to {loggers.INFO_NAME} or {loggers.DEBUG_NAME} (default {loggers.WARNING_NAME})", action="count", default=0)
  parser.add_argument("-q", "--quiet", help=f"set log level to {loggers.ERROR_NAME} or {loggers.CRITICAL_NAME} (default {loggers.WARNING_NAME})", action="count", default=0)

  parser.add_argument("--config", help="config json file", required=True)
  parser.add_argument("--cache", help="cache path")
  parser.add_argument("--logfile", help="log file")

  subparsers = parser.add_subparsers(title="commands", description="Search gallerys or download images.", dest="command", metavar="COMMAND")
  subparser = subparsers.add_parser("search", help="search gallerys")
  subparser.add_argument("-k", "--keyword", help="keyword", default="")
  # subparser.add_argument("-a", "--all", help="print all result info", action="store_true")
  subparser.add_argument("-b", "--begin", help="begin page", type=int, default=0)
  subparser.add_argument("-e", "--end", help="end page", type=int, default=1)
  subparser.add_argument("--search-format", help="format result info")
  subparser.add_argument("--search-expired", help="search cache expired time")

  subparser = subparsers.add_parser("download", help="download images")
  subparser.add_argument("gallery", help="gallery url")
  subparser.add_argument("path", help="download path")
  subparser.add_argument("--gallery-expired", help="gallery cache expired time")
  subparser.add_argument("--download-format", help="format download filename")
  subparser.add_argument("--image-retries", help="download image retries")
  subparser.add_argument("--image-timeout", help="download image timeout")

  args = parser.parse_args()
  level = max(0, loggers.WARNING - (args.verbose - args.quiet) * 10)
  logger.setLevel(level)

  logger.info(f"set log level to {loggers.levelname(level)}")
  logger.info(f"parse_args {args}")

  config = jsonio.JsonParser(jsonio.loadf(args.config))({})
  logger.info(f"load_config {config}")

  args.parser = parser
  args.level = level

  kwargs.update(vars(args))
  kwargs.update(config)
  kwargs.update({key: value for key, value in vars(args).items() if value is not None})
  runner = Image(**kwargs)
  try:
    asyncio.run(runner.run(**kwargs))
  except KeyboardInterrupt as e:
    logger.error(f"manual interrupt", exc_info=e)
    jsonio.retry(KeyboardInterrupt, func=runner.close, message="closing, please wait", print=logger.warning)
    parser.exit(2)

  # parser.exit(2)



if __name__ == "__main__":
  loggers.config([__name__])
  logger = loggers.get(__name__)

  kwargs = {}

  main()
