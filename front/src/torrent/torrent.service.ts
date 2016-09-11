import { Injectable } from '@angular/core';
import { Http, Headers, Response } from '@angular/http';
import 'rxjs/add/operator/toPromise';
import { Torrent } from './torrent';

@Injectable()
export class TorrentService {
  constructor( private http: Http ) {}

  getTorrents(): Promise<Torrent[]> {
    return this.http.get('/cgi-bin/get-torrent')
               .toPromise()
               .then(response => response.json().data as Torrent[])
               .catch(this.handleError);
  }

  getTorrent(id: number): Promise<Torrent> {
    return this.http.get('/cgi-bin/get-torrent/' + id)
               .toPromise()
               .then(response => response.json().data as Torrent)
               .catch(this.handleError);
  }

  addTorrent(torrent: Torrent): Promise<{code:number, message: string, data?: {id: number}}> {
    let headers = new Headers({'Content-Type': 'application/json'});
    return this.http
               .post('/cgi-bin/add-torrent', JSON.stringify(torrent), {headers: headers})
               .toPromise()
               .then(res => res.json())
               .catch(this.handleError);
  }

  delTorrent(torrent: Torrent): Promise<{code:number, message: string, data?: {id: number}}> {
    return this.http
               .delete('/cgi-bin/del-torrent/' + torrent.id )
               .toPromise()
               .then(res => res.json())
               .catch(this.handleError);
  }

  private handleError(error: any): Promise<any> {
    console.error('An error occurred', error);
    return Promise.reject(error.message || error);
  }
}
