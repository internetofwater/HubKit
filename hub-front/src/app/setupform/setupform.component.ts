import { Component, OnInit } from '@angular/core';
import { Field } from '../interfaces/field';
import {SETTINGS_FIELDS } from  '../mock/mock-settings-fields';
import {FIELDS } from  '../mock/mock-fields';
import { ApiService } from '../services/api.service';
import { TRANSFORM_CONFIG_SETTINGS } from '../mock/mock-transform_config';
import {HttpClient, HttpEvent, HttpErrorResponse, HttpEventType} from '@angular/common/http';
import { IParameter } from '../interfaces/parameter';
import { IObservation } from '../interfaces/observation';
import * as fileSaver from 'file-saver';



@Component({
  selector: 'app-setupform',
  templateUrl: './setupform.component.html',
  styleUrls: ['./setupform.component.scss']
})
export class SetupformComponent implements OnInit {

  title = 'Internet of Water Data Wizard';

  // field: Field = {
  //   id: 1,
  //   label: 'Excel',
  //   value: '',
  //   placeholder: ''
  // };


  answer = {
    data_source:""
  }
  
  config = {
    
  }

  add_new_parameter_is_active = false;
  
  setting_fields = SETTINGS_FIELDS;
  form_parameters:IParameter;
  form_reading:IObservation;
  transform_config;
  config_response:any;
  process_response:any;
  fields = FIELDS;
  test = "";
  sheet_selected = "";
  upload_type = "file"; // or web
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

  groups = [
    {
      "group_name": "Settings",
      "group_order": 1,
      "visibility": true,
      "layout": {
          "columns": 1
      }
    },
    // {
    //   "group_name": "Things",
    //   "group_order": 2,
    //   "visibility": true,
    //   "layout": {
    //       "columns": 1
    //   }
    // },
    // {
    //   "group_name": "Location",
    //   "group_order": 3,
    //   "visibility": true,
    //   "layout": {
    //       "columns": 1
    //   }
    // },
  ]

  fileName = '';
  successful_load = "";
  configFileName = ''
  successful_config_load = "";


  constructor(private apiService: ApiService, private http: HttpClient) { 
    this.transform_config = TRANSFORM_CONFIG_SETTINGS;
    this.form_parameters = {
      property_name:"",
      property_definition:"",
      property_description:"",
      sensor_name:"",
      sensor_description:"",
      sensor_encoding_type:"",
      sensor_metadata:"",
      unit_name:"",
      unit_symbol:"",
      unit_definition:"",
      observation_type:"",
      id:"",
      name:"",
      description:""
    } 
    this.form_reading = {
      id:"",
      name:"",
      phenomenonTime:"",
      result:""
    }
    this.config_response = {}
    this.process_response = {}    
  }

  reset_form_parameters():IParameter{

    let result = {
      property_name:"",
      property_definition:"",
      property_description:"",
      sensor_name:"",
      sensor_description:"",
      sensor_encoding_type:"",
      sensor_metadata:"",
      unit_name:"",
      unit_symbol:"",
      unit_definition:"",
      observation_type:"",
      id:"",
      name:"",
      description:""
      
    } 

    return result
  }

  reset_form_reading():IObservation{

    let result = {
      id:"",
      name:"",
      phenomenonTime:"",
      result:""

    } 

    return result
  }

  get_column_letter(csv:string):string{

    var result = ""

    var field = csv?csv.split(','):"";

    if  (field.length>0){

      result = field[1]
      
    }

    return result
  }

  onAddToThings(payload:any):void{


    var mapped_to = payload["mapped_to"]?payload["mapped_to"]:"";
    var field_name = "";
    var field = payload["field"]?payload.field.split(','):"";
    var sheet = payload["sheet"]?payload["sheet"]:"";
    var value = "";


    if  (field.length>0){
      
      field_name = field[0];
      value = field[1];
    }

  
    this.transform_config.Things.fields.push(
      {
        type:"single",
        mapped_to:mapped_to,
        field_source_type:"text",
        field_name:field_name,
        sheet:sheet,
        value_type:"sheet",
        value:value,
        data_source:"sheet"
      }
    )
  }

