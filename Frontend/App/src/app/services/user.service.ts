import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import {User} from 'src/app/Interfaces/User'
import {environment} from "../../environments/environment"

@Injectable({
  providedIn: 'root'
})
export class UserService {
  url = environment.apiUrl
  constructor(private httpClient : HttpClient) { }

  /**
   * 
   * @param user Login and password
   */
  signup(data : User){
    return this.httpClient.post(this.url + "/user", data, {
      headers: new HttpHeaders()
        .set("Content-Type", "application/json")
    });
  }

  /**
   * 
   * @param user Login and password 
   */
  login(data : User){
    return this.httpClient.post(this.url + "/user/get-token", data, {
      headers: new HttpHeaders()
        .set("Content-Type", "application/json")
    });
  }

  getUsers(token : string){
    return this.httpClient.get(this.url + "/user", {
      headers: new HttpHeaders()
        .set("Content-Type", "application/json")
        .set("Authorization", "Bearer " + token)
    });
  }
}
