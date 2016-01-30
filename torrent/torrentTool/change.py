# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 16:38:58 2015
@author: aneasystone
"""

import libtorrent as lt
import time

'''
    transfer a torrent file to a magnet link
'''
def torrent2magnet(torrent_file):

    info = lt.torrent_info(torrent_file)
    link = "magnet:?xt=urn:btih:%s&dn=%s" % (info.info_hash(), info.name())
    return link

'''
    transfer a magnet link to a torrent file
'''
def magnet2torrent(link):

    sess = lt.session()
    sess.add_dht_router('router.bittorrent.com', 6881)
    sess.add_dht_router('router.utorrent.com', 6881)
    sess.add_dht_router('router.bitcomet.com', 6881)
    sess.add_dht_router('dht.transmissionbt.com', 6881)
    sess.start_dht();

    params = {
        "save_path": '/tmp/tor',
        # "storage_mode":lt.storage_mode_t.storage_mode_sparse,
        #"paused": True,
        #"auto_managed": True,
        "duplicate_is_error": True
    }
    handle = lt.add_magnet_uri(sess, link, params)

    # waiting for metadata
    for x in xrange(1,20):
        if (not handle.has_metadata()):
            time.sleep(6)
        else:
            break

    sess.pause()
    if (not handle.has_metadata()):
        return {'status':404, 'message':u'没有取到种子'}

    # create a torrent
    torinfo = handle.get_torrent_info()
    torfile = lt.create_torrent(torinfo)
    torcontent = lt.bencode(torfile.generate())
    torname = torinfo.name()
    sess.remove_torrent(handle, 1)

    return {'status':200, 'name':torname, 'data':torcontent}
