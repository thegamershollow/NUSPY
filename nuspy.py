import struct, base64, binascii, sys, urllib.error, urllib.request, zlib, pathlib


MAX_BLOCK_SIZE = 10 * 1024 * 50 # up the block size a bit to hopefully increase dl speeds
CERT_DATA = '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' # placeholder
TIK_DATA = binascii.a2b_hex('00010004d15ea5ed15abe11ad15ea5ed15abe11ad15ea5ed15abe11ad15ea5ed15abe11ad15ea5ed15abe11ad15ea5ed15abe11ad15ea5ed15abe11ad15ea5ed15abe11ad15ea5ed15abe11ad15ea5ed15abe11ad15ea5ed15abe11ad15ea5ed15abe11ad15ea5ed15abe11ad15ea5ed15abe11ad15ea5ed15abe11ad15ea5ed15abe11ad15ea5ed15abe11ad15ea5ed15abe11ad15ea5ed15abe11ad15ea5ed15abe11ad15ea5ed15abe11ad15ea5ed15abe11ad15ea5ed15abe11ad15ea5ed15abe11ad15ea5ed15abe11ad15ea5ed15abe11ad15ea5ed15abe11ad15ea5ed15abe11ad15ea5ed15abe11ad15ea5ed15abe11ad15ea5ed15abe11ad15ea5ed15abe11a000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000526f6f742d434130303030303030332d585330303030303030630000000000000000000000000000000000000000000000000000000000000000000000000000feedfacefeedfacefeedfacefeedfacefeedfacefeedfacefeedfacefeedfacefeedfacefeedfacefeedfacefeedfacefeedfacefeedfacefeedface010000cccccccccccccccccccccccccccccccc00000000000000000000000000aaaaaaaaaaaaaaaa00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000010014000000ac000000140001001400000000000000280000000100000084000000840003000000000000ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')
TIK_OFFSET = 0x140


## Using slightly modified ticket patching from FunKiiU ##
def patch_ticket(tikdata, offset, data):
    """Patch a Wii U ticket with the given data."""
    tikdata[TIK_OFFSET + offset : TIK_OFFSET + offset + len(data)] = data


def patch_ticket_demo(tikdata):
    """Patch a Wii U ticket with demo data."""
    patch_ticket(tikdata, 0x124, bytes([0x00] * 64))


def patch_ticket_dlc(tikdata):
    """Patch a Wii U ticket with DLC data."""
    b64decompress = lambda d: zlib.decompress(base64.b64decode(d))
    patch_ticket(tikdata, 0x164, b64decompress('eNpjYGQQYWBgWAPEIgwQNghoADEjELeAMTNE8D8BwEBjAABCdSH/'))  # placeholder


def generate_ticket(title_id, title_key, title_version, fulloutputpath, patch_demo=False, patch_dlc=False):
    """Generate a Wii U ticket for the given title ID, title key, and title version."""
    tikdata = bytearray(TIK_DATA)
    tikdata[TIK_OFFSET + 0xA6:TIK_OFFSET + 0xA8] = title_version
    tikdata[TIK_OFFSET + 0x9C:TIK_OFFSET + 0xA4] = binascii.a2b_hex(title_id)
    tikdata[TIK_OFFSET + 0x7F:TIK_OFFSET + 0x8F] = binascii.a2b_hex(title_key)
    typecheck = title_id[4:8]
    if typecheck == '0002' and patch_demo:
        patch_ticket_demo(tikdata)
    elif typecheck == '000C' and patch_dlc:
        patch_ticket_dlc(tikdata)
    open(fulloutputpath, 'wb').write(tikdata)
## Using slightly modified ticket patching from FunKiiU ##    


