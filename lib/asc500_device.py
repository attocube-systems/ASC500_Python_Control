from lib.asc500_afm import ASC500AFM
from lib.asc500_autoapproach import ASC500AutoApproach
from lib.asc500_base import ASC500Base
from lib.asc500_coarsedevice import ASC500CoarseDevice
from lib.asc500_limits import ASC500Limits
from lib.asc500_scanner import ASC500Scanner
from lib.asc500_zcontrol import ASC500ZControl
from lib.asc500_zfeedback import ASC500ZFeedback


class Device():
    def __init__(self, binPath, dllPath, portNr=-1):
        self.afm = ASC500AFM()
        self.aap = ASC500AutoApproach()
        self.base = ASC500Base(binPath, dllPath, portNr)
        self.coarse = ASC500CoarseDevice()
        self.limits = ASC500Limits()
        self.scanner = ASC500Scanner()
        self.zcontrol = ASC500ZControl()
        self.zfeedback = ASC500ZFeedback()



