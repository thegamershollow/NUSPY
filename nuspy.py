import os, struct, base64, \
    binascii, sys, zlib, \
    pathlib, requests, colorama

## Set up graceful script exiting ##
def exit_gracefully(signum=None, frame=None):
    print("\nExited")
    sys.exit(0)


try:
    # Try to use signal.SIGINT on Unix-based systems
    import signal

    signal.signal(signal.SIGINT, exit_gracefully)
except (ImportError, AttributeError):
    try:
        # Try to use ctypes.windll.kernel32 on Windows
        import ctypes

        kernel32 = ctypes.windll.kernel32

        # Enable Ctrl+C handling
        kernel32.SetConsoleCtrlHandler(exit_gracefully, 1)
    except:
        print(
            "Failed to set up signal handling. Graceful exit upon CTRL+C not supported"
        )
## Set up graceful script exiting ##

## Define global vars ##

MAX_BLOCK_SIZE = 131072

# Set title.cert, and title.tik info
CERT_DATA = zlib.decompress(
    base64.b64decode(
        "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"
    )
)

TIK_DATA = zlib.decompress(
    base64.b64decode(
        "eJxjYGRguRi39K3o6odSI5VmoAAE5eeX6Do7GkCAsW5EMJSZTJz+f29/nSMXMzIwnEEDKGavggJK/MfASJFu6gBGBhEguQaIRaBsENBggLiuBYyZIYL/CQBaOxUAoIEBhQ=="
    )
)

TIK_OFFSET = 0x140
## Define global vars ##


## Using slightly modified ticket patching from FunKiiU ##
def patch_ticket(ticket_data, offset, data):
    ticket_offset_start = TIK_OFFSET + offset
    ticket_offset_end = ticket_offset_start + len(data)
    ticket_data[ticket_offset_start:ticket_offset_end] = data

def patch_ticket_demo(ticket_data):
    # Offset to patch
    offset = 0x124
    
    # Demo data to be patched
    demo_data = b"\x00" * 64
    
    # Patch the ticket data with demo data
    patch_ticket(ticket_data, offset, demo_data)


def patch_ticket_dlc(ticket_data):
    # Offset to patch
    offset = 0x164
    
    # DLC data to be patched
    dlc_data = base64.b64decode("eNpjYGQQYWBgWAPEIgwQNghoADEjELeAMTNE8D8BwEBjAABCdSH/")
    dlc_data = zlib.decompress(dlc_data)
    
    # Patch the ticket data with DLC data
    patch_ticket(ticket_data, offset, dlc_data)


def generate_ticket(title_id, title_key, title_version, full_output_path, patch_demo=False, patch_dlc=False):
    # Create an empty bytearray to store the ticket data
    ticket_data = bytearray(TIK_DATA)
    
    # Update the title version, title ID, and title key in the ticket data
    ticket_data[TIK_OFFSET + 0xA6: TIK_OFFSET + 0xA8] = title_version
    ticket_data[TIK_OFFSET + 0x9C: TIK_OFFSET + 0xA4] = binascii.a2b_hex(title_id)
    ticket_data[TIK_OFFSET + 0x7F: TIK_OFFSET + 0x8F] = binascii.a2b_hex(title_key)
    
    # Determine the type of title ID and apply the corresponding patch function if applicable
    type_check = title_id[4:8]
    patch_functions = {
        "0002": patch_ticket_demo if patch_demo else None,
        "000C": patch_ticket_dlc if patch_dlc else None,
    }
    patch_func = patch_functions.get(type_check)
    if patch_func:
        patch_func(ticket_data)
    
    # Save the ticket data to the specified output path
    with open(full_output_path, "wb") as f:
        f.write(ticket_data)

## Using slightly modified ticket patching from FunKiiU ##

# function to look up values by key using lib
def get_value(key, key_value_pairs):
    upper_key = key.upper()  # convert to upper-case
    return key_value_pairs.get(upper_key)

