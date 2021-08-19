# -*- coding: utf-8 -*-

from .CIHS import CIHS
from .CIMS import CIMS
from .CILS import CILS
from .PIHS import PIHS
from .PIMS import PIMS
from .PILS import PILS
from .NIHS import NIHS
from .NIMS import NIMS
from .NILS import NILS

task_list = [CIHS(), CIMS(), CILS(), PIHS(), PIMS(), PILS(), NIHS(), NIMS(), NILS()]
name_list = ["CIHS", "CIMS", "CILS", "PIHS", "PIMS", "PILS", "NIHS", "NIMS", "NILS"]