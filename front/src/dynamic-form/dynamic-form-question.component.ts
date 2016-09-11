import { Component, Input } from '@angular/core';
import { FormGroup } from '@angular/forms';
import { QuestionBase }     from './question-base';
@Component({
  selector: 'my-df-question',
  templateUrl: 'app/my-dynamic-form-question.component.html'
})
export class DynamicFormQuestionComponent {
  @Input() question: QuestionBase<any>;
  @Input() form: FormGroup;
  get isValid() { return this.form.controls[this.question.key].valid; }
}