# Main function, most stuff branches off from here
def main(title_id: str, version: str = None):
    # Install requirements if requirements.txt exists
    requirements_file = pathlib.Path("requirements.txt")
    if requirements_file.is_file():
        os.system("pip install -r requirements.txt")
        requirements_file.unlink()

    # Check if title_id is valid
    if len(title_id) not in (16, 32):
        print(f"{colorama.Fore.RED}Title ID is invalid length. Expected length: 16 or 32.")
        print(f"{colorama.Fore.GREEN}usage: {sys.argv[0]} <titleid>")
        print("Latest version is downloaded, if no version is specified.")
        print("This tool is for software archival purposes only. \n\
thegamershollow does not condone piracy of any kind as it is illegal.")
        sys.exit(1)

    # Get title key from NUSPY-Lib
    url = "https://raw.githubusercontent.com/thegamershollow/NUSPY-Lib/main/lib" # Using Korozin lib for now
    response = requests.get(url)
    content = response.text
    key_value_pairs = {}
    for line in content.splitlines():
        parts = line.split()
        if len(parts) >= 2:
            key = parts[0].upper()
            value = parts[1]
            key_value_pairs[key] = value
    title_key = get_value(title_id, key_value_pairs).upper()

    # Set up server URL(s)
    app_categories = {"0000", "0002", "000C", "000E"}
    base_url = f'http://{"ccs." if title_id[4:8] in app_categories else "nus."}cdn.c.shop.nintendowifi.net/ccs/download/{title_id}'

    # Check title ID validity
    if title_id[4:8] not in app_categories:
        print("Invalid Title ID / Title Key")
        sys.exit(1)

    # Set path naming
    suffix = {"0000": "_Game", "000E": "_Update", "000C": "_DLC", "0002": "_Demo"}.get(
        title_id[4:8], ""
    )
    downloads_dir = pathlib.Path("Downloads")
    downloads_dir.mkdir(exist_ok=True)
    root_dir = pathlib.Path("Downloads/" + title_id + suffix)
    root_dir.mkdir(exist_ok=True)

    # Download title.tmd
    tmd_url = f'{base_url}/tmd{"." + version if version else ""}'
    tmd = download(tmd_url, colorama.Fore.BLUE + f"Downloading: title.tmd...")
    contents = get_contents(tmd)

    # Write title.tmd contents
    with open(root_dir / "title.tmd", "wb") as f:
        f.write(tmd)

    # Get version from title.tmd
    with open(root_dir / "title.tmd", "rb") as f:
        tiver = f.read()[TIK_OFFSET + 0x9C : TIK_OFFSET + 0x9E]

    # Download title.tik if title is an update, otherwise generate fake ticket
    if "000E" in title_id[4:8]:
        tik_url = f"{base_url}/cetk{('.' + version) if version else ''}"
        tik = download(tik_url, colorama.Fore.BLUE + f"Downloading: title.tik...")
        with open(root_dir / "title.tik", "wb") as f:
            f.write(tik)
    else:
        # Generate fake ticket
        tik_file = root_dir / "title.tik"
        generate_ticket(title_id, title_key, tiver, tik_file)

    # Write cert data
    with open(root_dir / "title.cert", "wb") as f:
        f.write(CERT_DATA)

    # Download all contents
    for index, content in enumerate(contents, start=1):
        download_content(root_dir, base_url, contents, content, index, version)
    print(colorama.Fore.GREEN + f"\nSuccessfully downloaded Title to: {root_dir}")


