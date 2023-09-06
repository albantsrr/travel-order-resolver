import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { NbButtonModule, NbChatComponent, NbChatCustomMessageService, NbIconComponent, NbIconModule, NbInputModule, NbLayoutModule, NbPopoverModule, NbSidebarModule, NbSidebarService, NbThemeModule, NbToastrModule } from '@nebular/theme';
import { NbChatModule } from '@nebular/theme';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { NbEvaIconsModule } from '@nebular/eva-icons';
import { FormsModule } from '@angular/forms';

@NgModule({
  declarations: [
    AppComponent,
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    AppRoutingModule,
    FormsModule,
    NbInputModule,
    NbThemeModule.forRoot({ name: 'default' }),
    NbLayoutModule,
    NbSidebarModule.forRoot(), // NbSidebarModule.forRoot(), //if this is your app.module
    NbButtonModule,
    NbChatModule.forRoot(),
    NbIconModule,
    NbEvaIconsModule,
    NbPopoverModule,
    NbToastrModule.forRoot(),
  ],
  providers: [NbChatCustomMessageService],
  bootstrap: [AppComponent]
})
export class AppModule { }
