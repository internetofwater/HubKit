import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';


import { Observable, of } from 'rxjs';
import { catchError, map, tap } from 'rxjs/operators';

import { FIELDS } from '../mock/mock-fields';
import { Field } from '../interfaces/field';
import { TransformConfig } from '../interfaces/transformconfig';
import { ScheduleCronJob } from '../interfaces/schedule_cron_job';


@Injectable({
  providedIn: 'root'
})
export class ApiService {

 // private apiUrl = 'http://localhost:5000/v1';  // URL to web api
 // private frost_apiUrl = 'http://localhost:8080/FROST-Server/v1.1/Things';  // URL to web api
  private apiUrl =  window.location.origin + '/v1';  // URL to web api
  private frost_apiUrl = window.location.origin + '/FROST-Server/v1.1/Things';  // URL to web api

  httpOptions = {
    headers: new HttpHeaders({ 'Content-Type': 'application/json' })
  };

  constructor(
    private http: HttpClient
  ) { }

  create_config(transform_config: TransformConfig): Observable<TransformConfig> {
    return this.http.post<TransformConfig>(this.apiUrl+"/config",transform_config , this.httpOptions )
    .pipe(
      tap(_ => this.log('post config')),
      catchError(this.handleError<TransformConfig>('create_config', transform_config ))
    );
  }

  schedule_cron(schedule_cron_job: ScheduleCronJob): Observable<ScheduleCronJob> {
    return this.http.post<ScheduleCronJob>(this.apiUrl+"/schedule",schedule_cron_job , this.httpOptions )
    .pipe(
      tap(_ => this.log('post config')),
      catchError(this.handleError<ScheduleCronJob>('create_config', schedule_cron_job ))
    );
  }

  get_data_from_url(payload: any): Observable<any> {
    return this.http.post<any>(this.apiUrl+"/upload-file-url",payload , this.httpOptions )
    .pipe(
      tap(_ => this.log('post config')),
      catchError(this.handleError<any>('get file via url', payload ))
    );
  }

  get_cron_jobs(): Observable<any> {
    return this.http.get<any>(this.apiUrl+"/cron", this.httpOptions )
    .pipe(
      tap(_ => this.log('get list of crong jobs')),
      catchError(this.handleError<any>('did not get cron job list' ))
    );
  }

  delete_all_cron_jobs(): Observable<any> {
    return this.http.delete<any>(this.apiUrl+"/cron/delete-all", this.httpOptions )
    .pipe(
      tap(_ => this.log('Delete all cron jobs')),
      catchError(this.handleError<any>('did not delete all cron jobs' ))
    );
  }

  delete_cron_job(job:string): Observable<any> {
    return this.http.delete<any>(this.apiUrl+"/cron?name="+job, this.httpOptions )
    .pipe(
      tap(_ => this.log('delete job')),
      catchError(this.handleError<any>('did not delete the cron job' ))
    );
  }

  run_process(config_response: any): Observable<TransformConfig> {

    return this.http.post<TransformConfig>(this.apiUrl+"/process", config_response, this.httpOptions )
    .pipe(
      tap(_ => this.log('run_process')),
      catchError(this.handleError<TransformConfig>('run_process', config_response ))
    );
  }
  post_to_frost_server(config_response: any): Observable<TransformConfig> {


    if (config_response.Datastreams && config_response.Datastreams.length === 0){
      delete config_response.Datastreams;
    }
    if (config_response.Locations && config_response.Locations.length === 0){
      delete config_response.Locations;
    }



    return this.http.post<TransformConfig>(this.frost_apiUrl,config_response , this.httpOptions )
    .pipe(
      tap(_ => this.log('post convert')),
      catchError(this.handleError<TransformConfig>('run_convert', config_response ))
    );
  }

  run_convert(transform_config: TransformConfig): Observable<TransformConfig> {

    let payload = {
      source:transform_config.settings.source,
      config:transform_config.settings.file
    }

    return this.http.post<TransformConfig>(this.apiUrl+"/convert",payload , this.httpOptions )
    .pipe(
      tap(_ => this.log('post convert')),
      catchError(this.handleError<TransformConfig>('run_convert', payload ))
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


