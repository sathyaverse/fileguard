"""
FileGuard - File Signature & Extension Mismatch Detection Engine
Author: FileGuard Security Team
"""

import os
import io
import json
import zipfile
import hashlib
import mimetypes
from typing import Dict, Any, List, Optional, Tuple

# Comprehensive signature definitions
# Format: (name, category, magic_bytes, offset, valid_extensions, mime_type, threat_level, description)
SIGNATURES_TABLE = [
    # Executables / High Risk Binaries
    {
        "name": "Windows Portable Executable (EXE / DLL / SYS / SCR)",
        "category": "Executable",
        "magic": [b"\x4D\x5A"],  # MZ
        "offset": 0,
        "valid_extensions": ["exe", "dll", "sys", "scr", "cpl", "ocx", "fon", "drv"],
        "mime": "application/vnd.microsoft.portable-executable",
        "threat_level": "Critical",
        "description": "Standard Windows binary format. Attackers frequently disguise EXEs as PDFs or images."
    },
    {
        "name": "Linux Executable and Linkable Format (ELF)",
        "category": "Executable",
        "magic": [b"\x7F\x45\x4C\x46"],  # \x7fELF
        "offset": 0,
        "valid_extensions": ["elf", "bin", "so", "out"],
        "mime": "application/x-executable",
        "threat_level": "Critical",
        "description": "Unix/Linux executable binary format. High risk if disguised as document."
    },
    {
        "name": "macOS Mach-O Binary (32-bit)",
        "category": "Executable",
        "magic": [b"\xFE\xED\xFA\xCE", b"\xCE\xFA\xED\xFE"],
        "offset": 0,
        "valid_extensions": ["macho", "dylib", "bundle", "bin"],
        "mime": "application/x-mach-binary",
        "threat_level": "Critical",
        "description": "Apple macOS 32-bit executable binary."
    },
    {
        "name": "macOS Mach-O Binary (64-bit)",
        "category": "Executable",
        "magic": [b"\xFE\xED\xFA\xCF", b"\xCF\xFA\xED\xFE"],
        "offset": 0,
        "valid_extensions": ["macho", "dylib", "bundle", "bin"],
        "mime": "application/x-mach-binary",
        "threat_level": "Critical",
        "description": "Apple macOS 64-bit executable binary."
    },
    {
        "name": "Java Bytecode / Mach-O Fat Binary",
        "category": "Executable",
        "magic": [b"\xCA\xFE\xBA\xBE"],
        "offset": 0,
        "valid_extensions": ["class", "macho", "dylib"],
        "mime": "application/java-vm",
        "threat_level": "High",
        "description": "Compiled Java class file or macOS Universal Fat binary."
    },
    {
        "name": "Android Dalvik Executable (DEX)",
        "category": "Executable",
        "magic": [b"dex\n035\x00", b"dex\n037\x00", b"dex\n038\x00", b"dex\n039\x00"],
        "offset": 0,
        "valid_extensions": ["dex"],
        "mime": "application/vnd.android.dex",
        "threat_level": "High",
        "description": "Android runtime application bytecode."
    },
    {
        "name": "WebAssembly Binary (WASM)",
        "category": "Executable",
        "magic": [b"\x00asm"],
        "offset": 0,
        "valid_extensions": ["wasm"],
        "mime": "application/wasm",
        "threat_level": "Medium",
        "description": "Compiled WebAssembly binary for browser/WASI runtimes."
    },
    {
        "name": "Windows Shell Shortcut (LNK)",
        "category": "System",
        "magic": [b"\x4C\x00\x00\x00\x01\x14\x02\x00"],
        "offset": 0,
        "valid_extensions": ["lnk"],
        "mime": "application/x-ms-shortcut",
        "threat_level": "High",
        "description": "Windows link/shortcut. Frequently weaponized with PowerShell command payloads."
    },

    # Documents
    {
        "name": "Portable Document Format (PDF)",
        "category": "Document",
        "magic": [b"%PDF-"],
        "offset": 0,
        "valid_extensions": ["pdf"],
        "mime": "application/pdf",
        "threat_level": "Low",
        "description": "Standard Adobe PDF electronic document."
    },
    {
        "name": "Rich Text Format (RTF)",
        "category": "Document",
        "magic": [b"{\\rtf"],
        "offset": 0,
        "valid_extensions": ["rtf"],
        "mime": "application/rtf",
        "threat_level": "Medium",
        "description": "Rich Text document. Often targeted for MS Word memory corruption CVEs."
    },
    {
        "name": "Microsoft Office Legacy (OLE2 Compound Document / CFBF)",
        "category": "Document",
        "magic": [b"\xD0\xCF\x11\xE0\xA1\xB1\x1A\xE1"],
        "offset": 0,
        "valid_extensions": ["doc", "xls", "ppt", "msg", "vsd", "dot", "xlt"],
        "mime": "application/x-ole-storage",
        "threat_level": "Medium",
        "description": "Legacy binary Microsoft Word, Excel, or PowerPoint document."
    },
    {
        "name": "PostScript Document",
        "category": "Document",
        "magic": [b"%!PS-Adobe", b"%!PS"],
        "offset": 0,
        "valid_extensions": ["ps", "eps"],
        "mime": "application/postscript",
        "threat_level": "Low",
        "description": "Adobe PostScript vector document/image."
    },

    # Images
    {
        "name": "JPEG Image",
        "category": "Image",
        "magic": [b"\xFF\xD8\xFF"],
        "offset": 0,
        "valid_extensions": ["jpg", "jpeg", "jfif", "jpe", "jif"],
        "mime": "image/jpeg",
        "threat_level": "Low",
        "description": "Joint Photographic Experts Group raster image."
    },
    {
        "name": "PNG Image",
        "category": "Image",
        "magic": [b"\x89PNG\r\n\x1a\n"],
        "offset": 0,
        "valid_extensions": ["png"],
        "mime": "image/png",
        "threat_level": "Low",
        "description": "Portable Network Graphics lossless image."
    },
    {
        "name": "GIF Image",
        "category": "Image",
        "magic": [b"GIF87a", b"GIF89a"],
        "offset": 0,
        "valid_extensions": ["gif"],
        "mime": "image/gif",
        "threat_level": "Low",
        "description": "Graphics Interchange Format bitmap image."
    },
    {
        "name": "BMP Bitmap Image",
        "category": "Image",
        "magic": [b"BM"],
        "offset": 0,
        "valid_extensions": ["bmp", "dib"],
        "mime": "image/bmp",
        "threat_level": "Low",
        "description": "Standard uncompressed Windows bitmap image."
    },
    {
        "name": "TIFF Image (Little-Endian)",
        "category": "Image",
        "magic": [b"II*\x00"],
        "offset": 0,
        "valid_extensions": ["tif", "tiff"],
        "mime": "image/tiff",
        "threat_level": "Low",
        "description": "Tagged Image File Format (Intel little-endian)."
    },
    {
        "name": "TIFF Image (Big-Endian)",
        "category": "Image",
        "magic": [b"MM\x00*"],
        "offset": 0,
        "valid_extensions": ["tif", "tiff"],
        "mime": "image/tiff",
        "threat_level": "Low",
        "description": "Tagged Image File Format (Motorola big-endian)."
    },
    {
        "name": "Windows Icon / Cursor",
        "category": "Image",
        "magic": [b"\x00\x00\x01\x00", b"\x00\x00\x02\x00"],
        "offset": 0,
        "valid_extensions": ["ico", "cur"],
        "mime": "image/x-icon",
        "threat_level": "Low",
        "description": "Windows icon or cursor graphic resource."
    },
    {
        "name": "Adobe Photoshop Document (PSD)",
        "category": "Image",
        "magic": [b"8BPS"],
        "offset": 0,
        "valid_extensions": ["psd"],
        "mime": "image/vnd.adobe.photoshop",
        "threat_level": "Low",
        "description": "Layered Adobe Photoshop image file."
    },

    # Archives & Compressed Containers
    {
        "name": "7-Zip Archive",
        "category": "Archive",
        "magic": [b"\x37\x7A\xBC\xAF\x27\x1C"],
        "offset": 0,
        "valid_extensions": ["7z"],
        "mime": "application/x-7z-compressed",
        "threat_level": "Low",
        "description": "High-compression 7-Zip open archive container."
    },
    {
        "name": "RAR Archive",
        "category": "Archive",
        "magic": [b"Rar!\x1A\x07\x00", b"Rar!\x1A\x07\x01\x00"],
        "offset": 0,
        "valid_extensions": ["rar"],
        "mime": "application/vnd.rar",
        "threat_level": "Low",
        "description": "Roshal Archive compressed container."
    },
    {
        "name": "GZIP Archive",
        "category": "Archive",
        "magic": [b"\x1F\x8B"],
        "offset": 0,
        "valid_extensions": ["gz", "tgz", "tar.gz"],
        "mime": "application/gzip",
        "threat_level": "Low",
        "description": "GNU zip compressed stream/archive."
    },
    {
        "name": "BZIP2 Archive",
        "category": "Archive",
        "magic": [b"BZh"],
        "offset": 0,
        "valid_extensions": ["bz2", "tbz2"],
        "mime": "application/x-bzip2",
        "threat_level": "Low",
        "description": "Burrows-Wheeler block-sorting archive."
    },
    {
        "name": "XZ Archive",
        "category": "Archive",
        "magic": [b"\xFD7zXZ\x00"],
        "offset": 0,
        "valid_extensions": ["xz", "txz"],
        "mime": "application/x-xz",
        "threat_level": "Low",
        "description": "LZMA2 compression algorithm archive."
    },
    {
        "name": "Microsoft Cabinet (CAB)",
        "category": "Archive",
        "magic": [b"MSCF"],
        "offset": 0,
        "valid_extensions": ["cab"],
        "mime": "application/vnd.ms-cab-compressed",
        "threat_level": "Medium",
        "description": "Microsoft Windows installation archive package."
    },

    # Audio & Video
    {
        "name": "MP3 Audio (with ID3 Tag)",
        "category": "Audio/Video",
        "magic": [b"ID3"],
        "offset": 0,
        "valid_extensions": ["mp3"],
        "mime": "audio/mpeg",
        "threat_level": "Low",
        "description": "MPEG-1 Audio Layer III with metadata tag header."
    },
    {
        "name": "FLAC Audio",
        "category": "Audio/Video",
        "magic": [b"fLaC"],
        "offset": 0,
        "valid_extensions": ["flac"],
        "mime": "audio/flac",
        "threat_level": "Low",
        "description": "Free Lossless Audio Codec stream."
    },
    {
        "name": "Ogg Multimedia Container",
        "category": "Audio/Video",
        "magic": [b"OggS"],
        "offset": 0,
        "valid_extensions": ["ogg", "oga", "ogv", "opus"],
        "mime": "application/ogg",
        "threat_level": "Low",
        "description": "Xiph.Org open multimedia bitstream container."
    },
    {
        "name": "Matroska Multimedia (MKV / WebM)",
        "category": "Audio/Video",
        "magic": [b"\x1A\x45\xDF\xA3"],
        "offset": 0,
        "valid_extensions": ["mkv", "webm", "mka"],
        "mime": "video/x-matroska",
        "threat_level": "Low",
        "description": "EBML extensible multimedia container."
    },
    {
        "name": "MIDI Audio",
        "category": "Audio/Video",
        "magic": [b"MThd"],
        "offset": 0,
        "valid_extensions": ["mid", "midi"],
        "mime": "audio/midi",
        "threat_level": "Low",
        "description": "Musical Instrument Digital Interface audio file."
    },

    # Database
    {
        "name": "SQLite 3 Database",
        "category": "Database",
        "magic": [b"SQLite format 3\x00"],
        "offset": 0,
        "valid_extensions": ["sqlite", "db", "sqlite3", "db3"],
        "mime": "application/vnd.sqlite3",
        "threat_level": "Low",
        "description": "Self-contained serverless SQL database engine file."
    }
]

