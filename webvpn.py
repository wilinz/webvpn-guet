from Crypto.Cipher import AES
from binascii import hexlify, unhexlify

key_ = b'wrdvpnisthebest!'
iv_  = b'wrdvpnisthebest!'
institution = 'v.guet.edu.cn'   # Change the hostname here like 'webvpn.xxx.edu.cn'

def getCiphertext(plaintext, key = key_, cfb_iv = iv_, size = 128):
    '''From plantext hostname to ciphertext'''
    
    message = plaintext.encode('utf-8')
    
    cfb_cipher_encrypt = AES.new(key, AES.MODE_CFB, cfb_iv, segment_size = size)       # Must include segment_size
    mid = cfb_cipher_encrypt.encrypt(message)

    return hexlify(mid).decode()


def getPlaintext(ciphertext, key = key_, cfb_iv = iv_, size = 128):
    '''From ciphertext hostname to plaintext'''
    
    message = unhexlify(ciphertext.encode('utf-8'))
    
    cfb_cipher_decrypt = AES.new(key, AES.MODE_CFB, cfb_iv, segment_size = size)
    cfb_msg_decrypt = cfb_cipher_decrypt.decrypt(message).decode('utf-8')
    
    return cfb_msg_decrypt

    return message

def getVPNUrl(url):
    '''From ordinary url to webVPN url'''

    parts = url.split('://')
    pro = parts[0]
    add = parts[1]
    
    hosts = add.split('/')
    domain = hosts[0].split(':')[0]
    port = '-' + hosts[0].split(':')[1] if ":" in hosts[0] else ''
    cph = getCiphertext(domain)
    fold = '/'.join(hosts[1:])

    key = hexlify(iv_).decode('utf-8')
    
    return 'https://' + institution + '/' + pro + port + '/' + key + cph + '/' + fold

def getOrdinaryUrl(url):
    '''From webVPN url to ordinary url'''

    parts = url.split('/')
    pro = parts[3]
    key_cph = parts[4]
    
    if key_cph[:16] == hexlify(iv_).decode('utf-8'):
        print(key_cph[:32])
        return None
    else:
        hostname = getPlaintext(key_cph[32:])
        fold = '/'.join(parts[5:])

        return pro + "://" + hostname + '/' + fold

if __name__ == '__main__':
    #print(getCiphertext('xueshu.baidu.com'))
    #print(getPlaintext('e7e056d2253161546b468aa395'))

    url = 'https://bkjwtest.guet.edu.cn/student/home'
    print('From ordinary url: \n' + getVPNUrl(url))

    VPNUrl = 'https://v.guet.edu.cn/https/77726476706e69737468656265737421f2fc4b8b33357b44300f9ca98c1b2631e4350e37/student/home'
    print('\nFrom webVPN url: \n' + getOrdinaryUrl(VPNUrl))

    
