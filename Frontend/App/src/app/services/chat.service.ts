import { Injectable } from '@angular/core';
import {environment} from "../../environments/environment"
import { HttpClient, HttpHeaders } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class ChatService {
  url = environment.apiUrl

  constructor(private httpClient : HttpClient) { }
  

  connect(token : string, username : string){
    return this.httpClient.post(this.url + "/chat/connect", {
      "connectWith": username
    }, {
      headers: new HttpHeaders()
        .set("Content-Type", "application/json")
        .set("Authorization", "Bearer " + token)
    });
  }

  getMessages(token : string, chatId: string){
    return this.httpClient.post(this.url + "/chat/get-messages", {
      "chatId": chatId
    }, {
      headers: new HttpHeaders()
        .set("Content-Type", "application/json")
        .set("Authorization", "Bearer " + token)
    });
  }

  sendMessage(token : string, chatId : string, message : string){
    return this.httpClient.post(this.url + "/chat/send-message", {
      "chatId": chatId,
      "message": message
    }, {
      headers: new HttpHeaders()
        .set("Content-Type", "application/json")
        .set("Authorization", "Bearer " + token)
    });
  }

}
