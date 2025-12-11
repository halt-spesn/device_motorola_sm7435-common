#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
#
# SPDX-FileCopyrightText: 2025-2026 The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

from extract_utils.fixups_blob import (
    blob_fixup,
    blob_fixups_user_type,
)
from extract_utils.fixups_lib import (
    lib_fixup_remove,
    lib_fixups,
    lib_fixups_user_type,
)

from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)

namespace_imports = [
    'device/motorola/sm7435-common',
    'hardware/motorola',
    'hardware/qcom-caf/sm8450-6.6',
    'hardware/qcom-caf/wlan',
    'vendor/qcom/opensource/commonsys/display',
    'vendor/qcom/opensource/commonsys-intf/display',
    'vendor/qcom/opensource/dataservices',
]

libs_add_vendor_suffix = (
    'com.qualcomm.qti.dpm.api@1.0',
    'vendor.qti.ImsRtpService-V1-ndk',
    'vendor.qti.diaghal-V1-ndk',
    'vendor.qti.hardware.dpmaidlservice-V1-ndk',
    'vendor.qti.qccsyshal_aidl-V1-ndk',
    'vendor.qti.qccvndhal_aidl-V1-ndk',
)

def lib_fixup_vendor_suffix(lib: str, partition: str, *args, **kwargs):
    if partition != 'vendor':
        return None

    return f'{lib}_{partition}'


lib_fixups: lib_fixups_user_type = {
    **lib_fixups,
    libs_add_vendor_suffix: lib_fixup_vendor_suffix,
}


blob_fixups: blob_fixups_user_type = {
    'vendor/lib64/libqcodec2_core.so': blob_fixup()
        .add_needed('libcodec2_shim.so'),
    'system_ext/etc/permissions/moto-telephony.xml': blob_fixup()
        .regex_replace('/system/', '/system_ext/'),
    (
       'vendor/etc/media_codecs_parrot_v0.xml',
       'vendor/etc/media_codecs_ravelin.xml',
    ): blob_fixup()
        .regex_replace('.+media_codecs_(google_audio|google_c2|google_telephony|vendor_audio|dolby_audio).+\n', ''),
    'vendor/etc/sensors/hals.conf': blob_fixup()
        .add_line_if_missing('sensors.moto_ext.so'),
    'system_ext/priv-app/ims/ims.apk': blob_fixup()
        .apktool_patch('ims-patches'),
    (
        'vendor/bin/poweropt-service',
        'vendor/lib64/libaodoptfeature.so',
        'vendor/lib64/hw/libaudioeffecthal.qti.so',
        'vendor/lib64/libapengine.so',
        'vendor/lib64/libdpps.so',
        'vendor/lib64/libcamerapoweroptfeature.so',
        'vendor/lib64/libgamepoweroptfeature.so',
        'vendor/lib64/liblearningmodule.so',
        'vendor/lib64/liboffscreenpoweroptfeature.so',
        'vendor/lib64/libpowercallback.so',
        'vendor/lib64/libpowercore.so',
        'vendor/lib64/libpsmoptfeature.so',
        'vendor/lib64/libsnapdragoncolor-manager.so',
        'vendor/lib64/libstandbyfeature.so',
        'vendor/lib64/libvideooptfeature.so',
    ): blob_fixup()
        .replace_needed('libtinyxml2.so', 'libtinyxml2-v34.so'),
    (
        'vendor/lib64/hw/libaudiocorehal.default.so',
        'vendor/lib64/libaudioplatformconverter.qti.so',
        'vendor/lib64/libqtigefar.so',
    ): blob_fixup()
        .replace_needed('android.hardware.audio.core-V2-ndk.so', 'android.hardware.audio.core-V3-ndk.so')
        .replace_needed('android.media.audio.common.types-V3-ndk.so', 'android.media.audio.common.types-V4-ndk.so'),
    'vendor/lib64/hw/libaudiocorehal.qti.so': blob_fixup()
        .replace_needed('android.media.audio.common.types-V3-ndk.so', 'android.media.audio.common.types-V4-ndk.so')
        .replace_needed('android.hardware.audio.core-V2-ndk.so', 'android.hardware.audio.core-V3-ndk.so')
        .replace_needed('android.hardware.audio.effect-V2-ndk.so', 'android.hardware.audio.effect-V3-ndk.so')
        .replace_needed('android.hardware.audio.core.sounddose-V1-ndk.so', 'android.hardware.audio.core.sounddose-V3-ndk.so')
        .replace_needed('android.hardware.audio.common-V1-ndk.so', 'android.hardware.audio.common-V4-ndk.so'),
    'vendor/lib64/hw/android.hardware.bluetooth.audio_sw.so': blob_fixup()
        .replace_needed('android.hardware.audio.core-V2-ndk.so', 'android.hardware.audio.core-V3-ndk.so')
        .replace_needed('android.media.audio.common.types-V3-ndk.so', 'android.media.audio.common.types-V4-ndk.so')
        .replace_needed('android.hardware.bluetooth.audio-V4-ndk.so', 'android.hardware.bluetooth.audio-V5-ndk.so'),
    (
        'vendor/lib64/btaudio_offload_if.so',
        'vendor/lib64/hw/android.hardware.bluetooth.audio-impl-qti.so',
        'vendor/lib64/hw/audio.bluetooth_qti.default.so',
        'vendor/lib64/libbluetooth_audio_session_aidl_qti.so',
    ): blob_fixup()
        .replace_needed('android.hardware.bluetooth.audio-V4-ndk.so', 'android.hardware.bluetooth.audio-V5-ndk.so'),
    (
        'vendor/bin/qguard',
        'vendor/lib64/libqcodec2_utils.so',
        'vendor/lib64/libqtiperfd.so',
    ): blob_fixup()
        .replace_needed('vendor.qti.hardware.display.config-V5-ndk.so', 'vendor.qti.hardware.display.config-V12-ndk.so'),
    (
        'vendor/lib64/liboemcrypto.so',
        'vendor/lib64/libops.so',
    ): blob_fixup()
        .replace_needed('vendor.qti.hardware.display.config-V7-ndk.so', 'vendor.qti.hardware.display.config-V12-ndk.so'),
    'vendor/lib64/libsensorndkbridge.so': blob_fixup()
        .replace_needed('android.hardware.sensors-V2-ndk.so', 'android.hardware.sensors-V3-ndk.so'),
} # fmt: skip

module = ExtractUtilsModule(
    'sm7435-common',
    'motorola',
    blob_fixups=blob_fixups,
    lib_fixups=lib_fixups,
    namespace_imports=namespace_imports,
)

if __name__ == '__main__':
    utils = ExtractUtils.device(module)
    utils.run()
