import { Component, OnInit } from '@angular/core';
import { UserService } from 'src/app/services/user.service';
import {MatSnackBar} from '@angular/material/snack-bar';
import { MatDialogRef } from '@angular/material/dialog';


@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {
  password : string = ""
  username : string = ""
  isLoading : boolean = false;
  constructor(private userService: UserService, private snackBar : MatSnackBar, private dialogRef: MatDialogRef<LoginComponent>) { }

  ngOnInit(): void {
  }

  openSnackBar(message : string, action : string){
    this.snackBar.open(message, action);
  }

  loginAction(){
    if (this.isLoading){
      return ;
    }
    /* if (this.username.length < 3 || this.password.length < 5)
      return ; */
    this.isLoading = true;
    this.userService.login({"username": this.username, "password": this.password}).subscribe((response: any)=> {
      this.isLoading = false;
      localStorage.setItem("token", response.token)
      localStorage.setItem("username", this.username)
      this.openSnackBar("Logado", "close")
      this.dialogRef.close()
    }, (error) => {
      this.isLoading = false;
      this.openSnackBar("Houve um erro: " + error.error.message, "close")
    })
  }
}