# Helper for formatted byte representation
def format_bytes(num_bytes: int) -> str:
    """Formats raw bytes into human readable KB/MB format."""
    if num_bytes < 1024:
        return f"{num_bytes} B"
    elif num_bytes < 1024 * 1024:
        return f"{num_bytes / 1024:.2f} KB ({num_bytes:,} bytes)"
    elif num_bytes < 1024 * 1024 * 1024:
        return f"{num_bytes / (1024 * 1024):.2f} MB ({num_bytes:,} bytes)"
    else:
        return f"{num_bytes / (1024 * 1024 * 1024):.2f} GB ({num_bytes:,} bytes)"

def bytes_to_hex(data: bytes, length: int = 16) -> str:
    """Converts bytes to uppercase spaced hex string."""
    sample = data[:length]
    return " ".join(f"{b:02X}" for b in sample)

def bytes_to_ascii(data: bytes, length: int = 16) -> str:
    """Converts bytes to safe ASCII preview representation."""
    sample = data[:length]
    return "".join(chr(b) if 32 <= b <= 126 else "." for b in sample)

def calculate_hashes(data: bytes) -> Dict[str, str]:
    """Generates cryptographic fingerprints for threat intelligence."""
    return {
        "md5": hashlib.md5(data).hexdigest(),
        "sha1": hashlib.sha1(data).hexdigest(),
        "sha256": hashlib.sha256(data).hexdigest()
    }

