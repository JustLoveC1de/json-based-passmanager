import os
import json
class Config:
    def check(self) -> bool:
        return os.path.exists(self.path)
    
    def create(self) -> None:
        with open(self.path, 'wt+') as conf:
            conf.write(json.dumps(self.contents, ensure_ascii=False, indent=4))
            print("> Создан файл!")

    def write(self, pair: tuple, exclusivelyAdd: bool = True) -> None:
        keys: set = set(self.contents.keys()) 
        keyUsed: bool = pair[0] in keys
        if (keyUsed and exclusivelyAdd) or not (keyUsed or exclusivelyAdd):
            raise KeyError
        self.contents[pair[0]] = pair[1]
        self.update()

    def update(self):
        with open(self.path, 'wt+') as conf:
            conf.write(json.dumps(self.contents,ensure_ascii=False,indent=4))

    def delete(self, key: str):
        del self.contents[key]
        self.update()

    def read(self) -> None:
        with open(self.path, 'rt') as conf:
            self.contents = json.loads(conf.read())
        
    def __init__(self, path: str, standart_values: dict) -> None:
        self.path: str = path
        self.contents: dict = {}
        if not self.check():
            self.contents = standart_values
            self.create()
        else:
            self.read()
        
