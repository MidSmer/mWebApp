import { Injectable } from '@angular/core';
import { Http, Headers, Response } from '@angular/http';
import 'rxjs/add/operator/toPromise';
import { User } from './user';

@Injectable()
export class UserService {
  isLoggedIn: boolean = false;

  constructor( private http: Http ) {}

  getUser(): Promise<{code:number, message: string}> {
    return this.http.get('/cgi-bin/get-user')
               .toPromise()
               .then(response => {
                 let data = response.json();
                 if (200 == data.code) {
                   this.isLoggedIn = true;
                 }
                 return data;
               })
               .catch(this.handleError);
  }

  login(user: User): Promise<{id:number}> {
    let headers = new Headers({'Content-Type': 'application/json'});
    return this.http
               .post('/cgi-bin/login', JSON.stringify(user), {headers: headers})
               .toPromise()
               .then(res => {
                 let data = res.json();
                 if (200 == data.code) {
                   this.isLoggedIn = true;
                   return data.data;
                 }
               })
               .catch(this.handleError);
  }

  private handleError(error: any): Promise<any> {
    console.error('An error occurred', error);
    return Promise.reject(error.message || error);
  }
}
