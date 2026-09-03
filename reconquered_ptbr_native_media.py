#!/usr/bin/env python3
"""Install Reconquered PT-BR using Augustus native localized-media overlays.

This experimental installer copies localization-owned files only. It validates
the public Reconquered baseline, but never edits the campaign's canonical XMLs.
"""

from __future__ import annotations

import argparse
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

from reconquered_ptbr_media import (
    MUSIC_PLAN_PATH,
    PAYLOAD_AUDIO,
    PAYLOAD_LOCALIZATION,
    SPEECH_PLAN_PATH,
    load_json,
    sha256,
    validate_campaign_path,
)


INSTALL_MANIFEST = ".reconquered-ptbr-native-media-install.json"
CONFLICTING_MANIFESTS = (
    ".reconquered-ptbr-media-install.json",
    ".reconquered-ptbr-music-install.json",
    ".reconquered-ptbr-install.json",
)


def build_context() -> tuple[dict, dict, dict[str, dict], dict[str, str]]:
    music_plan = load_json(MUSIC_PLAN_PATH)
    speech_plan = load_json(SPEECH_PLAN_PATH)
    speech_by_mission = {item["id"]: item for item in speech_plan["missions"]}
    audio_hashes = {item["file"]: item["sha256"] for item in music_plan["assets"]}
    return music_plan, speech_plan, speech_by_mission, audio_hashes


def expected_localization_paths(music_plan: dict) -> set[str]:
    messages = {
        f"pt-BR/messages/{mission['xml'].removesuffix(' corrected.xml')}.xml"
        for mission in music_plan["missions"]
    }
    media = {
        f"pt-BR/media/{mission['xml'].removesuffix(' corrected.xml')}.xml"
        for mission in music_plan["missions"]
    }
    return {"locales.xml"} | messages | media


def validate_payload(campaign: Path) -> tuple[dict, dict[str, Path], dict[str, str]]:
    music_plan, speech_plan, speech_by_mission, audio_hashes = build_context()
    localization_files = {
        path.relative_to(PAYLOAD_LOCALIZATION).as_posix(): path
        for path in PAYLOAD_LOCALIZATION.rglob("*")
        if path.is_file()
    }
    expected_localization = expected_localization_paths(music_plan)
    if set(localization_files) != expected_localization:
        missing = sorted(expected_localization - set(localization_files))
        unexpected = sorted(set(localization_files) - expected_localization)
        raise ValueError(
            f"Invalid native localization payload; missing={missing}, unexpected={unexpected}"
        )

    for mission in music_plan["missions"]:
        speech_mission = speech_by_mission.get(mission["id"])
        if not speech_mission:
            raise ValueError(f"Missing speech plan for {mission['id']}")
        if (
            speech_mission["xml"] != mission["xml"]
            or speech_mission["baseline_sha256"] != mission["sha256"]
        ):
            raise ValueError(f"Media plans disagree for {mission['id']}")
        xml_path = campaign / "xmls" / mission["xml"]
        if not xml_path.is_file():
            raise FileNotFoundError(f"Missing XML: {mission['xml']}")
        actual = sha256(xml_path)
        if actual != mission["sha256"]:
            raise ValueError(
                f"Incompatible baseline for {mission['xml']}: "
                f"expected {mission['sha256']}, found {actual}"
            )
        for speech in speech_mission["speech"]:
            previous = audio_hashes.get(speech["file"])
            if previous and previous != speech["sha256"]:
                raise ValueError(f"Conflicting audio hash for {speech['file']}")
            audio_hashes[speech["file"]] = speech["sha256"]

    for name, expected_hash in audio_hashes.items():
        source = PAYLOAD_AUDIO / name
        if not source.is_file():
            raise FileNotFoundError(f"Missing payload audio: {name}")
        actual = sha256(source)
        if actual != expected_hash:
            raise ValueError(
                f"Payload hash mismatch for {name}: expected {expected_hash}, found {actual}"
            )
    return speech_plan, localization_files, audio_hashes


def install_file(source: Path, destination: Path, campaign: Path, backup_root: Path, kind: str) -> dict:
    relative = destination.relative_to(campaign)
    had_original = destination.exists()
    if had_original:
        backup = backup_root / relative
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(destination, backup)
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)
    return {
        "kind": kind,
        "relative_path": relative.as_posix(),
        "had_original": had_original,
        "installed_sha256": sha256(destination),
    }


