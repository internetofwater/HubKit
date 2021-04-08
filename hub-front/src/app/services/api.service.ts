import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';


import { Observable, of } from 'rxjs';
import { catchError, map, tap } from 'rxjs/operators';

import { FIELDS } from '../mock/mock-fields';
import { Field } from '../interfaces/field';


@Injectable({
  providedIn: 'root'
})
export class ApiService {

  private apiUrl = 'http://localhost:5000/v1/config';  // URL to web api

  httpOptions = {
    headers: new HttpHeaders({ 'Content-Type': 'application/json' })
  };

  constructor(
    private http: HttpClient
  ) { }

  create_config(): Observable<any> {
    return this.http.post<any>(this.apiUrl,'{"data":{"name":"value"}}' , this.httpOptions )
    .pipe(
      tap(_ => this.log('fetched heroes')),
      catchError(this.handleError<any>('create_config', '{data:thing}' ))
    );
  }

  /**
 * Handle Http operation that failed.
 * Let the app continue.
 * @param operation - name of the operation that failed
 * @param result - optional value to return as the observable result
 */
private handleError<T>(operation = 'operation', result?: T) {
  return (error: any): Observable<T> => {

    // TODO: send the error to remote logging infrastructure
    console.error(error); // log to console instead

    // TODO: better job of transforming error for user consumption
    this.log(`${operation} failed: ${error.message}`);

    // Let the app keep running by returning an empty result.
    return of(result as T);
  };
  
}
/** Log a HeroService message with the MessageService */
private log(message: string) {
  // this.messageService.add(`HeroService: ${message}`);
}
  
}


