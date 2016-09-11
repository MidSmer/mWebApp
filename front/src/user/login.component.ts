import { Component, OnInit } from '@angular/core';
import { Router }    from '@angular/router';

import { User } from './user';
import { UserService } from './user.service';

@Component({
  moduleId: module.id,
  selector: 'my-login',
  templateUrl: './login.component.html'
})
export class LoginComponent implements OnInit {
  model = new User(0, '', '');
  submitted = false;

  constructor(private userService: UserService, private router: Router) {}

  ngOnInit() {
    this.userService.getUser().then(() => {
      if (this.userService.isLoggedIn) {
        this.router.navigate(['']);
      }
    });
  }

  onSubmit() {
    this.submitted = true;

    this.userService.login(this.model).then(() => {
      if (this.userService.isLoggedIn) {
        this.router.navigate(['']);
      }
    });
  }
}