def check_filename_anomalies(filename: str) -> List[Dict[str, str]]:
    """
    Checks for common cyber attacker obfuscation techniques in file names:
    - Right-to-Left Override (RLO) character (\u202E)
    - Double extensions (e.g. invoice.pdf.exe)
    - Excessive whitespace masking
    """
    anomalies = []
    
    # 1. RLO character spoofing
    if "\u202E" in filename or "\u202D" in filename or "\u202C" in filename or "\u200E" in filename:
        anomalies.append({
            "type": "Unicode Bidirectional Override Spoofing (RLO)",
            "severity": "Critical",
            "detail": "Filename contains hidden Unicode override characters (U+202E) used to visually reverse file extensions and deceive victims into opening dangerous executables."
        })

    # 2. Double extensions
    parts = filename.split(".")
    if len(parts) > 2:
        ext = parts[-1].lower()
        second_ext = parts[-2].lower()
        dangerous_exts = ["exe", "scr", "vbs", "bat", "cmd", "ps1", "js", "wsf", "hta", "pif", "cpl"]
        luring_exts = ["pdf", "doc", "docx", "xls", "xlsx", "jpg", "png", "txt", "mp4", "zip"]
        
        if ext in dangerous_exts and second_ext in luring_exts:
            anomalies.append({
                "type": "Double Extension Disguise Attack",
                "severity": "Critical",
                "detail": f"File uses double extensions (.{second_ext}.{ext}). Systems with 'Hide extensions for known file types' will show this dangerous executable as a benign {second_ext.upper()} document."
            })
        elif ext in dangerous_exts:
            anomalies.append({
                "type": "Multiple Extensions Detected",
                "severity": "High",
                "detail": f"File contains multiple dot separators ending with executable extension '.{ext}'."
            })

    # 3. Hidden spaces masking extension
    if "  " in filename and filename.count(".") > 1:
        anomalies.append({
            "type": "Whitespace Extension Masking",
            "severity": "High",
            "detail": "Filename has multiple padded spaces intended to push the real executable extension off the visible desktop window."
        })

    return anomalies