def install(campaign: Path) -> None:
    manifest_path = campaign / INSTALL_MANIFEST
    if manifest_path.exists():
        raise FileExistsError("The native PT-BR media integration is already registered.")
    for conflicting in CONFLICTING_MANIFESTS:
        if (campaign / conflicting).exists():
            raise FileExistsError(
                f"Remove the previous integration ({conflicting}) before native installation."
            )

    speech_plan, localization_files, audio_hashes = validate_payload(campaign)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_root = campaign / ".reconquered-ptbr-native-media-backup" / stamp
    records: list[dict] = []

    for relative_name, source in sorted(localization_files.items()):
        destination = campaign / "localization" / Path(relative_name)
        records.append(install_file(source, destination, campaign, backup_root, "localization"))
    for name in sorted(audio_hashes):
        destination = campaign / "localization" / "pt-BR" / "audio" / name
        records.append(install_file(PAYLOAD_AUDIO / name, destination, campaign, backup_root, "audio"))

    manifest = {
        "component": "Reconquered PT-BR native localized-media integration",
        "installer": "portable-python-native-media",
        "installed_utc": datetime.now(timezone.utc).isoformat(),
        "campaign_directory": str(campaign),
        "backup_directory": str(backup_root),
        "missions": len(speech_plan["missions"]),
        "localization_files": len(localization_files),
        "speech_files": sum(len(item["speech"]) for item in speech_plan["missions"]),
        "music_files": len(load_json(MUSIC_PLAN_PATH)["assets"]),
        "files": records,
    }
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Installed native PT-BR localization in: {campaign}")
    print(
        f"Installed {len(localization_files)} localization files and "
        f"{len(audio_hashes)} localized audio files; canonical XMLs were not modified."
    )
    print(f"Backup: {backup_root}")


def uninstall(campaign: Path) -> None:
    manifest_path = campaign / INSTALL_MANIFEST
    if not manifest_path.is_file():
        raise FileNotFoundError("Native PT-BR media installation manifest not found.")
    manifest = load_json(manifest_path)
    backup_root = Path(manifest["backup_directory"])

    for record in manifest["files"]:
        destination = campaign / Path(record["relative_path"])
        if not destination.is_file():
            raise FileNotFoundError(f"Installed file is missing: {record['relative_path']}")
        actual = sha256(destination)
        if actual != record["installed_sha256"]:
            raise ValueError(
                f"File changed after installation; refusing to overwrite it: "
                f"{record['relative_path']}"
            )

    for record in manifest["files"]:
        destination = campaign / Path(record["relative_path"])
        if record["had_original"]:
            backup = backup_root / Path(record["relative_path"])
            if not backup.is_file():
                raise FileNotFoundError(f"Missing backup: {backup}")
            shutil.copy2(backup, destination)
        else:
            destination.unlink()

    installed_parents = {
        (campaign / Path(record["relative_path"])).parent for record in manifest["files"]
    }
    for directory in sorted(installed_parents, key=lambda path: len(path.parts), reverse=True):
        current = directory
        while current != campaign:
            try:
                current.rmdir()
            except OSError:
                break
            current = current.parent

    archived = backup_root / "uninstalled-native-media-install-manifest.json"
    shutil.copy2(manifest_path, archived)
    manifest_path.unlink()
    print("Removed native PT-BR localization and restored previous files.")
    print(f"Backup retained at: {backup_root}")


def verify(campaign: Path) -> None:
    manifest_path = campaign / INSTALL_MANIFEST
    if not manifest_path.is_file():
        raise FileNotFoundError("Native PT-BR media installation manifest not found.")
    manifest = load_json(manifest_path)
    validate_payload(campaign)
    for record in manifest["files"]:
        destination = campaign / Path(record["relative_path"])
        if not destination.is_file():
            raise FileNotFoundError(f"Installed file is missing: {record['relative_path']}")
        actual = sha256(destination)
        if actual != record["installed_sha256"]:
            raise ValueError(
                f"Installed file hash mismatch for {record['relative_path']}: "
                f"expected {record['installed_sha256']}, found {actual}"
            )
    print(
        f"Verified native PT-BR installation: {manifest['missions']} missions, "
        f"{manifest['localization_files']} localization files, "
        f"{manifest['speech_files']} speech files and {manifest['music_files']} music files."
    )
    print("All canonical XML hashes remain on the approved public baseline.")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    for command in ("install", "verify", "uninstall"):
        subparser = subparsers.add_parser(command)
        subparser.add_argument("campaign_directory")
    args = parser.parse_args()
    campaign = validate_campaign_path(args.campaign_directory)
    if args.command == "install":
        install(campaign)
    elif args.command == "verify":
        verify(campaign)
    else:
        uninstall(campaign)


if __name__ == "__main__":
    main()
