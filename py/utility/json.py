
import json as lib_json

from py.utility import *



def dump(obj: Any, filename: str, *args, skipkeys: bool = True, ensure_ascii: bool = False, check_circular: bool = True, allow_nan: bool = True, cls: Optional[Type[lib_json.JSONEncoder]] = None, indent: Optional[int | str] = None, separators: Optional[tuple[str, str]] = (',', ':'), default: Optional[Callable[[Any], Any]] = None, sort_keys: bool = False, encoding: Optional[str] = "utf-8", newline: Optional[str] = "\n", **kwargs):
  s = lib_json.dumps(obj, skipkeys=skipkeys, ensure_ascii=ensure_ascii, check_circular=check_circular, allow_nan=allow_nan, cls=cls, indent=indent, separators=separators, default=default, sort_keys=sort_keys)
  file.write(s, filename, encoding=encoding, newline=newline)

def load(filename: str, *args, cls: Optional[Type[lib_json.JSONDecoder]] = None, object_hook: Optional[Callable[[dict[Any, Any]], Any]] = None, parse_float: Optional[Callable[[str], Any]] = None, parse_int: Optional[Callable[[str], Any]] = None, parse_constant: Optional[Callable[[str], Any]] = None, object_pairs_hook: Optional[Callable[[list[tuple[Any, Any]]], Any]] = None, encoding: Optional[str] = "utf-8", newline: Optional[str] = "\n", default_obj: Optional[Any] = None, **kwargs):
  s = file.read(filename, encoding=encoding, newline=newline)
  return lib_json.loads(s, cls=cls, object_hook=object_hook, parse_float=parse_float, parse_int=parse_int, parse_constant=parse_constant, object_pairs_hook=object_pairs_hook) if s is not None else default_obj



# 1. obj=obj, filename=None
# 2. obj=obj, filename=filename
# 3. filename=filename, obj=load(filename, default_obj=default_obj)

_NOT_SET = object()

class json_handler:

  def __init__(self, obj: Any = _NOT_SET, filename: Optional[str] = None, default_obj: Optional[Any] = None, file_obj: Optional[Any] = None):
    if obj is _NOT_SET:
      obj = load(filename, default_obj=default_obj) if filename is not None else default_obj
    self.__obj = obj
    self.__filename = filename

    if file_obj is None:
      self.__file_obj = obj
      self._save()
    else:
      self.__file_obj = file_obj

  @property
  def _obj(self):
    return self.__obj

  @property
  def _file_obj(self):
    return self.__file_obj

  @property
  def _filename(self):
    return self.__filename

  @_filename.setter
  def _filename(self, value: Optional[str]):
    self.__filename = value
    self._save()

  def __getitem__(self, key: str | int):
    if self._obj is not None:
      try:
        return __class__(self._obj.__getitem__(key), self._filename, file_obj=self._file_obj)
      except (AttributeError, KeyError, IndexError):
        pass

    return __class__(None, filename=self._filename, file_obj=self._file_obj)

  def __setitem__(self, key: str | int, value: Any):
    if self._obj is not None:
      try:
        self._obj.__setitem__(key, value)
        self._save()
      except (AttributeError, IndexError):
        pass

  def __getattr__(self, name: str):
    if name == "keys":
      raise AttributeError()
    obj = self._obj
    obj_dir = dir(obj)
    if name in obj_dir:
      return getattr(obj, name)
    return self[name]

  def __call__(self):
    return self._obj

  def __bool__(self):
    return bool(self._obj)

  def __int__(self):
    return int(self._obj)

  def __float__(self):
    return float(self._obj)

  def __repr__(self):
    fileobj = self._file_obj
    if fileobj is not None:
      fileobj_type = type(fileobj)
      fileobj_id = util.hex(id(fileobj), upper=True, width=16)
      fileobj_repr = f"<{fileobj_type.__module__}.{fileobj_type.__qualname__} id=0x{fileobj_id}>"
    else:
      fileobj_repr = f"{fileobj}"
    return f"<{__class__.__module__}.{__class__.__qualname__} obj={self._obj} fileobj={fileobj_repr} filename={self._filename}>"

  def __iter__(self) -> Iterator[Any]:
    obj = self._obj
    print(f"iter {obj} {type(obj)}")
    if isinstance(obj, list):
      return iter(obj)

    if isinstance(obj, dict):
      return iter(obj.items())

    return iter([])

  def _save(self):
    filename = self._filename
    if filename is None:
      return

    dump(self._file_obj, filename)
