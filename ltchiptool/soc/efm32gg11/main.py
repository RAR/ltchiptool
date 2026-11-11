# Copyright (c) Andrew Rankin 2026-06-16.

from abc import ABC
from logging import info
from typing import List, Optional, Union

from ltchiptool import Family
from ltchiptool.models import OTAType
from ltchiptool.soc import SocInterfaceCommon
from ltchiptool.util.flash import FlashConnection, FlashFeatures

EFM32GG11_GUIDE = [
    "EFM32GG11 has no serial download mode, so ltchiptool cannot flash it.",
    "Flash the first image over SWD (in PlatformIO: `pio run -t upload`, "
    "which uses OpenOCD), then update over-the-air with the UF2 package.",
]


class EFM32GG11Main(
    SocInterfaceCommon,
    ABC,
):
    def __init__(self, family: Family) -> None:
        super().__init__()
        self.family = family

    def hello(self):
        info("Hello from EFM32GG11")

    @property
    def ota_type(self) -> Optional[OTAType]:
        # Two application banks (ota1, ota2), each linked for its own address.
        # The UF2 carries the ota1 image, plus binary patches that turn it
        # into the ota2 image on devices that are running from ota1.
        return OTAType.DUAL

    # LibreTiny's builder links and converts the images itself, so link2elf()
    # and elf2bin() are not implemented. The only use of this class is packing
    # the UF2, which needs nothing but ota_type.

    def flash_get_features(self) -> FlashFeatures:
        return FlashFeatures(
            can_write=False,
            can_read=False,
            can_read_rom=False,
            can_read_efuse=False,
            can_read_info=False,
        )

    def flash_get_guide(self) -> List[Union[str, list]]:
        return EFM32GG11_GUIDE

    def flash_set_connection(self, connection: FlashConnection) -> None:
        # first call of every `ltchiptool flash` command
        raise NotImplementedError(" ".join(EFM32GG11_GUIDE))
