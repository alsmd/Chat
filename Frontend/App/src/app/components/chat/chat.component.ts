import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';
import {MatInputModule} from '@angular/material/input'
import {Message} from 'src/app/Interfaces/Message'
import { ChatService } from 'src/app/services/chat.service';
@Component({
  selector: 'app-chat',
  templateUrl: './chat.component.html',
  styleUrls: ['./chat.component.css']
})



export class ChatComponent implements OnInit {
  @Input() token: string = ""
  @Input() username: string = ""
  @Output() closeEvent = new EventEmitter()
  text:string= "";
  chatId: string = ""
  id : any = null;

  /* messages : Message[] = [
    {message: "Opa como ta", owner: "user"},
    {message: "To bom asod aoskd osakdoas k oasdko sakdo a", owner: "outside"},
    {message: "Que lingua é essa?", owner: "user"},
    {message: " asodkoaksd oaskdka odskao oasko", owner: "user"},
    {message: "Acho que é assim", owner: "user"},
  ] */
  messages : any = []
  constructor(private chatService : ChatService) { }

  ngOnInit(): void {
    this.chatService.connect(this.token, this.username).subscribe((response : any) => {
      this.chatId = response.chatId
      this.scrollDown()
      console.log(this.chatId)
      this.id = setInterval(() => {
        this.chatService.getMessages(this.token, this.chatId).subscribe((response : any) => {
          let scroll = false;
          if (response.length > this.messages.length)
            scroll = true;
          this.messages = response
          if (scroll)
            this.scrollDown()
        }, (error) => {
          console.log(error)
        })
      }, 300)
    }, (error) => {
      console.log(error)
      this.closeEvent.emit();
    })
  }

  ngOnDestroy() {
    if (this.id) {
      clearInterval(this.id);
    }
  }

  sendMessage(){
    this.scrollDown()
    this.chatService.sendMessage(this.token, this.chatId, this.text).subscribe((response) => {
      this.text = "";
      this.scrollDown()
    }, (error) => {
      console.log(error)
    })
  }

  scrollDown(){
    setTimeout(() =>{
      let area = document.querySelector(".message-area")
      area?.scroll({top: area.scrollHeight, behavior: "smooth"})
    }, 100)
  }

  close(){
    this.closeEvent.emit()
  }

  

}
