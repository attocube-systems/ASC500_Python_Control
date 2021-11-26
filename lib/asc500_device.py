from lib.asc500_afm import ASC500AFM
from lib.asc500_autoapproach import ASC500AutoApproach
from lib.asc500_base import ASC500Base
from lib.asc500_coarsedevice import ASC500CoarseDevice
from lib.asc500_crosslink import ASC500Crosslink
from lib.asc500_data import ASC500Data
from lib.asc500_limits import ASC500Limits
from lib.asc500_path import ASC500Path
from lib.asc500_scanner import ASC500Scanner
from lib.asc500_spectroscopy import ASC500Spectroscopy
from lib.asc500_zcontrol import ASC500ZControl
from lib.asc500_zfeedback import ASC500ZFeedback


class Device():
    def __init__(self, binPath, dllPath, portNr=-1):
        self.afm = ASC500AFM(binPath, dllPath, portNr)
        self.aap = ASC500AutoApproach(binPath, dllPath, portNr)
        self.base = ASC500Base(binPath, dllPath, portNr)
        self.coarse = ASC500CoarseDevice(binPath, dllPath, portNr)
        self.cross = ASC500Crosslink(binPath, dllPath, portNr)
        self.data = ASC500Data(binPath, dllPath, portNr)
        self.limits = ASC500Limits(binPath, dllPath, portNr)
        self.path = ASC500Path(binPath, dllPath, portNr)
        self.scanner = ASC500Scanner(binPath, dllPath, portNr)
        self.spect = ASC500Spectroscopy(binPath, dllPath, portNr)
        self.zcontrol = ASC500ZControl(binPath, dllPath, portNr)
        self.zfeedback = ASC500ZFeedback(binPath, dllPath, portNr)



