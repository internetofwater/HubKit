import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { SetupformComponent} from './setupform/setupform.component'

const routes: Routes = [
  { path: 'form', component: SetupformComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
