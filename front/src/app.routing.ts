import { Routes, RouterModule } from '@angular/router';

import { LoginComponent } from './user/login.component';
import { HomeComponent } from './user/home.component';

import { AuthGuard } from './user/auth-guard.service';

const appRoutes: Routes = [
  {
    path: '',
    component: HomeComponent,
    canActivate: [ AuthGuard ]
  },
  {
    path: 'login',
    component: LoginComponent
  }
];

export const routing = RouterModule.forRoot(appRoutes);