  onFileSelected(event: any) {

    const file:File = event.target.files[0];

    if (file) {

        this.fileName = file.name;

        const formData = new FormData();

        formData.append('file', file);

        const upload$ = this.http.post("http://localhost:5000/v1/upload-file", formData);

        upload$.subscribe(file_contents => this.file_contents_local = file_contents);

        this.successful_load = "File has loaded";

        this.transform_config.settings.source = this.fileName;

    }
}

upload_via_url(event: any) {

  console.log( this.transform_config.settings.file_url);
  const payload = {"file_path":this.transform_config.settings.file_url}

  this.apiService.get_data_from_url(payload)
    .subscribe(payload => this.file_contents_local = payload);

  // const file:File = event.target.files[0];

  // if (file) {

  //     this.fileName = file.name;

  //     const formData = new FormData();

  //     formData.append('file', file);

  //     const upload$ = this.http.post("http://localhost:5000/v1/upload-file", formData);

  //     upload$.subscribe(file_contents => this.file_contents_local = file_contents);

  //     this.successful_load = "File has loaded";

  //     this.transform_config.settings.source = this.fileName;

  // }
}

onLoadConfig(event:any){
  const file:File = event.target.files[0];

    if (file) {

        this.configFileName = file.name;

        // this.transform_config = {}

        const formData = new FormData();

        formData.append("json", file);

        const upload$ = this.http.post("http://localhost:5000//v1/upload-config", formData);

        upload$.subscribe(transform_config => this.transform_config = transform_config);

        this.successful_config_load = "File has loaded";

        // this.transform_config.settings.source = this.fileName;

    }
  
}

  ngOnInit(): void {
    this.getFields()
  }




  getFields(): void {
    // this.apiService.getFields()
    // .subscribe(test => this.test = test);
    // .subscribe(fields => this.fields = fields);
  }

  create_config():void{

    // this.transform_config.settings.type = 'DUDE' 

    // PREPARE DATA TO BE SENT

    //

    // console.log(this.file_contents_local.features)

    this.apiService.create_config(this.transform_config)
    .subscribe(transform_config => this.transform_config = transform_config);

    let response = JSON.stringify(this.transform_config)

    let blob:any = new Blob([response], { type: 'text/json; charset=utf-8' });
    const url = window.URL.createObjectURL(blob);

			fileSaver.saveAs(blob, 'config.json');
  }


  run_convert():void{

    // this.transform_config.settings.type = 'DUDE' 

    // PREPARE DATA TO BE SENT

    //
    console.log("I was pressed");
    this.apiService.run_convert(this.transform_config)
    .subscribe(config_response => this.config_response = config_response);
  }

  process_data():void{

    // this.transform_config.settings.type = 'DUDE' 

    // PREPARE DATA TO BE SENT

    //
    console.log("I was pressed");
    this.apiService.run_process(this.config_response)
    .subscribe(process_response => this.process_response = process_response);
  }

  post_to_frost_server():void{

    // this.transform_config.settings.type = 'DUDE' 

    // PREPARE DATA TO BE SENT

    //
    console.log("I was pressed");
    this.apiService.post_to_frost_server(this.config_response)
    .subscribe();
  }

  set_sheet_name():void{

    this.transform_config.settings.sheet = this.file_contents_local.features[this.sheet_selected].sheet

  }

  save_parameter():void{

    this.form_reading.name = this.form_parameters.property_name;

    // ANY VALUES IN PARAMS? NO? THEN ADD ONE
    if (this.transform_config.parameters.length===0){
      this.transform_config.parameters.push(this.form_parameters);
    }

    // LOOP THROUGH AND CHECK IF NO MATCHES ADD PARAMS OTHERWISE OVERWRITE
    for (let i=0; i<this.transform_config.parameters.length;i++){
      var item = this.transform_config.parameters[i];
      if (item.property_name === this.form_parameters.property_name){
        item = this.form_parameters;
        break;
      }

      if (i===this.transform_config.parameters.length-1){
        this.transform_config.parameters.push(this.form_parameters);
        break;
      }
    }

    this.form_parameters = this.reset_form_parameters();  
    
    // SAVE READING
    // ANY VALUES IN PARAMS? NO? THEN ADD ONE
    if (this.transform_config.datastreams.length===0){
      this.form_reading.id = 0;
      this.transform_config.datastreams.push(this.form_reading);
    }else{
      // LOOP THROUGH AND CHECK IF NO MATCHES ADD PARAMS OTHERWISE OVERWRITE
      for (let i=0; i<this.transform_config.datastreams.length;i++){
        var item = this.transform_config.datastreams[i];
        if (item.id === this.form_reading.id){
          item = this.form_reading;
          break;
        }

        if (i===this.transform_config.datastreams.length-1){
          this.form_reading.id = this.transform_config.datastreams[this.transform_config.datastreams.length-1].id + 1;
          this.transform_config.datastreams.push(this.form_reading);
        break;
        }
      }

    }





    this.form_reading = this.reset_form_reading();
      
  }

  display_params(property_name:string):void{

    for (let i=0; i<this.transform_config.parameters.length;i++){
      var item = this.transform_config.parameters[i];
      if (item.property_name === property_name){
        this.form_parameters=item
      }
    }

    for (let i=0; i<this.transform_config.datastreams.length;i++){
      var item = this.transform_config.datastreams[i];
      if (item.name === property_name){
        this.form_reading=item
      }
    }

  }

}
