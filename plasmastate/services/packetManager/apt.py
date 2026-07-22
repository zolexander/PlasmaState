from .packetmanager import PackageManager
from ..process import ProcessService
class AptManager(PackageManager):

    def install(self,packages:list(str)):
        ProcessService.run(["apt","install",packages])

    def showmanual(self):
        res =ProcessService.run(["apt-mark","showmanual"])
        return res