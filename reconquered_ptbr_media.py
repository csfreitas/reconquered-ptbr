#!/usr/bin/env python3
"""Portable Reconquered PT-BR media installer for Windows, Linux and macOS.

Uses only the Python standard library. It patches media references in the
user-owned public campaign after exact baseline validation; full source XMLs
are never distributed by this project.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path


SCRIPT_ROOT = Path(__file__).resolve().parent
MUSIC_PLAN_PATH = SCRIPT_ROOT / "MEDIA_INTEGRATION_PLAN.json"
SPEECH_PLAN_PATH = SCRIPT_ROOT / "SPEECH_INTEGRATION_PLAN.json"
PAYLOAD_AUDIO = SCRIPT_ROOT / "Reconquered Campaign" / "audio"
PAYLOAD_LOCALIZATION = SCRIPT_ROOT / "Reconquered Campaign" / "localization"
INSTALL_MANIFEST = ".reconquered-ptbr-media-install.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def patch_xml_text(
    content: str,
    briefing_original: str,
    briefing_new: str,
    victory_original: str,
    victory_new: str,
    speech_entries: list[dict],
) -> str:
    def replace_music(text: str, original: str, replacement: str) -> str:
        pattern = re.compile(
            rf'<background_music\s+filename=["\']{re.escape(original)}["\']\s*/>',
            re.IGNORECASE,
        )
        if len(pattern.findall(text)) != 1:
            raise ValueError(f"Expected exactly one background_music reference to {original}")
        return pattern.sub(f'<background_music filename="{replacement}"/>', text)

    content = replace_music(content, briefing_original, briefing_new)
    content = replace_music(content, victory_original, victory_new)
    newline = "\r\n" if "\r\n" in content else "\n"
    speech_pattern = re.compile(
        r'<media\b(?=[^>]*\btype\s*=\s*["\']speech["\'])[^>]*/>',
        re.IGNORECASE,
    )

    for speech in speech_entries:
        uid = speech["uid"]
        message_pattern = re.compile(
            rf'<message\s+uid=["\']{re.escape(uid)}["\'][^>]*>.*?</message>',
            re.DOTALL,
        )
        matches = list(message_pattern.finditer(content))
        if len(matches) != 1:
            raise ValueError(f"Expected exactly one message UID {uid!r}")
        block = matches[0].group(0)
        existing = speech_pattern.findall(block)
        new_tag = f'<media type="speech" filename="{speech["file"]}"/>'
        if len(existing) > 1:
            raise ValueError(f"More than one speech node for UID {uid!r}")
        if existing:
            patched_block = speech_pattern.sub(new_tag, block, count=1)
        else:
            closing = block.rfind("</message>")
            patched_block = block[:closing] + f"        {new_tag}{newline}" + block[closing:]
        content = content[: matches[0].start()] + patched_block + content[matches[0].end() :]

    return content


def validate_campaign_path(value: str) -> Path:
    campaign = Path(value).expanduser().resolve(strict=True)
    if campaign.name != "Reconquered Campaign":
        raise ValueError("The final directory must be named exactly 'Reconquered Campaign'.")
    return campaign


def build_context(campaign: Path) -> tuple[dict, dict, dict[str, dict], dict[str, str]]:
    music_plan = load_json(MUSIC_PLAN_PATH)
    speech_plan = load_json(SPEECH_PLAN_PATH)
    speech_by_mission = {item["id"]: item for item in speech_plan["missions"]}
    music_hashes = {item["file"]: item["sha256"] for item in music_plan["assets"]}
    return music_plan, speech_plan, speech_by_mission, music_hashes


def install(campaign: Path) -> None:
    manifest_path = campaign / INSTALL_MANIFEST
    if manifest_path.exists():
        raise FileExistsError("The PT-BR media integration is already registered; uninstall it first.")
    if (campaign / ".reconquered-ptbr-music-install.json").exists():
        raise FileExistsError("Remove the music-only integration before installing the complete media package.")
    if (campaign / ".reconquered-ptbr-install.json").exists():
        raise FileExistsError("Remove the legacy PT-BR beta before installing the complete package.")

    music_plan, speech_plan, speech_by_mission, music_hashes = build_context(campaign)
    planned_audio: dict[str, str] = dict(music_hashes)
    patched_xml: dict[Path, str] = {}

    expected_localization = {"locales.xml"} | {
        f"pt-BR/messages/{mission['xml'].removesuffix(' corrected.xml')}.xml"
        for mission in music_plan["missions"]
    }
    localization_files = {
        path.relative_to(PAYLOAD_LOCALIZATION).as_posix(): path
        for path in PAYLOAD_LOCALIZATION.rglob("*")
        if path.is_file()
    }
    if set(localization_files) != expected_localization:
        missing = sorted(expected_localization - set(localization_files))
        unexpected = sorted(set(localization_files) - expected_localization)
        raise ValueError(f"Invalid localization payload; missing={missing}, unexpected={unexpected}")

    # Complete validation before the first write.
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
                f"Incompatible baseline for {mission['xml']}: expected {mission['sha256']}, found {actual}"
            )
        for speech in speech_mission["speech"]:
            previous = planned_audio.get(speech["file"])
            if previous and previous != speech["sha256"]:
                raise ValueError(f"Conflicting audio hash for {speech['file']}")
            planned_audio[speech["file"]] = speech["sha256"]
        original = xml_path.read_text(encoding="utf-8-sig")
        patched_xml[xml_path] = patch_xml_text(
            original,
            music_plan["briefing_original"],
            mission["briefing"],
            music_plan["victory_original"],
            mission["victory"],
            speech_mission["speech"],
        )

    for name, expected_hash in planned_audio.items():
        source = PAYLOAD_AUDIO / name
        if not source.is_file():
            raise FileNotFoundError(f"Missing payload audio: {name}")
        actual = sha256(source)
        if actual != expected_hash:
            raise ValueError(f"Payload hash mismatch for {name}: expected {expected_hash}, found {actual}")

    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_root = campaign / ".reconquered-ptbr-media-backup" / stamp
    records: list[dict] = []

    for relative_name, source in sorted(localization_files.items()):
        relative = Path("localization") / Path(relative_name)
        destination = campaign / relative
        had_original = destination.exists()
        if had_original:
            backup = backup_root / relative
            backup.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(destination, backup)
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
        records.append(
            {
                "kind": "localization",
                "relative_path": relative.as_posix(),
                "had_original": had_original,
                "installed_sha256": sha256(destination),
            }
        )

    for xml_path, patched in patched_xml.items():
        relative = xml_path.relative_to(campaign)
        backup = backup_root / relative
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(xml_path, backup)
        xml_path.write_text(patched, encoding="utf-8", newline="")
        records.append(
            {
                "kind": "xml",
                "relative_path": relative.as_posix(),
                "had_original": True,
                "installed_sha256": sha256(xml_path),
            }
        )

    for name in sorted(planned_audio):
        source = PAYLOAD_AUDIO / name
        destination = campaign / "audio" / name
        had_original = destination.exists()
        if had_original:
            backup = backup_root / "audio" / name
            backup.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(destination, backup)
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
        records.append(
            {
                "kind": "audio",
                "relative_path": destination.relative_to(campaign).as_posix(),
                "had_original": had_original,
                "installed_sha256": sha256(destination),
            }
        )

    manifest = {
        "component": "Reconquered PT-BR audiovisual integration",
        "installer": "portable-python",
        "installed_utc": datetime.now(timezone.utc).isoformat(),
        "campaign_directory": str(campaign),
        "backup_directory": str(backup_root),
        "missions": len(music_plan["missions"]),
        "localization_files": len(localization_files),
        "speech_files": sum(len(item["speech"]) for item in speech_plan["missions"]),
        "music_files": len(music_plan["assets"]),
        "files": records,
    }
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Installed PT-BR media in: {campaign}")
    print("Installed 21 localization files; updated 20 XMLs; installed 197 speech files and 10 music files.")
    print(f"Backup: {backup_root}")


def uninstall(campaign: Path) -> None:
    manifest_path = campaign / INSTALL_MANIFEST
    if not manifest_path.is_file():
        raise FileNotFoundError("PT-BR media installation manifest not found.")
    manifest = load_json(manifest_path)
    backup_root = Path(manifest["backup_directory"])

    for record in manifest["files"]:
        destination = campaign / Path(record["relative_path"])
        if not destination.is_file():
            raise FileNotFoundError(f"Installed file is missing: {record['relative_path']}")
        actual = sha256(destination)
        if actual != record["installed_sha256"]:
            raise ValueError(
                f"File changed after installation; refusing to overwrite it: {record['relative_path']}"
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

    archived = backup_root / "uninstalled-media-install-manifest.json"
    shutil.copy2(manifest_path, archived)
    manifest_path.unlink()
    print("Removed PT-BR media integration and restored previous files.")
    print(f"Backup retained at: {backup_root}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    for command in ("install", "uninstall"):
        subparser = subparsers.add_parser(command)
        subparser.add_argument("campaign_directory")
    args = parser.parse_args()
    campaign = validate_campaign_path(args.campaign_directory)
    if args.command == "install":
        install(campaign)
    else:
        uninstall(campaign)


if __name__ == "__main__":
    main()
