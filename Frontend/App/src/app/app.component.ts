import { Component, OnInit } from '@angular/core';
import { MatDialog, MatDialogConfig } from '@angular/material/dialog';
import { LoginComponent } from './components/login/login.component';
import { SignupComponent } from './components/signup/signup.component';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit{
  isAuth : boolean = false;
  token :string = "";
  username : string = ""
  chatIsOpen : boolean = false;
  title = 'Chat Serverless';
  constructor(private dialog:MatDialog) { }


  ngOnInit(): void {
    setInterval(() => {
      let t= localStorage.getItem("token")
      if (t){
        this.token = t;
        this.isAuth = true;        
      }else{
        this.isAuth = false;
        this.token = ""
      }
    }, 300)
  }

  signupComponent(){
    console.log("here")
    this.dialog.open(SignupComponent, {
      width: '300px',
    });
  }

  loginComponent(){
    console.log("here")
    this.dialog.open(LoginComponent, {
      width: '300px',
    });
  }

  logout(){
    localStorage.removeItem("token");
    localStorage.removeItem("username");
  }

  openChat(name: string){
    this.username = name;
    this.chatIsOpen = true;
  }

  closeChat(){
    this.chatIsOpen = false;
    this.username = "";
  }
}
