import { Component, OnInit } from '@angular/core';

// Own services imports
import { HttpRequestsService } from '../../services/utils/http-requests.service';
import { AuthService } from '../../services/auth/auth.service';
import { ConstService } from '../../services/utils/const.service';
// Import global class
import { Globals } from '../../globals';


@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {

  constructor(
    // Inject services
    private http: HttpRequestsService,
    private auth: AuthService,
    private constService: ConstService,
    // Inject global class
    private globals: Globals,

  ) { }

  ngOnInit() {
    
    if (this.constService.ambiente) {
      // Si es ambiente de producción, incluir posteo de acceso a la herramienta.
      this.http.postAppAuditInfo(
        this.globals.appHomeId,
        this.auth.getUserId()
      ); 
    }
  }

}
