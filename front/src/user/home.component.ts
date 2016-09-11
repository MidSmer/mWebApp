import { Component } from '@angular/core';

import { User } from './user';
import { UserService } from './user.service';

@Component({
  moduleId: module.id,
  selector: 'my-home',
  templateUrl: './home.component.html'
})
export class HomeComponent {
  private user: User;

  constructor(private userService: UserService) {}
}
