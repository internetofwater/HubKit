import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { SetupformComponent} from './setupform/setupform.component';
import { ScheduleComponent } from './schedule/schedule.component';

const routes: Routes = [
  { path: '', component: SetupformComponent },
  { path: 'schedule', component: ScheduleComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