# Function that sets up files to be downloaded by download function
def download_content(root_dir, base_url, contents, content, index, version=None):
    content_id, content_type, content_size, _ = content
    app_path = root_dir / f"{content_id}.app"
    
    if app_path.is_file() and app_path.stat().st_size == content_size:
        skip_msg = (
            colorama.Fore.YELLOW
            + "Skipping"
            + colorama.Fore.CYAN
            + f" [{index}/{len(contents)}] {colorama.Fore.RESET+content_id}.app due to existing file with proper size."
        )
        print(skip_msg)
        return
    
    app_msg = (
        colorama.Fore.BLUE
        + "Downloading"
        + colorama.Fore.CYAN
        + f" [{index}/{len(contents)}] {colorama.Fore.RESET+content_id}.app..."
        + colorama.Fore.RESET
    )
    app_size = f"({content_size/(1024**2):.2f} MiB)"
    app_content = download(f"{base_url}/{content_id}", app_msg, app_size)
    
    with open(app_path, "wb") as f:
        f.write(app_content)

    if content_type & 0x2:
        h3_path = root_dir / f"{content_id}.h3"
        
        if h3_path.is_file() and h3_path.stat().st_size == content_size:
            with open(h3_path, "rb") as f:
                existing_h3_content = f.read()
                
            if existing_h3_content == h3_content:
                skip_msg = (
                    colorama.Fore.YELLOW
                    + "Skipping"
                    + colorama.Fore.RESET
                    + f" {content_id}.h3 due to existing file with same content."
                )
                print(skip_msg)
                return
        
        h3_msg = (
            colorama.Fore.BLUE
            + "Downloading"
            + colorama.Fore.CYAN
            + f" [{index}/{len(contents)}] {colorama.Fore.RESET+content_id}.h3..."
            + colorama.Fore.RESET
        )
        h3_size = f"({content_size/(1024**2):.2f} MiB)"
        h3_content = download(f"{base_url}/{content_id}.h3", h3_msg, h3_size)
        
        with open(h3_path, "wb") as f:
            f.write(h3_content)


# Function that returns content info from tmd
def get_contents(tmd):
    content_count = struct.unpack(">H", tmd[0x1DE:0x1E0])[0]
    contents_list = []
    
    for content_index in range(content_count):
        content_id_bytes = tmd[0xB04 + (0x30 * content_index) : 0xB04 + (0x30 * content_index) + 0x4]
        content_id = binascii.hexlify(content_id_bytes).decode("utf-8")
        
        content_type_bytes = tmd[0xB0A + (0x30 * content_index) : 0xB0A + (0x30 * content_index) + 0x2]
        content_type = struct.unpack(">H", content_type_bytes)[0]
        
        content_size_bytes = tmd[0xB0C + (0x30 * content_index) : 0xB0C + (0x30 * content_index) + 0x8]
        content_size = struct.unpack(">Q", content_size_bytes)[0]
        
        contents_list.append((content_id, content_type, content_size, content_index + 1))
        
    print(colorama.Fore.RESET + "Contents:" + colorama.Fore.CYAN + f" {content_count}")
    total_size = sum(content[2] for content in contents_list)
    print(colorama.Fore.RESET + "Total size:" + f" ({total_size / (1024 ** 2)} MiB)")
    return contents_list


# Function that downloads the files
def download(url: str, message: str, message_suffix: str = "") -> bytes:
    response = requests.get(url, stream=True)
    response.raise_for_status()
    
    downloaded_content = b""
    total_size = int(response.headers.get("content-length", 0))
    
    # Download content in chunks
    if not total_size:
        downloaded_content = response.content
    else:
        print(message, end="", flush=True)
        downloaded_size = 0
        for chunk in response.iter_content(chunk_size=MAX_BLOCK_SIZE):
            downloaded_content += chunk
            downloaded_size += len(chunk)
            
            # Show download progress
            percent = round(downloaded_size * 100.0 / total_size, 1)
            downloaded_size_mb = downloaded_size / (1024 ** 2)
            total_size_mb = total_size / (1024 ** 2)
            progress_text = f"\r{message} ({downloaded_size_mb:.2f} MiB / {total_size_mb:.2f} MiB) ({percent}%) {message_suffix}"
            print(progress_text, end="", flush=True)
        print("")
        
    return downloaded_content


if __name__ == "__main__":
    # Check for the correct number of command line arguments
    if len(sys.argv) == 1:
        print(f"Usage: {sys.argv[0]} <titleid>")
        print("Latest version is downloaded if no version is specified.")
        sys.exit(1)

    # Call the main function with the specified arguments
    try:
        main(title_id=sys.argv[1].upper(),
            version=sys.argv[2] if len(sys.argv) > 2 else None)
    except IndexError:
        # Handle invalid number of arguments
        print(colorama.Fore.RED + "Invalid number of arguments")
        print(f"Usage: {sys.argv[0]} <titleid>")
        print("Latest version  of the title is downloaded if no version is specified.")
        print("For help go to https://github.com/thegamershollow/NUSPY/wiki")
        sys.exit(1)
