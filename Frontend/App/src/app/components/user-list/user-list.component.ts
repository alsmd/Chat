import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';
import { timeInterval } from 'rxjs';
import { UserService } from 'src/app/services/user.service';

@Component({
  selector: 'app-user-list',
  templateUrl: './user-list.component.html',
  styleUrls: ['./user-list.component.css']
})
export class UserListComponent implements OnInit {
  @Input() token: string = ""
  @Output() username = new EventEmitter<string>()
  users : any =  []
  data : any =  []
  itemPerPage = 5
  itemQuantity = 0

  pageObject : any = null;
  constructor(private userService : UserService) { }

  ngOnInit(): void {
    this.userService.getUsers(this.token).subscribe((response) =>{
      this.data = response;
      this.itemQuantity = this.data.length
      this.users = this.data.slice(0, this.itemPerPage)
    }, (error) => {
      console.log(error)
    })
    setInterval(() => {
      if (this.pageObject){
        this.users = this.data.slice(this.pageObject.pageIndex * this.itemPerPage, (this.pageObject.pageIndex * this.itemPerPage) + this.itemPerPage)
      }
    }, 100)
  }

  selectUser(name : string){
    this.username.emit(name)
  }

}
