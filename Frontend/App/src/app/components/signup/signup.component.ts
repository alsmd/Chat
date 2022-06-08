import { Component, OnInit, Output, EventEmitter } from '@angular/core';
import { UserService } from '../../services/user.service';
import {MatSnackBar} from '@angular/material/snack-bar';
import { MatDialogRef } from '@angular/material/dialog';

@Component({
  selector: 'app-signup',
  templateUrl: './signup.component.html',
  styleUrls: ['./signup.component.css']
})
export class SignupComponent implements OnInit {
  username: string = ""
  password: string = ""
  isLoading : boolean = false;
  @Output() token = new EventEmitter<string>()
  constructor(private userService: UserService, private snackBar : MatSnackBar, private dialogRef: MatDialogRef<SignupComponent>) { }

  ngOnInit(): void {
  }

  openSnackBar(message : string, action : string){
    this.snackBar.open(message, action);
  }

  signupAction(){
    if (this.isLoading){
      return ;
    }
    /* if (this.username.length < 3 || this.password.length < 5)
      return ; */
    this.isLoading = true;
    this.userService.signup({"username": this.username, "password": this.password}).subscribe((response: any)=> {
      this.isLoading = false;
      if (response.created){
        localStorage.setItem("token", response.token)
        localStorage.setItem("username", this.username)
        this.openSnackBar("Logado", "close")
        this.dialogRef.close()
      }
    }, (error) => {
      this.isLoading = false;
      this.openSnackBar("Houve um erro: " + error.error.message, "close")
    })
  }

}
