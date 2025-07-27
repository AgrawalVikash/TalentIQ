import { Routes } from '@angular/router';
import { LoginComponent } from './components/login/login.component';
import { CandidateDashboardComponent } from './components/candidate/candidate-dashboard/candidate-dashboard.component';

export const routes: Routes = [
  { path: '', component: LoginComponent },
  { path: 'dashboard', component: CandidateDashboardComponent }
];
