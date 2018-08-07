import { Component, OnInit } from '@angular/core';

// Own services imports
import { HttpRequestsService } from '../../services/utils/http-requests.service';
import { AuthService } from '../../services/auth/auth.service';

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
    // Inject global class
    private globals: Globals,
  ) { }

  ngOnInit() {
    // Post login view was rendered
    this.http.postAppAuditInfo(
      this.globals.appHomeId,
      this.auth.getUserId()
    );
  }

}
