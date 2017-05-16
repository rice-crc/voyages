import { moduleForComponent, test } from 'ember-qunit';
import hbs from 'htmlbars-inline-precompile';

moduleForComponent('control-vessel-owner', 'Integration | Component | control vessel owner', {
  integration: true
});

test('it renders', function(assert) {

  // Set any properties with this.set('myProperty', 'value');
  // Handle any actions with this.on('myAction', function(val) { ... });

  this.render(hbs`{{control-vessel-owner}}`);

  assert.equal(this.$().text().trim(), '');

  // Template block usage:
  this.render(hbs`
    {{#control-vessel-owner}}
      template block text
    {{/control-vessel-owner}}
  `);

  assert.equal(this.$().text().trim(), 'template block text');
});