def inspect_riff_format(data: bytes) -> Optional[Tuple[str, str, str, str]]:
    """Special handler for RIFF family (WEBP, WAV, AVI)."""
    if len(data) >= 12 and data[:4] == b"RIFF":
        riff_type = data[8:12]
        if riff_type == b"WEBP":
            return ("WebP Image", "Image", "webp", "image/webp")
        elif riff_type == b"WAVE":
            return ("WAV Audio", "Audio/Video", "wav", "audio/wav")
        elif riff_type == b"AVI ":
            return ("AVI Video", "Audio/Video", "avi", "video/x-msvideo")
    return None

def inspect_mp4_format(data: bytes) -> Optional[Tuple[str, str, str, str]]:
    """Inspects ISO base media file format (MP4, M4A, MOV)."""
    if len(data) >= 12:
        if data[4:8] == b"ftyp":
            brand = data[8:12]
            if brand in [b"M4A ", b"M4B ", b"m4a "]:
                return ("M4A Audio", "Audio/Video", "m4a", "audio/mp4")
            elif brand in [b"qt  ", b"moov"]:
                return ("QuickTime Movie (MOV)", "Audio/Video", "mov", "video/quicktime")
            else:
                return ("MP4 Video Container", "Audio/Video", "mp4", "video/mp4")
    return None

