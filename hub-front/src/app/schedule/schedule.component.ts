import { Component, OnInit } from '@angular/core';
import { SCHEDULE_LOG } from '../mock/mock-schedule-log';
import { CRON_JOBS } from '../mock/mock-cron-job';
import { ApiService } from '../services/api.service';
import {} from '../interfaces/schedule_cron_job';
import { SCHEDULE_CRON_JOBS } from '../mock/mock-schedule-cron-job';
import {HttpClient, HttpEvent, HttpErrorResponse, HttpEventType} from '@angular/common/http';
import { TRANSFORM_CONFIG_SETTINGS } from '../mock/mock-transform_config';



@Component({
  selector: 'app-schedule',
  templateUrl: './schedule.component.html',
  styleUrls: ['./schedule.component.scss']
})
export class ScheduleComponent implements OnInit {

  logs=SCHEDULE_LOG;
  cron_jobs = CRON_JOBS;
  configFileName = '';
  dataFromUrl = '';
  interval='';
  title = 'Scheduler';
  transform_config;
  schedule_cron_job;
  successful_config_load = "";
  fileUrl = "";


  schedule_cron_job_local:any= {
    config_file:"",
    source:"",
    interval:""
  };

  file_contents_local:any= {
    status:'',
    features : [{
      headers:[{
        column:'',
        row:'',
        value:'test'
      }],
      sheet:'',
      sheet_number:0
    }]
  };

  constructor(private apiService:ApiService, private http: HttpClient) {

    this.schedule_cron_job = SCHEDULE_CRON_JOBS;
    this.transform_config = TRANSFORM_CONFIG_SETTINGS;
   }

  // schedule_cron

  ngOnInit(): void {
  }

  // METHODS
  schedule_cron(config:string,source:string,interval:string,cron_job_name:string){

    this.schedule_cron_job={
      config_file:config,
      source:source,
      interval:interval,
      cron_job_name:cron_job_name
    }
    
    console.log("Schedule Cron",config,source,interval )
    this.apiService.schedule_cron(this.schedule_cron_job)
      .subscribe(schedule_cron_job => this.schedule_cron_job = schedule_cron_job)
  }

  onLoadConfig(event:any){
    if (event.target.files && event.target.files.length > 0){

      const file:File = event.target.files[0];
    
        if (file) {
          this.configFileName = file.name;
  
          const formData = new FormData();
  
          formData.append("json", file);
  
          const upload$ = this.http.post("http://localhost:5000//v1/upload-config", formData);
  
          upload$.subscribe(transform_config => this.transform_config = transform_config);
  
          this.successful_config_load = "File has loaded";      
        }
      }else{
        // TODO: DISPLAY ERROR MESSAGE
      }
    
  }
  upload_via_url(event: any) {

    console.log( this.transform_config.settings.file_url);
    const payload = {"file_path":this.transform_config.settings.file_url}
  
    this.apiService.get_data_from_url(payload)
      .subscribe(payload => this.file_contents_local = payload);
  }

}
