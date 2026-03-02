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

  // List of available tools
  tools = [
    {
      name: 'Subscriber Data Collector',
      description: 'Consulta datos detallados de suscriptores en la red móvil (LTE/UMTS/GSM) usando su número MSISDN.',
      icon: '📡',
      route: '/subscriber-data-collector',
      color: 'blue'
    }
    // Future tools can be added here easily
  ];

  constructor(
    // Inject services
    private http: HttpRequestsService,
    private auth: AuthService,
    private constService: ConstService,
    // Inject global class
    public globals: Globals,

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
