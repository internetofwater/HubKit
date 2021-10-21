import { Component, OnInit } from '@angular/core';
import { SCHEDULE_LOG } from '../mock/mock-schedule-log';
import { CRON_JOBS } from '../mock/mock-cron-job';

@Component({
  selector: 'app-schedule',
  templateUrl: './schedule.component.html',
  styleUrls: ['./schedule.component.scss']
})
export class ScheduleComponent implements OnInit {

  logs=SCHEDULE_LOG;
  cron_jobs = CRON_JOBS;

  title = 'Scheduler';

  constructor() { }

  ngOnInit(): void {
  }

}
