import struct, base64, binascii, sys, urllib.error, urllib.request, zlib, pathlib


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
        print("Failed to set up signal handling. Graceful exit upon CTRL+C not supported")
## Set up graceful script exiting ##

## Define global vars ##
'''
Lower = more responsive, but slower dl speed.
Higher = less responsive, but higher dl speed.
for most stability, only change last multipulcation value (EX: 10 * 1024 * X)
'''
MAX_BLOCK_SIZE = 10 * 1024 * 250

# Set title.cert, and title.tik info
CERT_DATA = binascii.a2b_hex('00010003704138EFBBBDA16A987DD901326D1C9459484C88A2861B91A312587AE70EF6237EC50E1032DC39DDE89A96A8E859D76A98A6E7E36A0CFE352CA893058234FF833FCB3B03811E9F0DC0D9A52F8045B4B2F9411B67A51C44B5EF8CE77BD6D56BA75734A1856DE6D4BED6D3A242C7C8791B3422375E5C779ABF072F7695EFA0F75BCB83789FC30E3FE4CC8392207840638949C7F688565F649B74D63D8D58FFADDA571E9554426B1318FC468983D4C8A5628B06B6FC5D507C13E7A18AC1511EB6D62EA5448F83501447A9AFB3ECC2903C9DD52F922AC9ACDBEF58C6021848D96E208732D3D1D9D9EA440D91621C7A99DB8843C59C1F2E2C7D9B577D512C166D6F7E1AAD4A774A37447E78FE2021E14A95D112A068ADA019F463C7A55685AABB6888B9246483D18B9C806F474918331782344A4B8531334B26303263D9D2EB4F4BB99602B352F6AE4046C69A5E7E8E4A18EF9BC0A2DED61310417012FD824CC116CFB7C4C1F7EC7177A17446CBDE96F3EDD88FCD052F0B888A45FDAF2B631354F40D16E5FA9C2C4EDA98E798D15E6046DC5363F3096B2C607A9D8DD55B1502A6AC7D3CC8D8C575998E7D796910C804C495235057E91ECD2637C9C1845151AC6B9A0490AE3EC6F47740A0DB0BA36D075956CEE7354EA3E9A4F2720B26550C7D394324BC0CB7E9317D8A8661F42191FF10B08256CE3FD25B745E5194906B4D61CB4C2E000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000526F6F7400000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001434130303030303030330000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000007BE8EF6CB279C9E2EEE121C6EAF44FF639F88F078B4B77ED9F9560B0358281B50E55AB721115A177703C7A30FE3AE9EF1C60BC1D974676B23A68CC04B198525BC968F11DE2DB50E4D9E7F071E562DAE2092233E9D363F61DD7C19FF3A4A91E8F6553D471DD7B84B9F1B8CE7335F0F5540563A1EAB83963E09BE901011F99546361287020E9CC0DAB487F140D6626A1836D27111F2068DE4772149151CF69C61BA60EF9D949A0F71F5499F2D39AD28C7005348293C431FFBD33F6BCA60DC7195EA2BCC56D200BAF6D06D09C41DB8DE9C720154CA4832B69C08C69CD3B073A0063602F462D338061A5EA6C915CD5623579C3EB64CE44EF586D14BAAA8834019B3EEBEED3790001000100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000100042EA66C66CFF335797D0497B77A197F9FE51AB5A41375DC73FD9E0B10669B1B9A5B7E8AB28F01B67B6254C14AA1331418F25BA549004C378DD72F0CE63B1F7091AAFE3809B7AC6C2876A61D60516C43A63729162D280BE21BE8E2FE057D8EB6E204242245731AB6FEE30E5335373EEBA970D531BBA2CB222D9684387D5F2A1BF75200CE0656E390CE19135B59E14F0FA5C1281A7386CCD1C8EC3FAD70FBCE74DEEE1FD05F46330B51F9B79E1DDBF4E33F14889D05282924C5F5DC2766EF0627D7EEDC736E67C2E5B93834668072216D1C78B823A072D34FF3ECF9BD11A29AF16C33BD09AFB2D74D534E027C19240D595A68EBB305ACC44AB38AB820C6D426560C000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000526F6F742D43413030303030303033000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000143503030303030303062000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000137A080BA689C590FD0B2F0D4F56B632FB934ED0739517B33A79DE040EE92DC31D37C7F73BF04BD3E44E20AB5A6FEAF5984CC1F6062E9A9FE56C3285DC6F25DDD5D0BF9FE2EFE835DF2634ED937FAB0214D104809CF74B860E6B0483F4CD2DAB2A9602BC56F0D6BD946AED6E0BE4F08F26686BD09EF7DB325F82B18F6AF2ED525BFD828B653FEE6ECE400D5A48FFE22D538BB5335B4153342D4335ACF590D0D30AE2043C7F5AD214FC9C0FE6FA40A5C86506CA6369BCEE44A32D9E695CF00B4FD79ADB568D149C2028A14C9D71B850CA365B37F70B657791FC5D728C4E18FD22557C4062D74771533C70179D3DAE8F92B117E45CB332F3B3C2A22E705CFEC66F6DA3772B000100010000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000010004919EBE464AD0F552CD1B72E7884910CF55A9F02E50789641D896683DC005BD0AEA87079D8AC284C675065F74C8BF37C88044409502A022980BB8AD48383F6D28A79DE39626CCB2B22A0F19E41032F094B39FF0133146DEC8F6C1A9D55CD28D9E1C47B3D11F4F5426C2C780135A2775D3CA679BC7E834F0E0FB58E68860A71330FC95791793C8FBA935A7A6908F229DEE2A0CA6B9B23B12D495A6FE19D0D72648216878605A66538DBF376899905D3445FC5C727A0E13E0E2C8971C9CFA6C60678875732A4E75523D2F562F12AABD1573BF06C94054AEFA81A71417AF9A4A066D0FFC5AD64BAB28B1FF60661F4437D49E1E0D9412EB4BCACF4CFD6A3408847982000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000526F6F742D43413030303030303033000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000158533030303030303063000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000137A0894AD505BB6C67E2E5BDD6A3BEC43D910C772E9CC290DA58588B77DCC11680BB3E29F4EABBB26E98C2601985C041BB14378E689181AAD770568E928A2B98167EE3E10D072BEEF1FA22FA2AA3E13F11E1836A92A4281EF70AAF4E462998221C6FBB9BDD017E6AC590494E9CEA9859CEB2D2A4C1766F2C33912C58F14A803E36FCCDCCCDC13FD7AE77C7A78D997E6ACC35557E0D3E9EB64B43C92F4C50D67A602DEB391B06661CD32880BD64912AF1CBCB7162A06F02565D3B0ECE4FCECDDAE8A4934DB8EE67F3017986221155D131C6C3F09AB1945C206AC70C942B36F49A1183BCD78B6E4B47C6C5CAC0F8D62F897C6953DD12F28B70C5B7DF751819A98346526250001000100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')
TIK_DATA = binascii.a2b_hex('00010004d15ea5ed15abe11ad15ea5ed15abe11ad15ea5ed15abe11ad15ea5ed15abe11ad15ea5ed15abe11ad15ea5ed15abe11ad15ea5ed15abe11ad15ea5ed15abe11ad15ea5ed15abe11ad15ea5ed15abe11ad15ea5ed15abe11ad15ea5ed15abe11ad15ea5ed15abe11ad15ea5ed15abe11ad15ea5ed15abe11ad15ea5ed15abe11ad15ea5ed15abe11ad15ea5ed15abe11ad15ea5ed15abe11ad15ea5ed15abe11ad15ea5ed15abe11ad15ea5ed15abe11ad15ea5ed15abe11ad15ea5ed15abe11ad15ea5ed15abe11ad15ea5ed15abe11ad15ea5ed15abe11ad15ea5ed15abe11ad15ea5ed15abe11ad15ea5ed15abe11ad15ea5ed15abe11ad15ea5ed15abe11a000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000526f6f742d434130303030303030332d585330303030303030630000000000000000000000000000000000000000000000000000000000000000000000000000feedfacefeedfacefeedfacefeedfacefeedfacefeedfacefeedfacefeedfacefeedfacefeedfacefeedfacefeedfacefeedfacefeedfacefeedface010000cccccccccccccccccccccccccccccccc00000000000000000000000000aaaaaaaaaaaaaaaa00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000010014000000ac000000140001001400000000000000280000000100000084000000840003000000000000ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')
TIK_OFFSET = 0x140
## Define global vars ##


