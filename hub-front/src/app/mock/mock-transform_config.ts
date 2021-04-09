import { TransformConfig } from "../interfaces/transformconfig"

export const TRANSFORM_CONFIG_SETTINGS: TransformConfig = 
    { 
        settings:{
            source:"1B-example.xls",
            data_structure:"One Sensor per row",
            type:"Excel",	
            file:""
        },
        Things:{
            name_of_thing:"",
            description:"",
        },
        Location:{
            iot:"",
            location_name:"",
            lat:"",
            lng:"",
        }
    }
