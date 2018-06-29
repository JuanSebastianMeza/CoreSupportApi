import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

// Import Routers
import { RouterModule, Routes, CanActivate } from '@angular/router';

// Import public components
import { LoginComponent } from './public-views/login/login.component';
import { HomeComponent } from './private-views/home/home.component';
import { ChangePasswordComponent } from './private-views/change-password/change-password.component';

// Import own services
import { AuthGuardService as AuthGuard } from './services/auth/auth-guard.service';
import { RoleGuardService as RoleGuard } from './services/auth/role-guard.service';
import { LoginGuardService as LoginGuard } from './services/auth/login-guard.service';

const routes: Routes = [
  // If no route, redirect to /principal
  { path: '', redirectTo: '/login', pathMatch: 'full' },
  // Routes with auth guards
  { path: 'login', 
    component: LoginComponent,
    canActivate: [LoginGuard] },
  // Login children
  { path: '', 
    canActivate: [AuthGuard],
    children: [
      { path: 'home', 
        component: HomeComponent},
      { path: 'password', 
        component: ChangePasswordComponent},
  //     { path: 'comandancia', 
  //       component: CmsCommandComponent, 
  //       canActivate: [RoleGuard],
  //       data: {expectedRole: 'auth.is_command_staff'}},
  //     { path: 'educacion', 
  //       component: CmsEducationComponent, 
  //       canActivate: [RoleGuard],
  //       data: {expectedRole: 'auth.is_education_staff'}},
  //     { path: 'riesgos', 
  //       component: CmsRisksComponent, 
  //       canActivate: [RoleGuard],
  //       data: {expectedRole: 'auth.is_risks_staff'}},
  //     { path: 'admin', 
  //       component: CmsAdminComponent},
    ] 
  },
  // Otherwise declaration
  { path: '**', redirectTo: '/login' }
];

@NgModule({
  imports: [
    CommonModule,
    RouterModule.forRoot(routes)
  ],
  exports: [ RouterModule, ],
  declarations: []
})
export class AppRoutingModule { }