## Using slightly modified ticket patching from FunKiiU ##
def patch_ticket(tikdata, offset, data):
    """Patch a Wii U ticket with the given data."""
    tikdata[TIK_OFFSET + offset : TIK_OFFSET + offset + len(data)] = data


def patch_ticket_demo(tikdata):
    """Patch a Wii U ticket with demo data."""
    patch_ticket(tikdata, 0x124, b'\x00' * 64)


def patch_ticket_dlc(tikdata):
    """Patch a Wii U ticket with DLC data."""
    patch_ticket(tikdata, 0x164, zlib.decompress(base64.b64decode('eNpjYGQQYWBgWAPEIgwQNghoADEjELeAMTNE8D8BwEBjAABCdSH/')))


def generate_ticket(title_id, title_key, title_version, fulloutputpath, patch_demo=False, patch_dlc=False):
    """Generate a Wii U ticket for the given title ID, title key, and title version."""
    tikdata = bytearray(TIK_DATA)
    tikdata[TIK_OFFSET + 0xA6:TIK_OFFSET + 0xA8] = title_version
    tikdata[TIK_OFFSET + 0x9C:TIK_OFFSET + 0xA4] = binascii.a2b_hex(title_id)
    tikdata[TIK_OFFSET + 0x7F:TIK_OFFSET + 0x8F] = binascii.a2b_hex(title_key)
    typecheck = title_id[4:8]
    
    patch_functions = {
        '0002': patch_ticket_demo if patch_demo else None,
        '000C': patch_ticket_dlc if patch_dlc else None
    }
    
    patch_functions.get(typecheck, lambda tikdata: None)(tikdata) if patch_functions.get(typecheck) else None
    open(fulloutputpath, 'wb').write(tikdata)
