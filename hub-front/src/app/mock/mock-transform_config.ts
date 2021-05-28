import { TransformConfig } from "../interfaces/transformconfig"

export const TRANSFORM_CONFIG_SETTINGS: TransformConfig = 
    { 
        settings:{
            source:"",
            data_structure:"One Sensor per row",
            type:"Excel",
            sheet:"",	
            file:"transform_config.json",
            thing_name_column:"",
            thing_description_column:"",
            thing_lng_column:"",
            thing_lat_column:"",
        },
        parameters:[],
        datastreams:[]
    }


