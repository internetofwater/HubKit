
import { Field } from '../interfaces/field';

export const SETTINGS_FIELDS: Field[] = [
  { id: 11, 
    datavalue:'excel', 
    field:{
      "field_name": "data_source",
      "field_label": "Data Source",
      "field_help": "",
      "field_order": 1,
      "field_placeholder": "",
      "is_editable": true,
      "is_custom": false,
      "is_required": false,
      "is_listed": false,
      "component":{
      "name": "select",
      "group":"",
      "options": {
          "values": [
              'Sunny',
              'Overcast',
              'Intermittent Rain',
              'Steady Rain',
              'Heavy Rain',
              'Snow'
          ]
        },
      }
    }
  },
  { id: 12, 
    datavalue:'excel', 
    field:{
      "field_name": "other_text",
      "field_label": "Other Text",
      "field_help": "",
      "field_order": 1,
      "field_placeholder": "",
      "is_editable": true,
      "is_custom": false,
      "is_required": false,
      "is_listed": false,
      "component":{
      "name": "textfield",
      "group":"",
      "options": {
          "values": [
              'Sunny',
              'Overcast',
              'Intermittent Rain',
              'Steady Rain',
              'Heavy Rain',
              'Snow'
          ]
        },
      }
    }
  }
];