def inspect_zip_container(data: bytes) -> Tuple[str, str, List[str], str]:
    """
    Deeply examines ZIP headers and contents to distinguish:
    - Microsoft Word (.docx)
    - Microsoft Excel (.xlsx)
    - Microsoft PowerPoint (.pptx)
    - Android Application (.apk)
    - Java Archive (.jar)
    - Generic ZIP archive (.zip)
    """
    try:
        with zipfile.ZipFile(io.BytesIO(data), "r") as zf:
            file_names = set(zf.namelist())

            # Office Open XML Documents
            if "word/document.xml" in file_names or any(n.startswith("word/") for n in file_names):
                return (
                    "Microsoft Word Document (OOXML)",
                    "Document",
                    ["docx", "docm", "dotx"],
                    "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )
            if "xl/workbook.xml" in file_names or any(n.startswith("xl/") for n in file_names):
                return (
                    "Microsoft Excel Spreadsheet (OOXML)",
                    "Document",
                    ["xlsx", "xlsm", "xltx"],
                    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            if "ppt/presentation.xml" in file_names or any(n.startswith("ppt/") for n in file_names):
                return (
                    "Microsoft PowerPoint Presentation (OOXML)",
                    "Document",
                    ["pptx", "pptm", "potx"],
                    "application/vnd.openxmlformats-officedocument.presentationml.presentation"
                )
            if "AndroidManifest.xml" in file_names:
                return (
                    "Android Application Package (APK)",
                    "Executable",
                    ["apk"],
                    "application/vnd.android.package-archive"
                )
            if "META-INF/MANIFEST.MF" in file_names:
                return (
                    "Java Archive (JAR)",
                    "Executable",
                    ["jar"],
                    "application/java-archive"
                )
            if "mimetype" in file_names:
                try:
                    mime_content = zf.read("mimetype").decode("utf-8", errors="ignore").strip()
                    if "epub" in mime_content:
                        return ("EPUB Digital Book", "Document", ["epub"], "application/epub+zip")
                except Exception:
                    pass
    except Exception:
        # Corrupted zip or partial stream, still has PK magic bytes
        pass

    return (
        "Standard ZIP Archive",
        "Archive",
        ["zip", "cbz"],
        "application/zip"
    )

def inspect_text_or_script(data: bytes) -> Optional[Tuple[str, str, List[str], str]]:
    """Checks whether the file is valid UTF-8/ASCII text or a script."""
    if not data:
        return ("Empty File", "Text", ["txt"], "text/plain")

    # If first 512 bytes contain null bytes, it's virtually guaranteed binary, not plain text
    sample = data[:512]
    if b"\x00" in sample:
        return None

    # Check for Shebang script
    if sample.startswith(b"#!"):
        first_line = sample.split(b"\n")[0].decode("utf-8", errors="ignore")
        if "python" in first_line:
            return ("Python Script", "Script", ["py", "pyw"], "text/x-python")
        elif "bash" in first_line or "sh" in first_line:
            return ("Shell Script (Bash/POSIX)", "Script", ["sh", "bash"], "application/x-sh")
        else:
            return ("Executable Script (Shebang)", "Script", ["sh", "py", "pl", "rb"], "text/x-script")

    # Check for XML / SVG / HTML
    stripped_sample = sample.lstrip()
    if stripped_sample.startswith(b"<?xml") or stripped_sample.startswith(b"<svg") or b"<svg" in sample:
        if b"<svg" in sample or b"xmlns=\"http://www.w3.org/2000/svg\"" in sample:
            return ("Scalable Vector Graphics (SVG)", "Image", ["svg"], "image/svg+xml")
        return ("XML Document", "Document", ["xml"], "application/xml")
    
    if stripped_sample.lower().startswith((b"<!doctype html", b"<html")):
        return ("HTML Document / Web Page", "Document", ["html", "htm"], "text/html")

    # Check for JSON
    if stripped_sample.startswith((b"{", b"[")):
        try:
            # Try parsing a small snippet or full data if under 1MB
            if len(data) < 1024 * 1024:
                json.loads(data.decode("utf-8"))
                return ("JSON Data Document", "Document", ["json"], "application/json")
        except Exception:
            pass

    # General UTF-8 text check
    try:
        sample.decode("utf-8")
        return ("Plain Text Document", "Text", ["txt", "log", "csv", "md", "cfg", "ini"], "text/plain")
    except UnicodeDecodeError:
        return None

def analyze_file(data: bytes, filename: str) -> Dict[str, Any]:
    """
    Main detection entrypoint:
    1. Extracts declared extension.
    2. Reads magic bytes at offset 0 and specific offsets.
    3. Identifies actual format and category.
    4. Compares declared extension with actual format.
    5. Categorizes status into:
       - SAFE: Format Match
       - SUSPICIOUS: Mismatch / Dangerous Disguise
       - UNKNOWN: Unsupported format
    6. Extracts hashes, MIME, file size, anomalies, and safety advice.
    """
    file_size = len(data)
    parts = filename.rsplit(".", 1)
    declared_ext = parts[1].lower().strip() if len(parts) > 1 else "(none)"
    
    anomalies = check_filename_anomalies(filename)
    hashes = calculate_hashes(data)
    
    hex_preview = bytes_to_hex(data, 16)
    ascii_preview = bytes_to_ascii(data, 16)

    # Detection logic
    detected_format: Optional[str] = None
    detected_category: str = "Unknown"
    valid_exts: List[str] = []
    mime_type: str = "application/octet-stream"
    threat_level: str = "Info"
    description: str = ""
    is_zip_container = False

    # 1. Check RIFF formats (WEBP, WAV, AVI)
    riff_res = inspect_riff_format(data)
    if riff_res:
        detected_format, detected_category, ext_match, mime_type = riff_res
        valid_exts = [ext_match]
        description = f"RIFF multimedia container identified as {detected_format}."
        threat_level = "Low"

    # 2. Check MP4 container
    if not detected_format:
        mp4_res = inspect_mp4_format(data)
        if mp4_res:
            detected_format, detected_category, ext_match, mime_type = mp4_res
            valid_exts = [ext_match, "mp4", "m4v", "mov"]
            description = f"ISO Base Media file format identified as {detected_format}."
            threat_level = "Low"

    # 3. Check ZIP containers (including DOCX, XLSX, PPTX, APK, JAR)
    if not detected_format and len(data) >= 4 and data[:4] in [b"\x50\x4B\x03\x04", b"\x50\x4B\x05\x06", b"\x50\x4B\x07\x08"]:
        is_zip_container = True
        detected_format, detected_category, valid_exts, mime_type = inspect_zip_container(data)
        description = "Zip-based package container verified via internal directory structure."
        threat_level = "High" if detected_category == "Executable" else "Low"

    # 4. Check Signature Table
    if not detected_format:
        for entry in SIGNATURES_TABLE:
            offset = entry["offset"]
            for magic in entry["magic"]:
                magic_len = len(magic)
                if len(data) >= offset + magic_len:
                    if data[offset:offset + magic_len] == magic:
                        detected_format = entry["name"]
                        detected_category = entry["category"]
                        valid_exts = entry["valid_extensions"]
                        mime_type = entry["mime"]
                        threat_level = entry["threat_level"]
                        description = entry["description"]
                        break
            if detected_format:
                break

    # 5. Check Plaintext / Scripts if no binary magic matched
    if not detected_format:
        text_res = inspect_text_or_script(data)
        if text_res:
            detected_format, detected_category, valid_exts, mime_type = text_res
            description = "Printable text structure with valid character encoding."
            threat_level = "Medium" if detected_category == "Script" else "Low"

    # 6. Fallback MIME detection from standard library
    if not mime_type or mime_type == "application/octet-stream":
        guessed, _ = mimetypes.guess_type(filename)
        if guessed:
            mime_type = guessed

    # Status determination: SAFE, SUSPICIOUS, or UNKNOWN
    status: str = "UNKNOWN"
    status_title: str = "Unknown or Unsupported Format"
    status_message: str = "File format could not be confidently identified."
    risk_summary: str = ""

    if detected_format is None:
        status = "UNKNOWN"
        status_title = "Unknown or Unsupported Format"
        status_message = "File format could not be confidently identified."
        detected_format = "Unrecognized Binary / Custom Format"
        detected_category = "Unknown"
        risk_summary = (
            "The file header bytes do not correspond to any known common file signature. "
            "It may be a proprietary internal format, an encrypted container, or an uncommon binary. "
            "Proceed with heightened caution and verify the source."
        )
    else:
        # Check if declared extension is in valid_extensions
        # Also treat OOXML / ZIP edge cases safely
        is_extension_match = False
        
        if declared_ext in valid_exts:
            is_extension_match = True
        elif is_zip_container and declared_ext in ["zip", "docx", "xlsx", "pptx", "jar", "apk", "epub"]:
            # If it's a generic zip and declared is zip
            is_extension_match = True
        elif detected_category == "Text" and declared_ext in ["txt", "log", "csv", "json", "xml", "md", "ini", "cfg", "yaml", "yml", "sql"]:
            is_extension_match = True

        if is_extension_match:
            # Check for anomaly overrides (e.g. double extension like file.pdf.exe is dangerous even if .exe matches)
            if any(a["severity"] == "Critical" for a in anomalies):
                status = "SUSPICIOUS"
                status_title = "Suspicious Disguise Detected"
                status_message = "Warning! The file has deceptive naming patterns and poses a security risk."
                risk_summary = (
                    "Although the file matches its trailing extension, high-severity naming anomalies "
                    "(such as double extensions or Unicode RLO tricks) were detected. "
                    "This is a common tactic to trick victims into executing harmful payloads."
                )
            else:
                status = "SAFE"
                status_title = "Format Match"
                status_message = "File extension and actual file format match."
                risk_summary = (
                    f"The declared extension (.{declared_ext}) corresponds directly to the verified "
                    f"magic byte signature for {detected_format}. No format spoofing detected."
                )
        else:
            status = "SUSPICIOUS"
            status_title = "Suspicious Mismatch"
            status_message = "Warning! The file extension does not match its actual format."
            
            # Highlight severe attacks: Executable disguised as Document or Image
            if detected_category in ["Executable", "Script"]:
                risk_summary = (
                    f"CRITICAL SECURITY ALERT: The file is named with extension '.{declared_ext}', "
                    f"but its internal binary structure is an {detected_format.upper()} ({detected_category}). "
                    f"Attackers disguise executable payloads as documents or pictures to bypass human scrutiny "
                    f"and trigger code execution when opened!"
                )
            else:
                risk_summary = (
                    f"FORMAT MISMATCH DETECTED: The file is labeled as '.{declared_ext}', but its internal bytes "
                    f"indicate it is actually a {detected_format} (expected extension: {', '.join('.' + e for e in valid_exts[:4])}). "
                    f"This mismatch may indicate intentional concealment, extension tampering, or file corruption."
                )

    disclaimer = (
        "IMPORTANT DISCLAIMER: Format verification confirms whether the file's extension aligns with its "
        "internal header signature. A matching format DOES NOT guarantee the file is free of embedded malicious "
        "macros, exploits, steganography, or payload code. Always maintain robust endpoint protection."
    )

    return {
        "filename": filename,
        "declared_extension": declared_ext if declared_ext != "(none)" else "None",
        "file_size": file_size,
        "file_size_formatted": format_bytes(file_size),
        "actual_format": detected_format,
        "actual_category": detected_category,
        "valid_extensions": valid_exts,
        "magic_hex": hex_preview,
        "magic_ascii": ascii_preview,
        "status": status,
        "status_title": status_title,
        "status_message": status_message,
        "threat_level": threat_level,
        "description": description,
        "risk_summary": risk_summary,
        "anomalies": anomalies,
        "hashes": hashes,
        "mime_type": mime_type,
        "disclaimer": disclaimer
    }