## Using slightly modified ticket patching from FunKiiU ##    


# Main function, most stuff branches off from here
def main(title_id: str, title_key: str, version: str = None):
    if len(title_id) != 16 or len(title_key) != 32:
        print('Title ID or Title Key is invalid length. Expected length: 16 or 32.')
        print(f'usage: {sys.argv[0]} <titleid> <titlekey>')
        print('Latest version is downloaded, if no version is specified.')
        print('If you do not know where to get the title id/title key of a game go to http://thegamershollow.github.io/wiiu-tdb/')
        print('This tool is for software archival purposes only, thegamershollow does not condone piracy of any kind as it is illigal.')
        sys.exit(1)

    app_categories = {'0000', '0002', '000C', '000E'}
    base_url = f'http://{"ccs." if title_id[4:8] in app_categories else "nus."}cdn.c.shop.nintendowifi.net/ccs/download/{title_id}'
    
    if title_id[4:8] not in app_categories:
        print('Invalid Title ID / Title Key')
        sys.exit(1)
    
    suffix = {'0000': '_Game', '000E': '_Update', '000C': '_DLC', '0002': '_Demo'}.get(title_id[4:8], '')
    root_dir = pathlib.Path(title_id + suffix)
    root_dir.mkdir(exist_ok=True)
            
    tmd_url = f'{base_url}/tmd{"." + version if version else ""}'
    tmd = download(tmd_url, f'Downloading: title.tmd...') # this msg appearing early is annoying, but idc enough to fix it
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
        f.write(CERT_DATA)

    for index, content in enumerate(contents, start=1):
        download_content(root_dir, base_url, contents, content, index, version)
    print(f'\nSuccessfully downloaded Title to: {root_dir}')


# Function that sets up files to be downloaded by download function
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


# Function that returns content info from tmd
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


# Function that downloads the files
def download(url: str, message: str, message_suffix: str = '') -> bytes:
    with urllib.request.urlopen(url) as response:
        content = b''
        total_size = int(response.headers.get('content-length', 0))
        if not total_size:
            content = response.read()
        else:
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
    return content


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print(f'usage: {sys.argv[0]} <titleid> <titlekey>')
        print('Latest version is downloaded, if no version is specified.')
        sys.exit(1)
    try:
        main(title_id=sys.argv[1].upper(), title_key=sys.argv[2].upper(), version=sys.argv[3] if len(sys.argv) > 3 else None)
    except IndexError:
        print('Invalid number of arguments')
        print(f'usage: {sys.argv[0]} <titleid> <titlekey>')
        print('Latest version is downloaded, if no version is specified.')
        sys.exit(1)
