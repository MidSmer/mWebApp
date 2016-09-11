import { Component, OnInit, OnDestroy } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

import { Subscription } from 'rxjs/Subscription';
import { Torrent } from './torrent';
import { TorrentService } from './torrent.service';

@Component({
  moduleId: module.id,
  selector: 'my-torrent-detail',
  templateUrl: './torrent-detail.component.html',
})
export class TorrentDetailComponent implements OnInit, OnDestroy {
  private sub: Subscription;
  private torrent: Torrent;
  private submitted: boolean = false;
  private note: string;

  constructor( private torrentService: TorrentService,
               private route: ActivatedRoute ) {}

  ngOnInit() {
    this.sub = this.route.params.subscribe(params => {
      if (params['id']) {
        let id = +params['id'];
        this.torrentService.getTorrent(id).then(
          data => this.torrent = data
        );
      } else {
        this.torrent = new Torrent();
      }
    });
  }

  ngOnDestroy() {
    this.sub.unsubscribe();
  }

  onSubmit() {
    this.submitted = true;
    this.torrentService.addTorrent(this.torrent).then(
      (data) => this.note = data.message
    );
  }

  newTorrent() {
    this.torrent = new Torrent();
    this.submitted = false;
  }
}
