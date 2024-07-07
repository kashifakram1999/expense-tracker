import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

const BASIC_URL = "http://localhost:8000/";

@Injectable({
  providedIn: 'root'
})
export class ExpenseService {

  constructor(private http: HttpClient) { }

  postExpense (expenseDTO: any):Observable<any>{
    return this.http.post(BASIC_URL + 'api/expense', expenseDTO)
  }
}
