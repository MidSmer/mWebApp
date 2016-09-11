import { Component, OnInit } from '@angular/core';
import { Torrent } from './torrent';
import { TorrentService } from './torrent.service';

@Component({
  moduleId: module.id,
  selector: 'my-torrent-list',
  templateUrl: './torrent-list.component.html',
})
export class TorrentListComponent implements OnInit {
  private torrents: Torrent[];

  constructor( private torrentService: TorrentService ) {}

  ngOnInit() {
    this.torrentService.getTorrents().then(
      data => this.torrents = data
    );
  }

  downTorrent(torrent: Torrent) {
    window.open('/cgi-bin/down-torrent/' + torrent.id);
  }

  delTorrent(torrent: Torrent) {
    this.torrentService.delTorrent(torrent).then(res => {
      this.torrents = this.torrents.filter(t => t.id !== res.data.id);
    })
  }
}
