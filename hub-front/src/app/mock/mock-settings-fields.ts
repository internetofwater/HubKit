
import { Field } from '../interfaces/field';

export const SETTINGS_FIELDS: Field[] = [
  { id: 1, 
    datavalue:'', 
    field:{
      "model" : "settings",
      "param" : "type",
      "field_name": "data_source",
      "field_label": "Data Source",
      "field_help": "",
      "field_order": 1,
      "field_placeholder": "",
      "is_editable": true,
      "is_custom": false,
      "is_required": true,
      "is_listed": false,
      "component":{
      "name": "select",
      "group":"",
      "options": {
          "values": [
              'Excel',
              'csv'
          ]
        },
      }
    }
  },
  { id: 2, 
    datavalue:'', 
    field:{
      "model" : "settings",
      "param" : "data_structure",
      "field_name": "data_structure",
      "field_label": "Data Structure",
      "field_help": "",
      "field_order": 1,
      "field_placeholder": "",
      "is_editable": true,
      "is_custom": false,
      "is_required": true,
      "is_listed": false,
      "component":{
      "name": "select",
      "group":"",
      "options": {
          "values": [
              'Multiple sensors per row',
              'One Sensor per row'
          ]
        },
      }
    }
  },
  { id: 3, 
    datavalue:'', 
    field:{
      "model" : "settings",
      "param" : "source",
      "field_name": "upload_data",
      "field_label": "Upload Data",
      "field_help": "",
      "field_order": 3,
      "field_placeholder": "",
      "is_editable": true,
      "is_custom": false,
      "is_required": true,
      "is_listed": false,
      "component":{
      "name": "textfield",
      "group":"",
      "options": {
        },
      }
    }
  }
];