def main(title_id: str, title_key: str, version: str = None):
    if len(title_id) != 16:
        print('Title ID is invalid length. Expected length: 16')
        print(f'usage: {sys.argv[0]} <titleid> <titlekey> [version]')
        print('Latest version is downloaded, if no version is specified.')
        sys.exit(1)
        
    if len(title_key) != 32:
        print('Title Key is invalid length. Expected length: 32')
        print(f'usage: {sys.argv[0]} <titleid> <titlekey> [version]')
        print('Latest version is downloaded, if no version is specified.')
        sys.exit(1)

    app_categories = {'0000', '0002', '000C', '000E'}
    base_url = f'http://ccs.cdn.c.shop.nintendowifi.net/ccs/download/{title_id}'
    if title_id[4:8] not in app_categories:
        base_url = f'http://nus.cdn.c.shop.nintendowifi.net/ccs/download/{title_id}'
        print('Invalid Title ID / Title Key')
        sys.exit(1)
    
    if '0000' in title_id[4:8]:
        root_dir = pathlib.Path(title_id + '_Game')
    if '000E' in title_id[4:8]:
        root_dir = pathlib.Path(title_id + '_Update')
    if '000C' in title_id[4:8]:
        root_dir = pathlib.Path(title_id + '_DLC')
    if '0002' in title_id[4:8]:
        root_dir = pathlib.Path(title_id + '_Demo')
    
    root_dir.mkdir(exist_ok=True)
            
    tmd_url = f'{base_url}/tmd{"." + version if version else ""}'
    tmd = download(tmd_url, f'Downloading: title.tmd...')
    contents = get_contents(tmd)
    
    with open(root_dir / 'title.tmd', 'wb') as f:
        f.write(tmd)
        
    with open(root_dir / 'title.tmd', 'rb') as f:
        tiver = f.read()[TIK_OFFSET + 0x9C:TIK_OFFSET + 0x9E]
        
    # If title is an update, get ticket from NUS
    if '000E' in title_id[4:8]:
        tik_url = f"{base_url}/cetk{('.' + version) if version else ''}"
        tik = download(tik_url, f'Downloading: title.tik...')
        
        with open(root_dir / 'title.tik', 'wb') as f:
            f.write(tik)
    else:
        tik_file = root_dir / 'title.tik'
        generate_ticket(title_id, title_key, tiver, tik_file)
    
    with open(root_dir / 'title.cert', 'wb') as f:
        f.write(zlib.decompress(base64.b64decode(CERT_DATA)))

    for index, content in enumerate(contents, start=1):
        download_content(root_dir, base_url, contents, content, index, version)


def download_content(root_dir, base_url, contents, content, index, version=None):
    content_id, content_type, content_size, _ = content
    app_path = root_dir / f'{content_id}.app'
    if app_path.is_file() and app_path.stat().st_size == content_size:
        print(f'Skipping [{index}/{len(contents)}] {content_id}.app due to existing file with proper size.')
        return
    message = f'Downloading [{index}/{len(contents)}] {content_id}.app...'
    message_suffix = f'({content_size/(1024**2):.2f} MiB)'
    app_content = download(f"{base_url}/{content_id}", message, message_suffix)
    with open(app_path, 'wb') as f:
        f.write(app_content)

    if content_type & 0x2:
        h3_path = root_dir / f'{content_id}.h3'
        if h3_path.is_file() and h3_path.stat().st_size == content_size:
            with open(h3_path, 'rb') as f:
                existing_h3_content = f.read()
            if existing_h3_content == h3_content:
                print(f'Skipping {content_id}.h3 due to existing file with same content.')
                return
        message = f'Downloading [{index}/{len(contents)}] {content_id}.h3...'
        message_suffix = f'({content_size/(1024**2):.2f} MiB)'
        h3_content = download(f'{base_url}/{content_id}.h3', message, message_suffix)
        with open(h3_path, 'wb') as f:
            f.write(h3_content)


def get_contents(tmd):
    count = struct.unpack('>H', tmd[0x1DE:0x1E0])[0]
    contents = []
    for c in range(count):
        content_id = binascii.hexlify(tmd[0xB04 + (0x30 * c):0xB04 + (0x30 * c) + 0x4]).decode('utf-8')
        content_type = struct.unpack('>H', tmd[0xB0A + (0x30 * c):0xB0A + (0x30 * c) + 0x2])[0]
        content_size = struct.unpack('>Q', tmd[0xB0C + (0x30 * c):0xB0C + (0x30 * c) + 0x8])[0]
        contents.append((content_id, content_type, content_size, c + 1))
    print(f'Contents: {count}')
    total_size = sum(c[2] for c in contents)
    print(f"Total size: ({total_size / (1024 ** 2)} MiB)")
    return contents


def download(url: str, message: str, message_suffix: str = '') -> bytes:
    with urllib.request.urlopen(url) as response:
        content = b''
        total_size = int(response.headers.get('content-length', 0))
        if total_size > 0:
            print(message, end='', flush=True)
            downloaded_size = 0
            while True:
                chunk = response.read(MAX_BLOCK_SIZE)
                if not chunk:
                    break
                content += chunk
                downloaded_size += len(chunk)
                percent = round(downloaded_size * 100.0 / total_size, 1)
                text = f'\r{message} ({len(content)/1024/1024:.2f} MiB / {total_size/1024/1024:.2f} MiB) ({percent}%) {message_suffix}'
                print(text, end='', flush=True)
            print('')
        else:
            content = response.read()
    return content


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print(f'usage: {sys.argv[0]} <titleid> <titlekey> [version]')
        print('Latest version is downloaded, if no version is specified.')
        sys.exit(1)
    try:
        main(title_id=sys.argv[1].upper(), title_key=sys.argv[2].upper(), version=sys.argv[3] if len(sys.argv) > 3 else None)
    except IndexError:
        print('Invalid number of arguments')
        print(f'usage: {sys.argv[0]} <titleid> <titlekey> [version]')
        print('Latest version is downloaded, if no version is specified.')
        sys.exit(1)
