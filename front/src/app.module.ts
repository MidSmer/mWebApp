import { NgModule }      from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpModule } from '@angular/http';
import { FormsModule } from '@angular/forms';

import { AppComponent }  from './app.component';
import { routing } from './app.routing';

import { HomeComponent } from './user/home.component';
import { TorrentListComponent } from './torrent/torrent-list.component';
import { TorrentDetailComponent } from './torrent/torrent-detail.component';
import { LoginComponent } from './user/login.component';
import { TorrentService } from './torrent/torrent.service';
import { UserService } from './user/user.service';
import { AuthGuard } from './user/auth-guard.service';

@NgModule({
  imports:      [ BrowserModule, HttpModule, FormsModule, routing ],
  declarations: [ AppComponent, TorrentListComponent, TorrentDetailComponent,
     HomeComponent, LoginComponent ],
  bootstrap:    [ AppComponent ],
　providers:    [ TorrentService, UserService, AuthGuard ]
})
export class AppModule { }
