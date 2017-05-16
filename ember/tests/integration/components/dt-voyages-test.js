import { moduleForComponent, test } from 'ember-qunit';
import hbs from 'htmlbars-inline-precompile';

moduleForComponent('dt-voyages', 'Integration | Component | dt voyages', {
  integration: true
});

test('it renders', function(assert) {

  // Set any properties with this.set('myProperty', 'value');
  // Handle any actions with this.on('myAction', function(val) { ... });

  this.render(hbs`{{dt-voyages}}`);

  assert.equal(this.$().text().trim(), '');

  // Template block usage:
  this.render(hbs`
    {{#dt-voyages}}
      template block text
    {{/dt-voyages}}
  `);

  assert.equal(this.$().text().trim(), 'template block text');
});
