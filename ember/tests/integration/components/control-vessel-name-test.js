import { moduleForComponent, test } from 'ember-qunit';
import hbs from 'htmlbars-inline-precompile';

moduleForComponent('control-vessel-name', 'Integration | Component | control vessel name', {
  integration: true
});

test('it renders', function(assert) {

  // Set any properties with this.set('myProperty', 'value');
  // Handle any actions with this.on('myAction', function(val) { ... });

  this.render(hbs`{{control-vessel-name}}`);

  assert.equal(this.$().text().trim(), '');

  // Template block usage:
  this.render(hbs`
    {{#control-vessel-name}}
      template block text
    {{/control-vessel-name}}
  `);

  assert.equal(this.$().text().trim(), 'template block text');
});
