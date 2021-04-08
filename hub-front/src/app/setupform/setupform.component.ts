import { Component, OnInit } from '@angular/core';
import { Field } from '../interfaces/field';
import {SETTINGS_FIELDS } from  '../mock/mock-settings-fields';
import {FIELDS } from  '../mock/mock-fields';
import { ApiService } from '../services/api.service';
import { TRANSFORM_CONFIG_SETTINGS } from '../mock/mock-transform_config';


@Component({
  selector: 'app-setupform',
  templateUrl: './setupform.component.html',
  styleUrls: ['./setupform.component.scss']
})
export class SetupformComponent implements OnInit {

  // field: Field = {
  //   id: 1,
  //   label: 'Excel',
  //   value: '',
  //   placeholder: ''
  // };

  setting_fields = SETTINGS_FIELDS;
  transform_config = TRANSFORM_CONFIG_SETTINGS;
  fields = FIELDS;
  test = "";

  constructor(private apiService: ApiService) { }

  ngOnInit(): void {
    this.getFields()
  }

  getFields(): void {
    // this.apiService.getFields()
    // .subscribe(test => this.test = test);
    // .subscribe(fields => this.fields = fields);
  }

  create_config():void{
    console.log("I was pressed");
    this.apiService.create_config(this.transform_config)
    .subscribe(transform_config => this.transform_config = transform_config);
  }

}
